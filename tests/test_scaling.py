"""Tests for pymididefs.scaling — widening and narrowing MIDI values.

Every numeric vector here is one M2-115-U v1.0.2 prints, named by the table it
comes from, so a failure says which published example stopped matching.
"""

import typing

import pytest

import pymididefs.rpn
import pymididefs.scaling


# M2-115 Table 5: Min-Center-Max, 7 bits to 16.
TABLE_5 = [
	(0, 0x0000), (5, 0x0A00), (30, 0x3C00), (32, 0x4000), (64, 0x8000),
	(70, 0x8C30), (96, 0xC104), (120, 0xF1C7), (127, 0xFFFF),
]

# M2-115 Table 6: Min-Center-Max, 7 bits to 32.
TABLE_6 = [
	(0, 0x00000000), (5, 0x0A000000), (30, 0x3C000000), (32, 0x40000000),
	(64, 0x80000000), (70, 0x8C30C30C), (96, 0xC1041041), (120, 0xF1C71C71),
	(127, 0xFFFFFFFF),
]

# M2-115 Table 7: Min-Center-Max, 16 bits to 32.
TABLE_7 = [
	(0, 0x00000000), (5, 0x00050000), (30, 0x001E0000), (16384, 0x40000000),
	(32768, 0x80000000), (40000, 0x9C403880), (49152, 0xC0008001),
	(65000, 0xFDE8FBD1), (65535, 0xFFFFFFFF),
]

# M2-115 Table 8: Min-Center-Max, 16 bits down to 7.
TABLE_8 = [(0x1400, 10), (0x8000, 64), (0xAEBA, 87), (0xFFFF, 127)]

# M2-115 Table 9: zero-extension, 7 bits to 16.
TABLE_9 = [(10, 0x1400), (64, 0x8000), (87, 0xAE00), (127, 0xFE00)]

# M2-115 Table 10: zero-extension, 16 bits down to 7.  The pairs that matter
# are 0xAEBA and 0xAF00, which round apart, and 0xFFFF, which needs clamping.
TABLE_10 = [
	(5120, 10), (5631, 11), (32768, 64), (44544, 87), (44730, 87),
	(44800, 88), (65024, 127), (65535, 127),
]

# M2-104-UM v1.1.2 Appendix D.1.3 prints these four for the same method.
APPENDIX_D = [(10, 0x1400), (64, 0x8000), (87, 0xAEBA), (127, 0xFFFF)]

# Width pairs a MIDI 1.0 value is widened across in practice: 7-bit controllers
# and velocities, 14-bit Registered Controllers and pitch bend, and the 14-bit
# high-resolution velocity of CA-031 widened to MIDI 2.0's 16-bit velocity.
#
# (14, 16) and (7, 8) are here for a second reason. The bit-repeat fill has two
# arms, and which one runs depends on whether the widening is wider than the
# bits there are to repeat. Every published vector and every other pair here
# takes the left-shift arm; without a narrow pair the right-shift arm is never
# executed at all, and a regression in it would ship green.
WIDTH_PAIRS = [(7, 16), (7, 32), (14, 32), (16, 32), (14, 16), (7, 8)]


