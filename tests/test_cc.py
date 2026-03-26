"""Tests for pymididefs.cc — MIDI Control Change number assignments."""

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
