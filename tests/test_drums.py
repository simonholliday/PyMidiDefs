"""Tests for pymididefs.drums — the General MIDI percussion key map."""

import inspect
import re

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


class TestDrumNames:

	"""The names the specifications print, declared as data.

	Verified on 2026-10-01 against the documents themselves, not against the
	comments they were promoted from: all 47 names for 35–81 match RP-003's
	Table 3, and all 14 for 27–34 and 82–87 match GM2 Appendix B's STANDARD Set.
	The documents cannot be shipped here, so what these tests hold is the
	shape — and, below, the agreement between the data and the comments it was
	read from, so that correcting one without the other fails.
	"""

	def test_every_note_in_the_key_map_has_a_name (self) -> None:
		"""A page showing the map must not meet a note with nothing to print."""
		named = set(pymididefs.drums.GM_DRUM_NAMES)
		mapped = set(pymididefs.drums.GM_DRUM_MAP.values())

		assert named == mapped, (
			f"named but not in the key map: {sorted(named - mapped)}; "
			f"in the key map but unnamed: {sorted(mapped - named)}"
		)

	def test_the_names_and_the_comments_say_the_same_thing (self) -> None:
		"""Each constant's trailing comment is the name declared for that note.

		The data was promoted from those comments, so this is what stops the two
		drifting: an editor who corrects one has to correct the other. The
		comments are also what a reader of the source sees, and a reference
		library cannot have its source and its data disagree about a name.
		"""
		source = inspect.getsource(pymididefs.drums)
		commented = {
			int(value): comment
			for _, value, comment
			in re.findall(r"^([A-Z][A-Z0-9_]*)\s*=\s*(\d+)\s*#\s*(.+?)\s*$", source, re.M)
		}

		assert commented, "no constant comments were found; has the format changed?"

		disagreements = {
			note: (comment, pymididefs.drums.GM_DRUM_NAMES.get(note))
			for note, comment in commented.items()
			if pymididefs.drums.GM_DRUM_NAMES.get(note) != comment
		}

		assert disagreements == {}, f"comment and name differ: {disagreements}"

	def test_no_name_is_empty_or_padded (self) -> None:
		"""These are printed verbatim, so stray whitespace would show."""
		for note, name in pymididefs.drums.GM_DRUM_NAMES.items():
			assert name == name.strip() != "", f"note {note}: {name!r}"
			assert "  " not in name, f"note {note}: {name!r}"

	def test_the_specifications_own_inconsistencies_are_preserved (self) -> None:
		"""RP-003 is not self-consistent, and this map prints what it prints.

		"Closed Hi Hat" has no hyphen where "Pedal Hi-Hat" does, and "Hi Bongo"
		is abbreviated where "High Timbale" is not. Tidying them would be
		inventing a specification, so these four are pinned deliberately.
		"""
		names = pymididefs.drums.GM_DRUM_NAMES

		assert names[pymididefs.drums.HI_HAT_CLOSED] == "Closed Hi Hat"
		assert names[pymididefs.drums.HI_HAT_PEDAL] == "Pedal Hi-Hat"
		assert names[pymididefs.drums.HIGH_BONGO] == "Hi Bongo"
		assert names[pymididefs.drums.HIGH_TIMBALE] == "High Timbale"


class TestGM2NameVariants:

	def test_every_variant_renames_a_level_1_note (self) -> None:
		"""GM2 only re-spells notes RP-003 already named; it adds none here."""
		for note in pymididefs.drums.GM2_DRUM_NAME_VARIANTS:
			assert pymididefs.drums.is_gm_level_1(note), note
			assert note in pymididefs.drums.GM_DRUM_NAMES, note

	def test_every_variant_actually_differs (self) -> None:
		"""A variant equal to the Level 1 name would be noise in the data."""
		for note, variant in pymididefs.drums.GM2_DRUM_NAME_VARIANTS.items():
			assert variant != pymididefs.drums.GM_DRUM_NAMES[note], note

	def test_the_six_the_documents_disagree_on (self) -> None:
		"""Measured against both documents on 2026-10-01: exactly these six."""
		assert pymididefs.drums.GM2_DRUM_NAME_VARIANTS == {
			42: "Closed Hi-hat",
			44: "Pedal Hi-hat",
			46: "Open Hi-hat",
			48: "High Mid Tom",
			58: "Vibra-slap",
			60: "High Bongo",
		}


class TestGMLevel1Range:

	def test_the_range_is_what_rp_003_requires (self) -> None:
		"""47 sounds, notes 35 to 81, as RP-003 asks of a sound generator."""
		lowest, highest = pymididefs.drums.GM1_PERCUSSION_RANGE

		assert (lowest, highest) == (35, 81)
		assert highest - lowest + 1 == 47

	def test_the_predicate_agrees_with_the_range (self) -> None:
		"""Over every note number, not only the interesting ones."""
		lowest, highest = pymididefs.drums.GM1_PERCUSSION_RANGE

		for note in range(128):
			assert pymididefs.drums.is_gm_level_1(note) == (lowest <= note <= highest)

	def test_the_extensions_are_outside_it (self) -> None:
		"""Everything this module carries beyond the block is GS/GM2."""
		extensions = {
			note for note in pymididefs.drums.GM_DRUM_NAMES
			if not pymididefs.drums.is_gm_level_1(note)
		}

		assert extensions == set(range(27, 35)) | set(range(82, 88))

	def test_percussion_is_on_channel_10 (self) -> None:
		"""Counted from 1, as the specifications count channels."""
		assert pymididefs.drums.PERCUSSION_CHANNEL == 10


class TestSources:

	def test_each_source_is_a_title_and_a_url (self) -> None:
		"""A page prints the pair, so both halves have to be usable."""
		assert pymididefs.drums.SOURCES

		for title, url in pymididefs.drums.SOURCES:
			assert title.strip() == title != ""
			assert url == "" or url.startswith("https://"), url

	def test_both_defining_documents_are_named (self) -> None:
		"""The names come from two documents, and both are credited."""
		titles = " ".join(title for title, _ in pymididefs.drums.SOURCES)

		assert "RP-003" in titles
		assert "RP-024" in titles
