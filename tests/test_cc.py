"""Tests for pymididefs.cc — MIDI Control Change number assignments."""

import pytest

import pymididefs.cc


class TestCCConstants:

	def test_well_known_values (self) -> None:
		"""Spot-check commonly used CC numbers against the spec."""
		assert pymididefs.cc.BANK_SELECT_MSB == 0
		assert pymididefs.cc.MODULATION_WHEEL == 1
		assert pymididefs.cc.VOLUME == 7
		assert pymididefs.cc.PAN == 10
		assert pymididefs.cc.EXPRESSION == 11
		assert pymididefs.cc.SUSTAIN_PEDAL == 64
		assert pymididefs.cc.ALL_NOTES_OFF == 123

	def test_lsb_offset (self) -> None:
		"""LSB controllers are exactly 32 higher than their MSB counterparts."""
		assert pymididefs.cc.BANK_SELECT_LSB == pymididefs.cc.BANK_SELECT_MSB + 32
		assert pymididefs.cc.MODULATION_WHEEL_LSB == pymididefs.cc.MODULATION_WHEEL + 32
		assert pymididefs.cc.VOLUME_LSB == pymididefs.cc.VOLUME + 32
		assert pymididefs.cc.PAN_LSB == pymididefs.cc.PAN + 32

	def test_channel_mode_range (self) -> None:
		"""Channel mode messages occupy CC 120–127."""
		assert pymididefs.cc.ALL_SOUND_OFF == 120
		assert pymididefs.cc.POLY_MODE_ON == 127

	def test_all_values_in_range (self) -> None:
		"""Every constant value must be in the valid CC range 0–127."""
		for name, value in pymididefs.cc.CC_MAP.items():
			assert 0 <= value <= 127, f"CC_MAP[{name!r}] = {value} is out of range"


class TestCCMap:

	def test_snake_case_lookup (self) -> None:
		"""Dictionary keys match the constant names in snake_case."""
		assert pymididefs.cc.CC_MAP["sustain_pedal"] == pymididefs.cc.SUSTAIN_PEDAL
		assert pymididefs.cc.CC_MAP["pan"] == pymididefs.cc.PAN
		assert pymididefs.cc.CC_MAP["filter_cutoff"] == pymididefs.cc.FILTER_CUTOFF

	def test_no_duplicate_values_per_name (self) -> None:
		"""Each key in CC_MAP maps to a unique CC number."""
		values = list(pymididefs.cc.CC_MAP.values())
		assert len(values) == len(set(values))


class TestPack14bit:

	def test_zero (self) -> None:
		assert pymididefs.cc.pack_14bit(0) == (0, 0)

	def test_max (self) -> None:
		assert pymididefs.cc.pack_14bit(16383) == (127, 127)

	def test_pitch_bend_centre (self) -> None:
		"""8192 is the pitch-bend centre value: MSB = 64, LSB = 0."""
		assert pymididefs.cc.pack_14bit(8192) == (64, 0)

	def test_byte_boundaries (self) -> None:
		"""LSB rolls over into MSB at 128."""
		assert pymididefs.cc.pack_14bit(127) == (0, 127)
		assert pymididefs.cc.pack_14bit(128) == (1, 0)

	def test_out_of_range_low (self) -> None:
		with pytest.raises(ValueError):
			pymididefs.cc.pack_14bit(-1)

	def test_out_of_range_high (self) -> None:
		with pytest.raises(ValueError):
			pymididefs.cc.pack_14bit(16384)


class TestUnpack14bit:

	def test_zero (self) -> None:
		assert pymididefs.cc.unpack_14bit(0, 0) == 0

	def test_max (self) -> None:
		assert pymididefs.cc.unpack_14bit(127, 127) == 16383

	def test_pitch_bend_centre (self) -> None:
		assert pymididefs.cc.unpack_14bit(64, 0) == 8192

	def test_msb_out_of_range (self) -> None:
		with pytest.raises(ValueError):
			pymididefs.cc.unpack_14bit(128, 0)
		with pytest.raises(ValueError):
			pymididefs.cc.unpack_14bit(-1, 0)

	def test_lsb_out_of_range (self) -> None:
		with pytest.raises(ValueError):
			pymididefs.cc.unpack_14bit(0, 128)
		with pytest.raises(ValueError):
			pymididefs.cc.unpack_14bit(0, -1)


class TestRoundTrip14bit:

	def test_all_14bit_values (self) -> None:
		"""unpack_14bit(*pack_14bit(v)) == v for every v in 0..=16383."""
		for v in range(16384):
			msb, lsb = pymididefs.cc.pack_14bit(v)
			assert pymididefs.cc.unpack_14bit(msb, lsb) == v
