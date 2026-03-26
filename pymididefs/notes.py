"""MIDI note number constants and name/number conversion.

Convention: **C4 = 60** (Middle C), matching the MIDI Manufacturers Association
standard and most DAWs (Ableton, Logic, Reaper, FL Studio).

Notes are named ``<Pitch><Octave>`` for naturals and ``<Pitch>S<Octave>`` for
sharps::

	import pymididefs.notes
	pymididefs.notes.C4    # 60  (Middle C)
	pymididefs.notes.A4    # 69  (Concert pitch, 440 Hz)
	pymididefs.notes.CS3   # 49  (C#3)

For string-based access use :func:`name_to_note` and :func:`note_to_name`::

	pymididefs.notes.name_to_note("Db4")  # 61
	pymididefs.notes.note_to_name(61)     # "C#4"

Source: MIDI 1.0 Detailed Specification, §2 — Data Format.
Note numbering: 0–127 where Middle C (C4) = 60.
"""


# ── Chromatic pitch classes ──────────────────────────────────────────────────
# Indexed by semitone offset within an octave (0 = C, 11 = B).
# Output representation uses sharps only; flats are accepted as input via
# SEMITONE_MAP but are not generated as output.

NOTE_CLASSES: tuple[str, ...] = (
	"C", "C#", "D", "D#", "E", "F",
	"F#", "G", "G#", "A", "A#", "B",
)


# ── Semitone offset map ──────────────────────────────────────────────────────
# Maps note class strings (sharps *and* flats) to their semitone offset 0–11.
# Both enharmonic spellings share the same value (e.g. C# = Db = 1).

SEMITONE_MAP: dict[str, int] = {
	"C": 0, "C#": 1, "DB": 1,
	"D": 2, "D#": 3, "EB": 3,
	"E": 4,
	"F": 5, "F#": 6, "GB": 6,
	"G": 7, "G#": 8, "AB": 8,
	"A": 9, "A#": 10, "BB": 10,
	"B": 11,
}


# ── Conversion functions ─────────────────────────────────────────────────────

def note_to_name (note: int) -> str:

	"""Convert a MIDI note number (0–127) to a human-readable note name.

	Uses sharps only (C#, not Db) and the C4 = 60 convention.
	Octave range in output: -1 (note 0) to 9 (note 127).

	>>> note_to_name(0)
	'C-1'
	>>> note_to_name(60)
	'C4'
	>>> note_to_name(127)
	'G9'
	"""

	if not 0 <= note <= 127:
		raise ValueError(
			f"MIDI note number must be 0–127, got {note}"
		)

	return f"{NOTE_CLASSES[note % 12]}{(note // 12) - 1}"


def name_to_note (name: str) -> int:

	"""Parse a note name string to a MIDI note number (0–127).

	Accepts sharps (C#4, F#2), flats (Db4, Bb2), and naturals (C4, G2).
	Uses the C4 = 60 convention.  Octave numbers from -1 (C-1 = 0) to
	9 (G9 = 127).

	>>> name_to_note("C4")
	60
	>>> name_to_note("Db4")
	61
	>>> name_to_note("C-1")
	0
	"""

	name = name.strip()

	if len(name) < 2:
		raise ValueError(f"Malformed note name {name!r}")

	# Split into note class (letter + optional accidental) and octave.
	# Two-character classes: letter + '#' or 'b' (e.g. "C#", "Db").

	if len(name) >= 2 and name[1] in ("#", "b"):
		note_class = name[:2].upper()
		octave_str = name[2:]
	else:
		note_class = name[:1].upper()
		octave_str = name[1:]

	if note_class not in SEMITONE_MAP:
		raise ValueError(
			f"Unrecognised note class {note_class!r} in {name!r} — "
			f"expected a letter A–G with optional # or b (e.g. C4, D#3, Bb2)"
		)

	try:
		octave = int(octave_str)
	except ValueError:
		raise ValueError(
			f"Malformed note name {name!r} — octave part {octave_str!r} is not an integer"
		) from None

	midi = (octave + 1) * 12 + SEMITONE_MAP[note_class]

	if not 0 <= midi <= 127:
		raise ValueError(
			f"Note {name!r} maps to MIDI {midi}, outside the valid range 0–127 "
			f"(C-1 = 0, G9 = 127)"
		)

	return midi


