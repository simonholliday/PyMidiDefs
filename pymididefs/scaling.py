"""Scaling values between the resolutions MIDI 1.0 and MIDI 2.0 use.

MIDI 2.0 carries the same quantities at wider resolutions: a Control Change
value is 32-bit where MIDI 1.0 had 7, a note velocity 16-bit, and a Registered
Controller 32-bit where an RPN had 14.  The specification defines how to widen
and narrow them, and this module is that arithmetic and nothing else.

**There are two methods, and which one applies depends on what the value is,
not on its width.**  The difference is not a rounding error.  A 7-bit maximum
of 127 widens to 16 bits as ``0xFFFF`` under one method and ``0xFE00`` under
the other:

- :func:`min_center_max_up` and :func:`min_center_max_down` — the default
  (M2-115 §3), for Control Change, note velocity, pitch bend, poly and channel
  pressure, Assignable Controllers (NRPN), and Registered Controllers whose
  index LSB is 32–127.  Minimum, centre and maximum all survive: 0 stays 0,
  the centre stays the centre, and the maximum stays the maximum.
- :func:`zero_extension_up` and :func:`zero_extension_down` — M2-115 §4, which
  *shall* be used for Registered Controllers whose index LSB is 0–31.  It
  shifts, so the maximum does not stay the maximum, and it rounds on the way
  back down.  Min-Center-Max adds noise to the top half of the range of a
  value that means a quantity rather than a proportion, and the specification
  works the example: a pitch round-trips about a third of a cent sharp.

**Every Registered Parameter in :mod:`pymididefs.rpn` that carries a value
uses zero-extension**, because each of those has an index LSB of 0–8.  The one
exception is ``NULL_PARAMETER``, whose LSB is 127: it is the sentinel that stops
a controller listening rather than a value to scale, so which method would apply
to it is moot.  :func:`rpn_uses_zero_extension` answers the question for any
parameter number, so a caller never writes the 0–31 boundary out again.

Scaling is not translation.  Translating a message can mean more than widening
its value, and M2-104's special rules outrank everything here (M2-115 §1.3).
Two of them bite, one in each direction, and both are about a velocity of zero:

- **Narrowing to MIDI 1.0**, a Note On velocity can land on 0, which in MIDI 1.0
  means Note Off.  D.2.1 says to replace it with 1 — or with 0x0080, where the
  14-bit High Resolution Velocity Prefix of CA-031 is in use.
- **Widening to MIDI 2.0**, a MIDI 1.0 Note On whose velocity is *already* 0 is
  a Note Off, and D.3.1 says it "shall be translated to a MIDI 2.0 Protocol Note
  Off message with Velocity 0x8000".  Not a Note On with a widened velocity:
  MIDI 2.0 does not read velocity 0 as a release, so a bridge that widens such a
  message with these functions leaves the note sounding for ever.

Nothing here does either for a caller.  A function that silently changed a
value, let alone a message's type, would be lying about what it computed.

Nor is this every mechanism M2-115 defines.  Its §5 gives a third, for stepped
values and enumerations — a filter mode or a wavetable entry, where a device
uses a handful of settings rather than a range.  That is a different shape of
problem: it divides a resolution into a number of steps, so it needs a step
count rather than a source width, and it is not implemented here.

Sources: M2-115-U v1.0.2, "MIDI 2.0 Bit Scaling and Resolution", §§3–4, whose
algorithms and all 43 of its published test vectors the tests reproduce;
M2-104-UM v1.1.2 Appendix D, which gives the same Min-Center-Max algorithm and
does not describe zero-extension at all.
"""

import operator
import typing

# Everything this module defines, and nothing it imports.  A star-import
# brings the definitions only, and a name added to the module shows up here
# in the same diff, where a reader can see the public surface change.
__all__ = [
	"MAX_RESOLUTION_BITS", "min_center_max_up", "min_center_max_down",
	"zero_extension_up", "zero_extension_down", "rpn_uses_zero_extension",
]


# ── Limits ───────────────────────────────────────────────────────────────────
# The widest field any MIDI 2.0 value occupies, and the bound the
# specification's own algorithms are written to (M2-115 §3.3.1, "dstBits<=32").

MAX_RESOLUTION_BITS = 32


# ── Argument checks ──────────────────────────────────────────────────────────
# Shared by all four scaling functions, so that a width or value mistake is
# reported as itself rather than as a wrong answer.
#
# Every argument is also converted to a Python ``int`` here, and the converted
# values are what the arithmetic below uses.  That is not pedantry.  A caller
# who reads MIDI bytes with ``numpy.frombuffer`` holds fixed-width integers,
# and on those the shifts and additions here silently wrap instead of growing:
# a ``uint8`` velocity widened to 16 bits came back as 32 rather than 51492, a
# ``uint16`` maximum narrowed to 0 rather than clamping to its maximum, and the
# bit-repeat loop, whose fill is shifted right until it empties, never emptied
# at all for a signed type whose sign bit the fill reached.  ``operator.index``
# is the protocol for "this is an integer", so it accepts those and rejects a
# float or a ``Fraction``, which have no business being a MIDI value.

