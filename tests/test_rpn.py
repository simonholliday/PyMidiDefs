"""Tests for pymididefs.rpn — Registered Parameter Number constants."""

import re

import pymididefs.cc
import pymididefs.rpn


class TestRPNConstants:

	def test_pitch_bend_sensitivity (self) -> None:
		"""(0, 0) — required by GM1."""
		assert pymididefs.rpn.PITCH_BEND_SENSITIVITY == 0

	def test_channel_fine_tuning (self) -> None:
		"""(0, 1) — required by GM1."""
		assert pymididefs.rpn.CHANNEL_FINE_TUNING == 1

	def test_channel_coarse_tuning (self) -> None:
		"""(0, 2) — required by GM1."""
		assert pymididefs.rpn.CHANNEL_COARSE_TUNING == 2

	def test_tuning_program_select (self) -> None:
		assert pymididefs.rpn.TUNING_PROGRAM_SELECT == 3

	def test_tuning_bank_select (self) -> None:
		assert pymididefs.rpn.TUNING_BANK_SELECT == 4

	def test_modulation_depth_range (self) -> None:
		"""(0, 5) — added in GM2."""
		assert pymididefs.rpn.MODULATION_DEPTH_RANGE == 5


class TestNullParameter:

	def test_value (self) -> None:
		"""NULL parameter is sent as MSB = 127, LSB = 127."""
		assert pymididefs.rpn.NULL_PARAMETER == 16383

	def test_matches_byte_pair (self) -> None:
		"""NULL_PARAMETER equals the 14-bit packing of (127, 127)."""
		assert pymididefs.rpn.NULL_PARAMETER == pymididefs.cc.unpack_14bit(127, 127)


class TestRPNRange:

	def test_parameter_max (self) -> None:
		"""14-bit parameter space is 0–16383."""
		assert pymididefs.rpn.PARAMETER_MAX == 16383

	def test_standard_rpns_within_range (self) -> None:
		"""Every standard RPN value is within the 14-bit parameter space."""
		standard_rpns = [
			pymididefs.rpn.PITCH_BEND_SENSITIVITY,
			pymididefs.rpn.CHANNEL_FINE_TUNING,
			pymididefs.rpn.CHANNEL_COARSE_TUNING,
			pymididefs.rpn.TUNING_PROGRAM_SELECT,
			pymididefs.rpn.TUNING_BANK_SELECT,
			pymididefs.rpn.MODULATION_DEPTH_RANGE,
		]
		for value in standard_rpns:
			assert 0 <= value <= pymididefs.rpn.PARAMETER_MAX


class TestRPNMap:

	def test_snake_case_lookup (self) -> None:
		"""Dictionary keys match the constant names in snake_case."""
		assert pymididefs.rpn.RPN_MAP["pitch_bend_sensitivity"] == pymididefs.rpn.PITCH_BEND_SENSITIVITY
		assert pymididefs.rpn.RPN_MAP["channel_fine_tuning"] == pymididefs.rpn.CHANNEL_FINE_TUNING
		assert pymididefs.rpn.RPN_MAP["modulation_depth_range"] == pymididefs.rpn.MODULATION_DEPTH_RANGE
		assert pymididefs.rpn.RPN_MAP["null_parameter"] == pymididefs.rpn.NULL_PARAMETER

	def test_keys_are_snake_case (self) -> None:
		"""All keys are lowercase snake_case identifiers."""
		pattern = re.compile(r"^[a-z][a-z0-9_]*$")
		for key in pymididefs.rpn.RPN_MAP:
			assert pattern.match(key), f"RPN_MAP key {key!r} is not snake_case"

	def test_all_values_in_range (self) -> None:
		"""Every value is within the 14-bit parameter space."""
		for name, value in pymididefs.rpn.RPN_MAP.items():
			assert 0 <= value <= pymididefs.rpn.PARAMETER_MAX, (
				f"RPN_MAP[{name!r}] = {value} is out of range"
			)

	def test_no_duplicate_standard_rpns (self) -> None:
		"""The six standard RPNs each map to a unique parameter number."""
		standard_keys = (
			"pitch_bend_sensitivity",
			"channel_fine_tuning",
			"channel_coarse_tuning",
			"tuning_program_select",
			"tuning_bank_select",
			"modulation_depth_range",
		)
		values = [pymididefs.rpn.RPN_MAP[k] for k in standard_keys]
		assert len(values) == len(set(values))