class TestMinCenterMaxPublishedVectors:

	@pytest.mark.parametrize("source, expected", TABLE_5)
	def test_table_5_widen_7_to_16 (self, source: int, expected: int) -> None:
		"""M2-115 Table 5."""
		assert pymididefs.scaling.min_center_max_up(source, 7, 16) == expected

	@pytest.mark.parametrize("source, expected", TABLE_6)
	def test_table_6_widen_7_to_32 (self, source: int, expected: int) -> None:
		"""M2-115 Table 6."""
		assert pymididefs.scaling.min_center_max_up(source, 7, 32) == expected

	@pytest.mark.parametrize("source, expected", TABLE_7)
	def test_table_7_widen_16_to_32 (self, source: int, expected: int) -> None:
		"""M2-115 Table 7."""
		assert pymididefs.scaling.min_center_max_up(source, 16, 32) == expected

	@pytest.mark.parametrize("source, expected", TABLE_8)
	def test_table_8_narrow_16_to_7 (self, source: int, expected: int) -> None:
		"""M2-115 Table 8."""
		assert pymididefs.scaling.min_center_max_down(source, 16, 7) == expected

	@pytest.mark.parametrize("source, expected", APPENDIX_D)
	def test_appendix_d_agrees_where_it_overlaps (self, source: int, expected: int) -> None:
		"""M2-104 Appendix D.1.3 gives the same answers for the same method.

		The two documents disagree about *which* values this method governs,
		not about the method.  Keeping Appendix D's own four vectors here
		records that, so a change to the algorithm cannot quietly claim the
		older document would have allowed it.
		"""
		assert pymididefs.scaling.min_center_max_up(source, 7, 16) == expected


class TestMinCenterMaxRules:

	"""The three properties M2-115 §3.2 states, checked as rules not samples."""

	@pytest.mark.parametrize("src_bits, dst_bits", WIDTH_PAIRS)
	def test_minimum_stays_minimum (self, src_bits: int, dst_bits: int) -> None:
		"""Zero widens to zero at every resolution."""
		assert pymididefs.scaling.min_center_max_up(0, src_bits, dst_bits) == 0

	@pytest.mark.parametrize("src_bits, dst_bits", WIDTH_PAIRS)
	def test_maximum_stays_maximum (self, src_bits: int, dst_bits: int) -> None:
		"""Every bit set widens to every bit set."""
		widened = pymididefs.scaling.min_center_max_up(
			(1 << src_bits) - 1, src_bits, dst_bits
		)

		assert widened == (1 << dst_bits) - 1

	@pytest.mark.parametrize("src_bits, dst_bits", WIDTH_PAIRS)
	def test_centre_stays_centre (self, src_bits: int, dst_bits: int) -> None:
		"""The centre value of one resolution is the centre of the other.

		M2-115 Table 4 gives these: 0x40 for 7 bits, 0x2000 for 14, 0x8000 for
		16 and 0x80000000 for 32.  The rule is ``TRUNC((highest + 1) / 2)``,
		which for a power-of-two width is the top bit alone.
		"""
		centre = 1 << (src_bits - 1)
		widened = pymididefs.scaling.min_center_max_up(centre, src_bits, dst_bits)

		assert widened == 1 << (dst_bits - 1)

	@pytest.mark.parametrize("src_bits, dst_bits", WIDTH_PAIRS)
	def test_widening_is_monotonic (self, src_bits: int, dst_bits: int) -> None:
		"""A larger value never widens to a smaller one.

		Not stated as a rule, but implied by "smoothly increase from center to
		maximum", and it is what a bit-repeat scheme could plausibly break at
		the seam just above the centre.
		"""
		widened = [
			pymididefs.scaling.min_center_max_up(value, src_bits, dst_bits)
			for value in range(1 << src_bits)
		]

		assert widened == sorted(widened)
		assert len(set(widened)) == len(widened)

	def test_one_bit_widens_to_the_boundaries (self) -> None:
		"""M2-115 §3.3: one bit is its own case, and 1 becomes every bit set."""
		assert pymididefs.scaling.min_center_max_up(0, 1, 16) == 0
		assert pymididefs.scaling.min_center_max_up(1, 1, 16) == 0xFFFF
		assert pymididefs.scaling.min_center_max_up(1, 1, 32) == 0xFFFFFFFF

		# Were the general algorithm let loose on it, 1 would land at the
		# centre, which is the outcome §3.3 singles out as not good enough.
		assert pymididefs.scaling.min_center_max_up(1, 1, 16) != 1 << 15