def _as_int (value: typing.SupportsIndex, what: str) -> int:

	"""Convert value to a Python int, rejecting anything not an integer."""

	try:
		return operator.index(value)
	except TypeError:
		raise TypeError(
			f"{what} must be an integer, got {type(value).__name__}"
		) from None


def _check_fits (value: int, bits: int) -> None:

	"""Raise :exc:`ValueError` unless value is representable in bits bits."""

	highest = (1 << bits) - 1

	if not 0 <= value <= highest:
		raise ValueError(
			f"{bits}-bit value must be 0–{highest}, got {value}"
		)


def _check_widening (
	value: typing.SupportsIndex,
	src_bits: typing.SupportsIndex,
	dst_bits: typing.SupportsIndex,
) -> tuple[int, int, int]:

	"""Return the arguments as ints, unless value cannot widen src_bits to dst_bits."""

	value, src_bits, dst_bits = (
		_as_int(value, "value"),
		_as_int(src_bits, "src_bits"),
		_as_int(dst_bits, "dst_bits"),
	)

	if not 1 <= src_bits < dst_bits <= MAX_RESOLUTION_BITS:
		raise ValueError(
			f"cannot widen {src_bits} bits to {dst_bits}: need "
			f"1 <= src_bits < dst_bits <= {MAX_RESOLUTION_BITS}"
		)

	_check_fits(value, src_bits)

	return value, src_bits, dst_bits


def _check_narrowing (
	value: typing.SupportsIndex,
	src_bits: typing.SupportsIndex,
	dst_bits: typing.SupportsIndex,
) -> tuple[int, int, int]:

	"""Return the arguments as ints, unless value cannot narrow src_bits to dst_bits."""

	value, src_bits, dst_bits = (
		_as_int(value, "value"),
		_as_int(src_bits, "src_bits"),
		_as_int(dst_bits, "dst_bits"),
	)

	if not 1 <= dst_bits < src_bits <= MAX_RESOLUTION_BITS:
		raise ValueError(
			f"cannot narrow {src_bits} bits to {dst_bits}: need "
			f"1 <= dst_bits < src_bits <= {MAX_RESOLUTION_BITS}"
		)

	_check_fits(value, src_bits)

	return value, src_bits, dst_bits


# ── Min-Center-Max scaling (M2-115 §3) ───────────────────────────────────────
# The default method, and the only one M2-104 Appendix D describes.  For
# Control Change, note velocity, pitch bend, poly and channel pressure, NRPN,
# and Registered Controllers whose index LSB is 32–127.

def min_center_max_up (
	value: typing.SupportsIndex,
	src_bits: typing.SupportsIndex,
	dst_bits: typing.SupportsIndex,
) -> int:

	"""Widen value, keeping its minimum, centre and maximum where they are.

	Below the centre the value is shifted, which keeps increments even and
	leaves the centre at the centre.  Above it, the new low bits are filled by
	repeating the source's own bits — all but its highest — so values climb
	smoothly to a maximum that is every bit set.

	One bit is not that algorithm's case and M2-115 §3.3 gives it its own
	rule: 0 widens to 0 and 1 widens to every bit set.

	>>> min_center_max_up(64, 7, 16)
	32768
	>>> hex(min_center_max_up(87, 7, 16))
	'0xaeba'
	>>> hex(min_center_max_up(127, 7, 16))
	'0xffff'
	>>> hex(min_center_max_up(1, 1, 16))
	'0xffff'
	"""

	value, src_bits, dst_bits = _check_widening(value, src_bits, dst_bits)

	if src_bits == 1:
		return 0 if value == 0 else (1 << dst_bits) - 1

	scale_bits = dst_bits - src_bits
	widened = value << scale_bits

	if value <= 1 << (src_bits - 1):
		return widened

	repeat_bits = src_bits - 1
	repeated = value & ((1 << repeat_bits) - 1)

	if scale_bits > repeat_bits:
		repeated <<= scale_bits - repeat_bits
	else:
		repeated >>= repeat_bits - scale_bits

	while repeated:
		widened |= repeated
		repeated >>= repeat_bits

	return widened


