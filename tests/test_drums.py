"""Tests for pymididefs.drums — General MIDI Level 1 percussion key map."""

import pymididefs.drums


class TestDrumConstants:

	def test_kick_drums (self) -> None:
		"""Standard GM kick drum assignments."""
		assert pymididefs.drums.KICK_1 == 36
		assert pymididefs.drums.KICK_2 == 35

	def test_snare_drums (self) -> None:
		"""Standard GM snare drum assignments."""
		assert pymididefs.drums.SNARE_1 == 38
		assert pymididefs.drums.SNARE_2 == 40

	def test_hi_hats (self) -> None:
		"""Standard GM hi-hat assignments."""
		assert pymididefs.drums.HI_HAT_CLOSED == 42
		assert pymididefs.drums.HI_HAT_PEDAL == 44
		assert pymididefs.drums.HI_HAT_OPEN == 46

	def test_range (self) -> None:
		"""GM percussion key map spans notes 27–87."""
		assert pymididefs.drums.HIGH_Q == 27
		assert pymididefs.drums.OPEN_SURDO == 87

	def test_all_values_in_range (self) -> None:
		"""Every drum constant must be in the GM percussion range 27–87."""
		for name, value in pymididefs.drums.GM_DRUM_MAP.items():
			assert 27 <= value <= 87, f"GM_DRUM_MAP[{name!r}] = {value} is outside 27–87"


class TestGMDrumMap:

	def test_snake_case_lookup (self) -> None:
		"""Dictionary keys use snake_case matching the constant names."""
		assert pymididefs.drums.GM_DRUM_MAP["kick_1"] == pymididefs.drums.KICK_1
		assert pymididefs.drums.GM_DRUM_MAP["hand_clap"] == pymididefs.drums.HAND_CLAP
		assert pymididefs.drums.GM_DRUM_MAP["cowbell"] == pymididefs.drums.COWBELL

	def test_no_duplicate_values (self) -> None:
		"""Each drum in the map has a unique note number."""
		values = list(pymididefs.drums.GM_DRUM_MAP.values())
		assert len(values) == len(set(values))

	def test_count (self) -> None:
		"""GM Level 1 defines 61 percussion instruments (notes 27–87)."""
		assert len(pymididefs.drums.GM_DRUM_MAP) == 61