class TestZeroExtensionPublishedVectors:

	@pytest.mark.parametrize("source, expected", TABLE_9)
	def test_table_9_widen_7_to_16 (self, source: int, expected: int) -> None:
		"""M2-115 Table 9."""
		assert pymididefs.scaling.zero_extension_up(source, 7, 16) == expected

	@pytest.mark.parametrize("source, expected", TABLE_10)
	def test_table_10_narrow_16_to_7 (self, source: int, expected: int) -> None:
		"""M2-115 Table 10."""
		assert pymididefs.scaling.zero_extension_down(source, 16, 7) == expected


class TestZeroExtensionRules:

	def test_the_maximum_does_not_stay_the_maximum (self) -> None:
		"""M2-115 §4.2: the highest value is widened by bit shift alone.

		This is the whole difference between the two methods, and the one a
		caller is most likely to get wrong, so it is asserted against the other
		method rather than against a number alone.
		"""
		assert pymididefs.scaling.zero_extension_up(127, 7, 16) == 0xFE00
		assert pymididefs.scaling.min_center_max_up(127, 7, 16) == 0xFFFF

	def test_minimum_and_centre_still_survive (self) -> None:
		"""M2-115 §4.2 keeps both, and only the maximum behaves differently."""
		assert pymididefs.scaling.zero_extension_up(0, 7, 16) == 0
		assert pymididefs.scaling.zero_extension_up(64, 7, 16) == 0x8000

	def test_narrowing_rounds_rather_than_truncating (self) -> None:
		"""Half the discarded range is added first, so 0xAF00 reaches 88.

		A plain shift — which is what Min-Center-Max does — would give 87 for
		both, and the difference is a step the sender meant.
		"""
		assert pymididefs.scaling.zero_extension_down(0xAF00, 16, 7) == 88
		assert pymididefs.scaling.min_center_max_down(0xAF00, 16, 7) == 87

	def test_narrowing_clamps_instead_of_overflowing (self) -> None:
		"""Rounding can carry past the top; §4.4 clamps it.

		Without the clamp this returns 128, which is not a 7-bit value at all.
		"""
		assert pymididefs.scaling.zero_extension_down(0xFFFF, 16, 7) == 127

		for narrow_bits, wide_bits in WIDTH_PAIRS:
			narrowed = pymididefs.scaling.zero_extension_down(
				(1 << wide_bits) - 1, wide_bits, narrow_bits
			)

			assert narrowed == (1 << narrow_bits) - 1


class TestRoundTrip:

	"""Narrowing a widened value returns it, which both §3.2 and §4.2 require.

	Checked over every value of the narrower resolution rather than sampled.
	This is the test that fails loudest if either algorithm is subtly wrong:
	the bit-repeat scheme and the rounding-and-clamping both have to be exactly
	right for it to hold across a whole domain.
	"""

	@pytest.mark.parametrize("src_bits, dst_bits", WIDTH_PAIRS)
	def test_min_center_max_round_trips (self, src_bits: int, dst_bits: int) -> None:
		"""M2-115 §3.2, over all 2**src_bits values."""
		for value in range(1 << src_bits):
			widened = pymididefs.scaling.min_center_max_up(value, src_bits, dst_bits)
			assert pymididefs.scaling.min_center_max_down(
				widened, dst_bits, src_bits
			) == value

	@pytest.mark.parametrize("src_bits, dst_bits", WIDTH_PAIRS)
	def test_zero_extension_round_trips (self, src_bits: int, dst_bits: int) -> None:
		"""M2-115 §4.2, over all 2**src_bits values."""
		for value in range(1 << src_bits):
			widened = pymididefs.scaling.zero_extension_up(value, src_bits, dst_bits)
			assert pymididefs.scaling.zero_extension_down(
				widened, dst_bits, src_bits
			) == value


