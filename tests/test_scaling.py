"""Tests for pymididefs.scaling — widening and narrowing MIDI values.

Every numeric vector here is one M2-115-U v1.0.2 prints, named by the table it
comes from, so a failure says which published example stopped matching.
"""

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

# Every width pair a MIDI 1.0 value is widened across in practice: 7-bit
# controllers and velocities, and 14-bit RPNs and pitch bend.
WIDTH_PAIRS = [(7, 16), (7, 32), (14, 32), (16, 32)]


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
