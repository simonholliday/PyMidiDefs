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

**Every Registered Parameter in :mod:`pymididefs.rpn` uses zero-extension**,
because each one's index LSB is 0–8.  :func:`rpn_uses_zero_extension` answers
that for a parameter number, so a caller never writes the 0–31 boundary out
again.

Scaling is not translation.  Translating a message can mean more than widening
its value, and M2-104's special rules outrank everything here (M2-115 §1.3).
The one that bites: a MIDI 2.0 Note On velocity narrowed to 7 bits can land on
0, which in MIDI 1.0 is a Note Off, so a translator has to raise it to 1.
Nothing here does that for a caller, because a function that silently changed
a value would be lying about what it computed.

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


# ── Range checks ─────────────────────────────────────────────────────────────
# Shared by all four scaling functions, so that a width mistake is reported as
# itself rather than as a wrong answer.

def _check_fits (value: int, bits: int) -> None:

	"""Raise :exc:`ValueError` unless value is representable in bits bits."""

	highest = (1 << bits) - 1

	if not 0 <= value <= highest:
		raise ValueError(
			f"{bits}-bit value must be 0–{highest}, got {value}"
		)


def _check_widening (value: int, src_bits: int, dst_bits: int) -> None:

	"""Raise :exc:`ValueError` unless value can widen from src_bits to dst_bits."""

	if not 1 <= src_bits < dst_bits <= MAX_RESOLUTION_BITS:
		raise ValueError(
			f"cannot widen {src_bits} bits to {dst_bits}: need "
			f"1 <= src_bits < dst_bits <= {MAX_RESOLUTION_BITS}"
		)

	_check_fits(value, src_bits)


def _check_narrowing (value: int, src_bits: int, dst_bits: int) -> None:

	"""Raise :exc:`ValueError` unless value can narrow from src_bits to dst_bits."""

	if not 1 <= dst_bits < src_bits <= MAX_RESOLUTION_BITS:
		raise ValueError(
			f"cannot narrow {src_bits} bits to {dst_bits}: need "
			f"1 <= dst_bits < src_bits <= {MAX_RESOLUTION_BITS}"
		)

	_check_fits(value, src_bits)


# ── Min-Center-Max scaling (M2-115 §3) ───────────────────────────────────────
# The default method, and the only one M2-104 Appendix D describes.  For
# Control Change, note velocity, pitch bend, poly and channel pressure, NRPN,
# and Registered Controllers whose index LSB is 32–127.

def min_center_max_up (value: int, src_bits: int, dst_bits: int) -> int:

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

	_check_widening(value, src_bits, dst_bits)

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


def min_center_max_down (value: int, src_bits: int, dst_bits: int) -> int:

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

	_check_narrowing(value, src_bits, dst_bits)

	return value >> (src_bits - dst_bits)


# ── Zero-extension scaling with rounding (M2-115 §4) ─────────────────────────
# What Registered Controllers with an index LSB of 0–31 shall use, which is
# every Registered Parameter pymididefs.rpn defines.  M2-104 Appendix D does
# not mention this method.

def zero_extension_up (value: int, src_bits: int, dst_bits: int) -> int:

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

	_check_widening(value, src_bits, dst_bits)

	return value << (dst_bits - src_bits)


def zero_extension_down (value: int, src_bits: int, dst_bits: int) -> int:

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

	_check_narrowing(value, src_bits, dst_bits)

	scale_bits = src_bits - dst_bits
	narrowed = (value + (1 << (scale_bits - 1))) >> scale_bits

	return min(narrowed, (1 << dst_bits) - 1)


# ── Which method a Registered Parameter uses (M2-115 §4.1) ───────────────────
# The one piece of dispatch the specification defines, kept here so that no
# caller has to write the boundary out for itself.

def rpn_uses_zero_extension (parameter: int) -> bool:

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

	if not 0 <= parameter <= 16383:
		raise ValueError(
			f"RPN parameter number must be 0–16383, got {parameter}"
		)

	return (parameter & 0x7F) <= 31