class TestWhichMethodAnRPNUses:

	def test_every_registered_parameter_we_define_uses_zero_extension (self) -> None:
		"""M2-115 §4.1, checked against the whole of RPN_MAP.

		Every Registered Parameter this package defines has an index LSB of
		0–8, so all of them scale by zero-extension.  ``NULL_PARAMETER`` is the
		exception and carries no value to scale: it is the "stop listening"
		sentinel, MSB and LSB both 127.

		Asserting over the map rather than over a list of names is what catches
		a parameter added later whose LSB is above 31 — it would need the other
		method, and nothing else here would notice.
		"""
		for name, parameter in pymididefs.rpn.RPN_MAP.items():
			uses_zero_extension = pymididefs.scaling.rpn_uses_zero_extension(parameter)

			if parameter == pymididefs.rpn.NULL_PARAMETER:
				assert not uses_zero_extension, name
			else:
				assert uses_zero_extension, f"{name} ({parameter}) would need Min-Center-Max"

	def test_the_boundary_is_where_the_specification_puts_it (self) -> None:
		"""Index LSB 31 is the last that zero-extends; 32 is the first that does not."""
		assert pymididefs.scaling.rpn_uses_zero_extension(31)
		assert not pymididefs.scaling.rpn_uses_zero_extension(32)

	def test_only_the_index_lsb_decides (self) -> None:
		"""The MSB is the parameter's bank and has no say in the method.

		The 3D Sound Controllers sit at MSB 61, and answer the same way as the
		MIDI 1.0 parameters at MSB 0 because their LSBs are in the same range.
		"""
		assert pymididefs.scaling.rpn_uses_zero_extension(0)
		assert pymididefs.scaling.rpn_uses_zero_extension((61 << 7) | 0)
		assert not pymididefs.scaling.rpn_uses_zero_extension((61 << 7) | 32)
		assert not pymididefs.scaling.rpn_uses_zero_extension((0 << 7) | 127)


class TestRejectedArguments:

	"""A width or value mistake is reported as itself, not as a wrong answer."""

	@pytest.mark.parametrize("widen", [
		pymididefs.scaling.min_center_max_up,
		pymididefs.scaling.zero_extension_up,
	])
	def test_widening_refuses_bad_widths (self, widen: object) -> None:
		"""Widening needs 1 <= src_bits < dst_bits <= 32."""
		assert callable(widen)

		with pytest.raises(ValueError):
			widen(0, 16, 7)          # the wrong way round

		with pytest.raises(ValueError):
			widen(0, 7, 7)           # not a widening at all

		with pytest.raises(ValueError):
			widen(0, 7, 64)          # past the specification's own bound

		with pytest.raises(ValueError):
			widen(0, 0, 16)          # no source resolution

	@pytest.mark.parametrize("narrow", [
		pymididefs.scaling.min_center_max_down,
		pymididefs.scaling.zero_extension_down,
	])
	def test_narrowing_refuses_bad_widths (self, narrow: object) -> None:
		"""Narrowing needs 1 <= dst_bits < src_bits <= 32."""
		assert callable(narrow)

		with pytest.raises(ValueError):
			narrow(0, 7, 16)

		with pytest.raises(ValueError):
			narrow(0, 7, 7)

		with pytest.raises(ValueError):
			narrow(0, 64, 7)

		with pytest.raises(ValueError):
			narrow(0, 16, 0)

	@pytest.mark.parametrize("scale, src_bits, dst_bits", [
		(pymididefs.scaling.min_center_max_up, 7, 16),
		(pymididefs.scaling.zero_extension_up, 7, 16),
		(pymididefs.scaling.min_center_max_down, 16, 7),
		(pymididefs.scaling.zero_extension_down, 16, 7),
	])
	def test_a_value_too_wide_for_its_resolution_is_refused (
		self, scale: object, src_bits: int, dst_bits: int
	) -> None:
		"""Claiming 7 bits and passing 128 is a caller bug, not a value to scale."""
		assert callable(scale)
		highest = (1 << src_bits) - 1

		assert scale(highest, src_bits, dst_bits) >= 0

		with pytest.raises(ValueError):
			scale(highest + 1, src_bits, dst_bits)

		with pytest.raises(ValueError):
			scale(-1, src_bits, dst_bits)

	def test_an_impossible_parameter_number_is_refused (self) -> None:
		"""A Registered Parameter number is 14-bit, like the constants are."""
		with pytest.raises(ValueError):
			pymididefs.scaling.rpn_uses_zero_extension(16384)

		with pytest.raises(ValueError):
			pymididefs.scaling.rpn_uses_zero_extension(-1)