def min_center_max_down (
	value: typing.SupportsIndex,
	src_bits: typing.SupportsIndex,
	dst_bits: typing.SupportsIndex,
) -> int:

	"""Narrow value by discarding its low bits.

	M2-115 §3.4 says plain bit shifting is "sufficient and accurate enough"
	here, and it is what makes widening reversible: narrowing a value that
	:func:`min_center_max_up` produced returns what went in.

	>>> min_center_max_down(32768, 16, 7)
	64
	>>> min_center_max_down(0xaeba, 16, 7)
	87
	>>> min_center_max_down(0xffff, 16, 7)
	127
	"""

	value, src_bits, dst_bits = _check_narrowing(value, src_bits, dst_bits)

	return value >> (src_bits - dst_bits)


# ── Zero-extension scaling with rounding (M2-115 §4) ─────────────────────────
# What Registered Controllers with an index LSB of 0–31 shall use, which is
# every Registered Parameter pymididefs.rpn defines that carries a value --
# NULL_PARAMETER, at LSB 127, is a sentinel rather than a value.  M2-104
# Appendix D does not mention this method.

def zero_extension_up (
	value: typing.SupportsIndex,
	src_bits: typing.SupportsIndex,
	dst_bits: typing.SupportsIndex,
) -> int:

	"""Widen value by filling the new low bits with zeros.

	The maximum does not stay the maximum: a 7-bit 127 widens to 16 bits as
	``0xFE00``, not ``0xFFFF``.  That is the point of the method.  These values
	mean a quantity in defined units rather than a proportion of a range, so
	their maximum legitimately differs with resolution, and padding with zeros
	is what keeps a sender from transmitting noise in the low bits.

	M2-115 §4.3 says this method *should not* be used to widen a single bit,
	because 1 would land halfway up rather than at the top.  It is computed
	rather than refused — the specification recommends against it and does not
	forbid it — so a caller widening an on/off value wants
	:func:`min_center_max_up`, which has a rule for exactly that case.

	>>> zero_extension_up(64, 7, 16)
	32768
	>>> hex(zero_extension_up(87, 7, 16))
	'0xae00'
	>>> hex(zero_extension_up(127, 7, 16))
	'0xfe00'
	"""

	value, src_bits, dst_bits = _check_widening(value, src_bits, dst_bits)

	return value << (dst_bits - src_bits)


def zero_extension_down (
	value: typing.SupportsIndex,
	src_bits: typing.SupportsIndex,
	dst_bits: typing.SupportsIndex,
) -> int:

	"""Narrow value, rounding to the nearest step and clamping to the maximum.

	Half the discarded range is added before shifting, so the result is the
	closest value the narrower resolution can hold rather than the next one
	down.  Rounding can carry past the top, so the result is clamped: narrowing
	``0xFFFF`` to 7 bits gives 127, where the arithmetic alone would give 128.

	>>> zero_extension_down(0xae00, 16, 7)
	87
	>>> zero_extension_down(0xaeba, 16, 7)
	87
	>>> zero_extension_down(0xaf00, 16, 7)
	88
	>>> zero_extension_down(0xffff, 16, 7)
	127
	"""

	value, src_bits, dst_bits = _check_narrowing(value, src_bits, dst_bits)

	scale_bits = src_bits - dst_bits
	narrowed = (value + (1 << (scale_bits - 1))) >> scale_bits

	return min(narrowed, (1 << dst_bits) - 1)


# ── Which method a Registered Parameter uses (M2-115 §4.1) ───────────────────
# The one piece of dispatch the specification defines, kept here so that no
# caller has to write the boundary out for itself.

def rpn_uses_zero_extension (parameter: typing.SupportsIndex) -> bool:

	"""Does this Registered Parameter scale by zero-extension rather than Min-Center-Max?

	M2-115 §4.1: zero-extension "shall be used on all Registered Controller
	(RPN) Messages where the index (RPN LSB) is 0-31", for compatibility with
	the RPNs the MIDI 1.0 Detailed Specification already defined.  Everything
	above that uses Min-Center-Max.

	The argument is a 14-bit parameter number, as the constants in
	:mod:`pymididefs.rpn` are — the index LSB is its low seven bits.  Every
	Registered Parameter that module defines answers ``True``, apart from
	``NULL_PARAMETER``, which carries no value to scale.

	>>> rpn_uses_zero_extension(0)       # Pitch Bend Sensitivity
	True
	>>> rpn_uses_zero_extension(7808)    # 3D Sound: Azimuth Angle
	True
	>>> rpn_uses_zero_extension(16383)   # RPN Null
	False
	"""

	parameter = _as_int(parameter, "parameter")

	if not 0 <= parameter <= 16383:
		raise ValueError(
			f"RPN parameter number must be 0–16383, got {parameter}"
		)

	return (parameter & 0x7F) <= 31
