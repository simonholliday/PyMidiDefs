"""Tests for pymididefs.notes — note constants and name/number conversion."""

import pytest

import pymididefs.notes


class TestNoteConstants:

	def test_c4_is_middle_c (self) -> None:
		"""C4 = 60 per MMA standard."""
		assert pymididefs.notes.C4 == 60

	def test_a4_is_concert_pitch (self) -> None:
		"""A4 = 69 (440 Hz concert pitch reference)."""
		assert pymididefs.notes.A4 == 69

	def test_lowest_note (self) -> None:
		"""C-1 = 0 is the lowest MIDI note."""
		assert pymididefs.notes.C_NEG1 == 0

	def test_highest_note (self) -> None:
		"""G9 = 127 is the highest MIDI note."""
		assert pymididefs.notes.G9 == 127

	def test_chromatic_sequence_octave_4 (self) -> None:
		"""All 12 notes in octave 4 are consecutive from C4 = 60."""

		expected = list(range(60, 72))
		actual = [
			pymididefs.notes.C4, pymididefs.notes.CS4,
			pymididefs.notes.D4, pymididefs.notes.DS4,
			pymididefs.notes.E4,
			pymididefs.notes.F4, pymididefs.notes.FS4,
			pymididefs.notes.G4, pymididefs.notes.GS4,
			pymididefs.notes.A4, pymididefs.notes.AS4,
			pymididefs.notes.B4,
		]

		assert actual == expected

	def test_octave_boundaries (self) -> None:
		"""Each octave starts 12 semitones above the previous."""
		assert pymididefs.notes.C0 == 12
		assert pymididefs.notes.C1 == 24
		assert pymididefs.notes.C2 == 36
		assert pymididefs.notes.C3 == 48
		assert pymididefs.notes.C5 == 72
		assert pymididefs.notes.C6 == 84
		assert pymididefs.notes.C7 == 96
		assert pymididefs.notes.C8 == 108
		assert pymididefs.notes.C9 == 120


class TestNoteToName:

	def test_middle_c (self) -> None:
		assert pymididefs.notes.note_to_name(60) == "C4"

	def test_lowest (self) -> None:
		assert pymididefs.notes.note_to_name(0) == "C-1"

	def test_highest (self) -> None:
		assert pymididefs.notes.note_to_name(127) == "G9"

	def test_sharp (self) -> None:
		assert pymididefs.notes.note_to_name(61) == "C#4"

	def test_out_of_range_low (self) -> None:
		with pytest.raises(ValueError):
			pymididefs.notes.note_to_name(-1)

	def test_out_of_range_high (self) -> None:
		with pytest.raises(ValueError):
			pymididefs.notes.note_to_name(128)


class TestNameToNote:

	def test_natural (self) -> None:
		assert pymididefs.notes.name_to_note("C4") == 60

	def test_sharp (self) -> None:
		assert pymididefs.notes.name_to_note("C#4") == 61

	def test_flat (self) -> None:
		assert pymididefs.notes.name_to_note("Db4") == 61

	def test_negative_octave (self) -> None:
		assert pymididefs.notes.name_to_note("C-1") == 0

	def test_highest (self) -> None:
		assert pymididefs.notes.name_to_note("G9") == 127

	def test_whitespace_stripped (self) -> None:
		assert pymididefs.notes.name_to_note("  A4  ") == 69

	def test_invalid_note_class (self) -> None:
		with pytest.raises(ValueError):
			pymididefs.notes.name_to_note("X4")

	def test_out_of_range (self) -> None:
		with pytest.raises(ValueError):
			pymididefs.notes.name_to_note("C10")


class TestRoundTrip:

	def test_all_128_notes (self) -> None:
		"""note_to_name and name_to_note are inverse for all 128 MIDI notes."""

		for note in range(128):
			name = pymididefs.notes.note_to_name(note)
			assert pymididefs.notes.name_to_note(name) == note


class TestNoteNames:

	def test_length (self) -> None:
		assert len(pymididefs.notes.NOTE_NAMES) == 128

	def test_indexed_by_note_number (self) -> None:
		assert pymididefs.notes.NOTE_NAMES[60] == "C4"
		assert pymididefs.notes.NOTE_NAMES[0] == "C-1"
		assert pymididefs.notes.NOTE_NAMES[127] == "G9"


class TestSemitoneMap:

	def test_enharmonic_equivalents (self) -> None:
		"""C# and Db map to the same semitone offset."""
		assert pymididefs.notes.SEMITONE_MAP["C#"] == pymididefs.notes.SEMITONE_MAP["DB"]

	def test_all_naturals (self) -> None:
		expected = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
		for name, offset in expected.items():
			assert pymididefs.notes.SEMITONE_MAP[name] == offset