class _Saboteur:

	"""An integer-like object whose every operator fails.

	Only ``__index__`` works. If any scaling function does arithmetic on the
	argument it was handed, rather than on the integer it converted that
	argument to, one of these raises and says so.

	This is what a fixed-width integer does wrong without the conversion, with
	the failure made loud instead of silent: a NumPy ``uint8`` shifted left by
	nine does not grow, it wraps, and nothing complains.
	"""

	def __init__ (self, value: int) -> None:
		self._value = value

	def __index__ (self) -> int:
		return self._value

	def _refuse (self, *_: object) -> typing.NoReturn:
		raise AssertionError("an argument was used without being converted to int")

	__lshift__ = __rlshift__ = __rshift__ = __rrshift__ = _refuse
	__add__ = __radd__ = __sub__ = __rsub__ = _refuse
	__and__ = __rand__ = __or__ = __ror__ = _refuse
	__le__ = __lt__ = __ge__ = __gt__ = _refuse


class TestIntegerConversion:

	"""Any integer is accepted, converted, and nothing else is.

	A caller reading MIDI bytes with ``numpy.frombuffer`` holds fixed-width
	integers, and the arithmetic here wraps on those instead of growing. Before
	the conversion, a ``uint8`` velocity widened 7 to 16 bits returned 32
	instead of 51492, narrowing a ``uint16`` maximum returned 0 instead of
	clamping, and two signed cases did not return at all: the bit-repeat fill
	reached the sign bit, and an arithmetic right shift of a negative number
	settles at -1 rather than emptying.
	"""

	@pytest.mark.parametrize("scale, args", [
		(pymididefs.scaling.min_center_max_up, (87, 7, 16)),
		(pymididefs.scaling.min_center_max_down, (0xAEBA, 16, 7)),
		(pymididefs.scaling.zero_extension_up, (127, 7, 16)),
		(pymididefs.scaling.zero_extension_down, (0xFFFF, 16, 7)),
	])
	def test_arithmetic_never_touches_the_argument (self, scale: object, args: tuple[int, int, int]) -> None:
		"""Every argument is converted first, and the conversion is what is used."""
		assert callable(scale)
		value, src_bits, dst_bits = args

		assert scale(_Saboteur(value), src_bits, dst_bits) == scale(*args)
		assert scale(value, _Saboteur(src_bits), dst_bits) == scale(*args)
		assert scale(value, src_bits, _Saboteur(dst_bits)) == scale(*args)

	@pytest.mark.parametrize("scale, args", [
		(pymididefs.scaling.min_center_max_up, (87, 7, 16)),
		(pymididefs.scaling.min_center_max_down, (0xAEBA, 16, 7)),
		(pymididefs.scaling.zero_extension_up, (127, 7, 16)),
		(pymididefs.scaling.zero_extension_down, (0xFFFF, 16, 7)),
	])
	def test_the_result_is_always_a_plain_int (self, scale: object, args: tuple[int, int, int]) -> None:
		"""A fixed-width argument must not make the return value fixed-width too."""
		assert callable(scale)
		value, src_bits, dst_bits = args

		assert type(scale(_Saboteur(value), src_bits, dst_bits)) is int

	def test_the_chooser_converts_too (self) -> None:
		"""rpn_uses_zero_extension masks its argument, so it converts first."""
		assert pymididefs.scaling.rpn_uses_zero_extension(_Saboteur(0))
		assert not pymididefs.scaling.rpn_uses_zero_extension(_Saboteur(127))

	@pytest.mark.parametrize("not_an_integer", [0.5, 1.0, "7", None, [7], 7j])
	def test_anything_that_is_not_an_integer_is_refused (self, not_an_integer: object) -> None:
		"""Including in the one-bit path, which returns before any arithmetic.

		``min_center_max_up(0.5, 1, 16)`` used to return 65535: the one-bit rule
		only asks whether the value is zero, so a float sailed through a range
		check that compares but never converts.
		"""
		with pytest.raises(TypeError):
			pymididefs.scaling.min_center_max_up(not_an_integer, 1, 16)   # type: ignore[arg-type]

		with pytest.raises(TypeError):
			pymididefs.scaling.min_center_max_up(not_an_integer, 7, 16)   # type: ignore[arg-type]

		with pytest.raises(TypeError):
			pymididefs.scaling.zero_extension_down(0, 16, not_an_integer)  # type: ignore[arg-type]

		with pytest.raises(TypeError):
			pymididefs.scaling.rpn_uses_zero_extension(not_an_integer)     # type: ignore[arg-type]

	def test_bool_is_an_integer_and_is_allowed (self) -> None:
		"""bool subclasses int, so refusing it would be inventing a rule."""
		assert pymididefs.scaling.min_center_max_up(True, 1, 16) == 0xFFFF
		assert pymididefs.scaling.min_center_max_up(False, 1, 16) == 0


