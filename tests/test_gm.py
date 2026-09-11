"""Tests for pymididefs.gm — General MIDI Level 1 instrument program numbers."""

import pymididefs.gm


class TestGMConstants:

	def test_first_instrument (self) -> None:
		"""Program 0 is Acoustic Grand Piano."""
		assert pymididefs.gm.ACOUSTIC_GRAND_PIANO == 0

	def test_last_instrument (self) -> None:
		"""Program 127 is Gunshot."""
		assert pymididefs.gm.GUNSHOT == 127

	def test_well_known_instruments (self) -> None:
		"""Spot-check commonly referenced instruments."""
		assert pymididefs.gm.ELECTRIC_BASS_FINGER == 33
		assert pymididefs.gm.VIOLIN == 40
		assert pymididefs.gm.STRING_ENSEMBLE_1 == 48
		assert pymididefs.gm.TRUMPET == 56
		assert pymididefs.gm.ALTO_SAX == 65
		assert pymididefs.gm.FLUTE == 73

	def test_all_values_in_range (self) -> None:
		"""Every instrument program number must be 0–127."""
		for name, value in pymididefs.gm.GM_INSTRUMENT_MAP.items():
			assert 0 <= value <= 127, f"GM_INSTRUMENT_MAP[{name!r}] = {value} out of range"


class TestGMInstrumentMap:

	def test_count (self) -> None:
		"""GM Level 1 defines exactly 128 instruments."""
		assert len(pymididefs.gm.GM_INSTRUMENT_MAP) == 128

	def test_no_duplicate_values (self) -> None:
		"""Each instrument has a unique program number."""
		values = list(pymididefs.gm.GM_INSTRUMENT_MAP.values())
		assert len(values) == len(set(values))

	def test_snake_case_lookup (self) -> None:
		assert pymididefs.gm.GM_INSTRUMENT_MAP["violin"] == pymididefs.gm.VIOLIN
		assert pymididefs.gm.GM_INSTRUMENT_MAP["acoustic_grand_piano"] == 0


class TestGMInstrumentNames:

	def test_length (self) -> None:
		"""128 names, one per program number."""
		assert len(pymididefs.gm.GM_INSTRUMENT_NAMES) == 128

	def test_indexed_lookup (self) -> None:
		assert pymididefs.gm.GM_INSTRUMENT_NAMES[0] == "Acoustic Grand Piano"
		assert pymididefs.gm.GM_INSTRUMENT_NAMES[40] == "Violin"
		assert pymididefs.gm.GM_INSTRUMENT_NAMES[127] == "Gunshot"

	def test_names_are_gm1s_own_spelling (self) -> None:
		"""RP-003 Table 2, character for character, where it differs from the tidy form.

		0.4 and earlier gave "Clavinet", "Guitar Harmonics", "Synth Strings 1",
		"Synth Brass 1" and "Bagpipe", while claiming to follow the specification.
		"""
		assert pymididefs.gm.GM_INSTRUMENT_NAMES[7] == "Clavi"
		assert pymididefs.gm.GM_INSTRUMENT_NAMES[31] == "Guitar harmonics"
		assert pymididefs.gm.GM_INSTRUMENT_NAMES[50] == "SynthStrings 1"
		assert pymididefs.gm.GM_INSTRUMENT_NAMES[51] == "SynthStrings 2"
		assert pymididefs.gm.GM_INSTRUMENT_NAMES[62] == "SynthBrass 1"
		assert pymididefs.gm.GM_INSTRUMENT_NAMES[63] == "SynthBrass 2"
		assert pymididefs.gm.GM_INSTRUMENT_NAMES[109] == "Bag pipe"

	def test_identifiers_keep_their_spelling (self) -> None:
		"""Constant names and map keys are identifiers, so the corrections leave them alone."""
		assert pymididefs.gm.CLAVINET == 7
		assert pymididefs.gm.GM_INSTRUMENT_MAP["bagpipe"] == 109


class TestGMFamilies:

	def test_count (self) -> None:
		"""16 instrument families."""
		assert len(pymididefs.gm.GM_FAMILIES) == 16

	def test_each_family_has_8_instruments (self) -> None:
		"""Each family spans exactly 8 program numbers."""
		for name, (start, end) in pymididefs.gm.GM_FAMILIES.items():
			assert end - start == 7, f"Family {name!r} spans {end - start + 1} instruments"

	def test_families_cover_full_range (self) -> None:
		"""All families together cover 0–127 without gaps or overlaps."""
		covered = set()

		for start, end in pymididefs.gm.GM_FAMILIES.values():
			for i in range(start, end + 1):
				assert i not in covered, f"Program {i} appears in multiple families"
				covered.add(i)

		assert covered == set(range(128))

	def test_piano_family (self) -> None:
		assert pymididefs.gm.GM_FAMILIES["piano"] == (0, 7)

	def test_sound_effects_family (self) -> None:
		assert pymididefs.gm.GM_FAMILIES["sound_effects"] == (120, 127)
