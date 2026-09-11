"""Tests for pymididefs.drums — the General MIDI percussion key map."""

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
		"""The key map spans notes 27–87: GM Level 1's 35–81 plus the GS/GM2 extras."""
		assert pymididefs.drums.HIGH_Q == 27
		assert pymididefs.drums.OPEN_SURDO == 87

	def test_all_values_in_range (self) -> None:
		"""Every drum constant is within the map's range, 27–87."""
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
		"""The map holds 61 instruments: 47 from GM Level 1 and 14 extended."""
		assert len(pymididefs.drums.GM_DRUM_MAP) == 61

	def test_gm_level_1_block_is_complete_and_contiguous (self) -> None:
		"""GM Level 1 percussion is notes 35–81, every one of them named.

		The fourteen sounds outside that block came from Roland GS and reached
		General MIDI through GM2, so they are not guaranteed on a GM Level 1
		device.  Pinning the boundary keeps the module's docstring honest about
		which of its notes carry that guarantee.
		"""
		notes = set(pymididefs.drums.GM_DRUM_MAP.values())

		assert {n for n in notes if 35 <= n <= 81} == set(range(35, 82))
		assert sorted(n for n in notes if n < 35) == [27, 28, 29, 30, 31, 32, 33, 34]
		assert sorted(n for n in notes if n > 81) == [82, 83, 84, 85, 86, 87]


class TestPrimaryAliases:

	def test_constants_point_to_primary (self) -> None:
		"""Unnumbered names alias the '1' of each pair, by this package's choice."""
		assert pymididefs.drums.KICK == pymididefs.drums.KICK_1 == 36
		assert pymididefs.drums.SNARE == pymididefs.drums.SNARE_1 == 38
		assert pymididefs.drums.CRASH == pymididefs.drums.CRASH_1 == 49
		assert pymididefs.drums.RIDE == pymididefs.drums.RIDE_1 == 51

	def test_alias_map (self) -> None:
		"""GM_DRUM_PRIMARY_ALIASES maps the four bare names to their primary note."""
		assert pymididefs.drums.GM_DRUM_PRIMARY_ALIASES == {
			"kick": 36,
			"snare": 38,
			"crash": 49,
			"ride": 51,
		}

	def test_aliases_kept_separate_from_key_map (self) -> None:
		"""The bare names stay OUT of GM_DRUM_MAP, which is one name per note."""
		for name in pymididefs.drums.GM_DRUM_PRIMARY_ALIASES:
			assert name not in pymididefs.drums.GM_DRUM_MAP