class TestNumpyIntegers:

	"""The real case the conversion is for, where NumPy is installed.

	Skipped rather than required: this package has no dependencies and is not
	about to gain one for a test. The Saboteur tests above hold the same
	invariant without NumPy; these prove it against the type that prompted it.
	"""

	def test_widening_a_numpy_scalar_gives_the_same_answer_as_an_int (self) -> None:
		numpy = pytest.importorskip("numpy")

		for dtype in (numpy.uint8, numpy.int8, numpy.uint16, numpy.int16, numpy.int32):
			if numpy.iinfo(dtype).max < 127:
				continue

			widened = pymididefs.scaling.min_center_max_up(dtype(87), 7, 16)

			assert widened == 0xAEBA, dtype
			assert type(widened) is int, dtype

	def test_narrowing_a_numpy_maximum_still_clamps (self) -> None:
		numpy = pytest.importorskip("numpy")

		assert pymididefs.scaling.zero_extension_down(numpy.uint16(0xFFFF), 16, 7) == 127
		assert pymididefs.scaling.zero_extension_down(numpy.uint32(0xFFFFFFFF), 32, 14) == 16383

	def test_a_word_read_from_a_buffer_widens_correctly (self) -> None:
		"""The path that found this: MIDI bytes read straight into NumPy."""
		numpy = pytest.importorskip("numpy")

		velocity = numpy.frombuffer(bytes([0x90, 0x3C, 0x64]), numpy.uint8)[2]

		assert pymididefs.scaling.min_center_max_up(velocity, 7, 16) == 51492
		assert pymididefs.scaling.zero_extension_up(numpy.uint16(16383), 14, 32) == 0xFFFC0000