# ── Note name lookup table ───────────────────────────────────────────────────
# Tuple of 128 human-readable note name strings indexed by MIDI note number.
# Generated from note_to_name() for consistency.

NOTE_NAMES: tuple[str, ...] = tuple(note_to_name(n) for n in range(128))


# ── Octave -1  (MIDI 0–11) ──────────────────────────────────────────────────
# Sub-octave notes.  Rarely used musically but part of the full MIDI range.

C_NEG1  = 0
CS_NEG1 = 1
D_NEG1  = 2
DS_NEG1 = 3
E_NEG1  = 4
F_NEG1  = 5
FS_NEG1 = 6
G_NEG1  = 7
GS_NEG1 = 8
A_NEG1  = 9
AS_NEG1 = 10
B_NEG1  = 11

# ── Octave 0  (MIDI 12–23) ──────────────────────────────────────────────────

C0  = 12
CS0 = 13
D0  = 14
DS0 = 15
E0  = 16
F0  = 17
FS0 = 18
G0  = 19
GS0 = 20
A0  = 21
AS0 = 22
B0  = 23

# ── Octave 1  (MIDI 24–35) ──────────────────────────────────────────────────

C1  = 24
CS1 = 25
D1  = 26
DS1 = 27
E1  = 28
F1  = 29
FS1 = 30
G1  = 31
GS1 = 32
A1  = 33
AS1 = 34
B1  = 35

# ── Octave 2  (MIDI 36–47) ──────────────────────────────────────────────────

C2  = 36
CS2 = 37
D2  = 38
DS2 = 39
E2  = 40
F2  = 41
FS2 = 42
G2  = 43
GS2 = 44
A2  = 45
AS2 = 46
B2  = 47

# ── Octave 3  (MIDI 48–59) ──────────────────────────────────────────────────

C3  = 48
CS3 = 49
D3  = 50
DS3 = 51
E3  = 52
F3  = 53
FS3 = 54
G3  = 55
GS3 = 56
A3  = 57
AS3 = 58
B3  = 59

# ── Octave 4  (MIDI 60–71) ──────────────────────────────────────────────────
# Middle C (C4 = 60) lives here.

C4  = 60
CS4 = 61
D4  = 62
DS4 = 63
E4  = 64
F4  = 65
FS4 = 66
G4  = 67
GS4 = 68
A4  = 69
AS4 = 70
B4  = 71

# ── Octave 5  (MIDI 72–83) ──────────────────────────────────────────────────

C5  = 72
CS5 = 73
D5  = 74
DS5 = 75
E5  = 76
F5  = 77
FS5 = 78
G5  = 79
GS5 = 80
A5  = 81
AS5 = 82
B5  = 83

# ── Octave 6  (MIDI 84–95) ──────────────────────────────────────────────────

C6  = 84
CS6 = 85
D6  = 86
DS6 = 87
E6  = 88
F6  = 89
FS6 = 90
G6  = 91
GS6 = 92
A6  = 93
AS6 = 94
B6  = 95

# ── Octave 7  (MIDI 96–107) ─────────────────────────────────────────────────

C7  = 96
CS7 = 97
D7  = 98
DS7 = 99
E7  = 100
F7  = 101
FS7 = 102
G7  = 103
GS7 = 104
A7  = 105
AS7 = 106
B7  = 107

# ── Octave 8  (MIDI 108–119) ────────────────────────────────────────────────

C8  = 108
CS8 = 109
D8  = 110
DS8 = 111
E8  = 112
F8  = 113
FS8 = 114
G8  = 115
GS8 = 116
A8  = 117
AS8 = 118
B8  = 119

# ── Octave 9  (MIDI 120–127) ────────────────────────────────────────────────
# Partial octave — ends at G9 (127).

C9  = 120
CS9 = 121
D9  = 122
DS9 = 123
E9  = 124
F9  = 125
FS9 = 126
G9  = 127