class TestWhereTheBitRepeatStarts:

	"""The seam between the two halves of the widening algorithm.

	M2-115 §3.3: "For values from minimum to the center, use simple bit
	shifting... Use an expanded bit-repeat scheme for the range from center to
	maximum." Nothing else in this file pins where that changes over. The
	published vectors step over it, monotonicity holds either side of a seam in
	the wrong place, and the round trip tolerates any fill at all, because
	narrowing discards exactly the bits the fill occupies.
	"""

	@pytest.mark.parametrize("src_bits, dst_bits", WIDTH_PAIRS)
	def test_up_to_the_centre_it_is_exactly_a_shift (self, src_bits: int, dst_bits: int) -> None:
		"""Every value from 0 to the centre inclusive, with no fill at all.

		This is the specification's first clause, asserted over the whole lower
		half rather than sampled. A seam placed below the centre puts a fill on
		a value that should not have one, and fails here.
		"""
		centre = 1 << (src_bits - 1)
		scale_bits = dst_bits - src_bits

		for value in range(centre + 1):
			assert pymididefs.scaling.min_center_max_up(value, src_bits, dst_bits) == (
				value << scale_bits
			), f"{value} at {src_bits}->{dst_bits}"

	def test_just_above_the_centre_the_fill_is_already_there (self) -> None:
		"""The first value past the centre is filled, where the fill is nonzero.

		These are computed from §3.3.1's algorithm rather than printed in the
		document, and each was also worked by hand: for 7 to 16 bits, 65 shifts
		to 0x8200 and repeats its low six bits, 1, shifted up by three, giving
		0x8208. A seam one step high returns the bare shift instead.
		"""
		assert pymididefs.scaling.min_center_max_up(65, 7, 16) == 0x8208
		assert pymididefs.scaling.min_center_max_up(0x8001, 16, 32) == 0x80010002
		assert pymididefs.scaling.min_center_max_up(8193, 14, 32) == 0x80040020

	def test_a_narrow_widening_can_have_no_room_to_repeat (self) -> None:
		"""Not every value above the centre gets a nonzero fill, and that is right.

		At 7 to 8 bits there is one new bit and six to repeat, so the repeat is
		shifted down past the end and nothing is filled in. Pinned because it
		looks like the fill failing, and is not: the maximum still reaches the
		maximum, which is what §3.2 requires.
		"""
		assert pymididefs.scaling.min_center_max_up(65, 7, 8) == 130
		assert pymididefs.scaling.min_center_max_up(8193, 14, 16) == 32772
		assert pymididefs.scaling.min_center_max_up(127, 7, 8) == 255


class TestZeroExtensionFillsWithZeros:

	"""Zero-extension's whole purpose: no noise in the low bits.

	§4 exists because Min-Center-Max "adds noise to the values in the upper
	half", and a sender "should not send this noise". A fill of any kind here
	would be that noise, and the round trip cannot see it -- narrowing rounds,
	so up to half a step of noise survives a round trip untouched.
	"""

	@pytest.mark.parametrize("src_bits, dst_bits", WIDTH_PAIRS)
	def test_the_new_low_bits_are_always_zero (self, src_bits: int, dst_bits: int) -> None:
		"""Over every value of the narrower resolution, not a sample."""
		scale_bits = dst_bits - src_bits
		new_bits = (1 << scale_bits) - 1

		for value in range(1 << src_bits):
			widened = pymididefs.scaling.zero_extension_up(value, src_bits, dst_bits)

			assert widened & new_bits == 0, f"{value} at {src_bits}->{dst_bits}"
			assert widened == value << scale_bits

	def test_a_registered_controller_widens_without_noise (self) -> None:
		"""The case §4 is written for, at the width Registered Controllers use.

		Pitch Bend Sensitivity of 2 semitones is 14-bit 256. Widened to 32 bits
		it must be 0x04000000 exactly; a fill would make it 0x0401FFFF or
		similar, which is the noise this method exists to avoid, and the round
		trip would still map it back to 256.
		"""
		assert pymididefs.scaling.zero_extension_up(256, 14, 32) == 0x04000000

	def test_one_bit_lands_halfway_as_documented (self) -> None:
		"""§4.3 says this method should not be used for one bit, and why.

		A single bit widens to the halfway value rather than the maximum, which
		is the reason for the recommendation. It is computed rather than
		refused, because the specification recommends against it and does not
		forbid it, so the documented behaviour is pinned here.
		"""
		assert pymididefs.scaling.zero_extension_up(1, 1, 16) == 0x8000
		assert pymididefs.scaling.zero_extension_up(0, 1, 16) == 0
		assert pymididefs.scaling.min_center_max_up(1, 1, 16) == 0xFFFF


class TestTheIndexBoundaryInFull:

	"""Every index LSB, not only the ones either side of the boundary.

	§4.1 draws the line at 0-31, and probing a handful of indexes leaves most of
	the Min-Center-Max side unconstrained: masking with 0x3F instead of 0x7F
	reclassifies a quarter of all parameter numbers and passes a spot check.
	"""

	@pytest.mark.parametrize("bank", [0, 1, 61, 63, 127])
	def test_zero_to_thirty_one_zero_extend (self, bank: int) -> None:
		for index in range(32):
			assert pymididefs.scaling.rpn_uses_zero_extension((bank << 7) | index)

	@pytest.mark.parametrize("bank", [0, 1, 61, 63, 127])
	def test_thirty_two_to_one_hundred_and_twenty_seven_do_not (self, bank: int) -> None:
		for index in range(32, 128):
			assert not pymididefs.scaling.rpn_uses_zero_extension((bank << 7) | index)

	def test_every_parameter_number_is_decided_by_its_index_alone (self) -> None:
		"""All 16384 of them, so no bank can change the answer."""
		for parameter in range(16384):
			expected = (parameter % 128) < 32

			assert pymididefs.scaling.rpn_uses_zero_extension(parameter) == expected, parameter


class TestTheClaimsTheDocstringsMake:

	"""Prose that states a fact about the data has to be checked like data.

	Each of these is asserted somewhere in this package's docstrings, its
	comments or its README, in more than one place. A statement repeated in five
	places and checked in none is how this project's documentation has gone
	stale before (#1489, #2500).
	"""

	def test_every_registered_parameter_that_carries_a_value_has_a_low_index (self) -> None:
		"""The "index LSB is 0–8" claim, which is restated in several places.

		Adding a Registered Parameter whose index LSB is above 8 would make that
		sentence false everywhere it appears while every other test stayed
		green. If this fails, the parameter is probably fine and the prose needs
		correcting.
		"""
		for name, parameter in pymididefs.rpn.RPN_MAP.items():
			if parameter == pymididefs.rpn.NULL_PARAMETER:
				continue

			assert (parameter & 0x7F) <= 8, (
				f"{name} ({parameter}) has index LSB {parameter & 0x7F}; "
				f"the docstrings and README say every one of these is 0–8"
			)

	def test_the_null_parameter_is_the_only_exception (self) -> None:
		"""The carve-out the prose now makes, pinned so it stays a carve-out of one."""
		not_zero_extended = {
			name for name, parameter in pymididefs.rpn.RPN_MAP.items()
			if not pymididefs.scaling.rpn_uses_zero_extension(parameter)
		}

		assert not_zero_extended == {"null_parameter"}


class TestM2104PublishedVectors:

	"""The vectors M2-104 prints in its own translation rules.

	Appendix D's four for the upscaling method are already covered above. These
	come from the Note On rules either side of it, and are worth keeping because
	they are the specification checking its own arithmetic against a message.
	"""

	def test_velocity_one_widens_as_d_3_1_says (self) -> None:
		"""D.3.1: "MIDI Velocity = 0x01: translates to 0x0200"."""
		assert pymididefs.scaling.min_center_max_up(0x01, 7, 16) == 0x0200

	def test_the_note_off_velocity_d_3_1_requires_is_the_centre (self) -> None:
		"""D.3.1 sends a translated Note Off at velocity 0x8000, the 16-bit centre.

		Not a scaling rule, and that is the point: no widening of 0 produces
		0x8000, so a caller cannot reach the specification's answer by scaling.
		It is pinned here because the module's docstring says so, and because it
		shows why the two jobs are separate.
		"""
		assert pymididefs.scaling.min_center_max_up(0, 7, 16) == 0
		assert pymididefs.scaling.zero_extension_up(0, 7, 16) == 0
		assert 0x8000 == 1 << 15
