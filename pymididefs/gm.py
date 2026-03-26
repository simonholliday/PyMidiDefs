"""General MIDI Level 1 instrument program numbers and families.

All 128 GM Level 1 instrument program numbers (0–127), organised into
16 families of 8 instruments each.  Program numbers are 0-indexed as
sent over MIDI (Program Change message data byte).

Two ways to use this module::

	import pymididefs.gm

	# As named constants
	pymididefs.gm.ACOUSTIC_GRAND_PIANO  # 0
	pymididefs.gm.VIOLIN                # 40

	# As a lookup dictionary
	pymididefs.gm.GM_INSTRUMENT_MAP["violin"]  # 40

	# Human-readable name by program number
	pymididefs.gm.GM_INSTRUMENT_NAMES[40]  # "Violin"

Source: General MIDI Level 1 Specification — Instrument Patch Map.
"""

import typing


# ── Piano (0–7) ──────────────────────────────────────────────────────────────

ACOUSTIC_GRAND_PIANO    = 0
BRIGHT_ACOUSTIC_PIANO   = 1
ELECTRIC_GRAND_PIANO    = 2
HONKY_TONK_PIANO        = 3
ELECTRIC_PIANO_1        = 4   # Rhodes
ELECTRIC_PIANO_2        = 5   # Chorused
HARPSICHORD             = 6
CLAVINET                = 7

# ── Chromatic Percussion (8–15) ──────────────────────────────────────────────

CELESTA                 = 8
GLOCKENSPIEL            = 9
MUSIC_BOX               = 10
VIBRAPHONE              = 11
MARIMBA                 = 12
XYLOPHONE               = 13
TUBULAR_BELLS           = 14
DULCIMER                = 15

# ── Organ (16–23) ────────────────────────────────────────────────────────────

DRAWBAR_ORGAN           = 16
PERCUSSIVE_ORGAN        = 17
ROCK_ORGAN              = 18
CHURCH_ORGAN            = 19
REED_ORGAN              = 20
ACCORDION               = 21
HARMONICA               = 22
TANGO_ACCORDION         = 23

# ── Guitar (24–31) ───────────────────────────────────────────────────────────

ACOUSTIC_GUITAR_NYLON   = 24
ACOUSTIC_GUITAR_STEEL   = 25
ELECTRIC_GUITAR_JAZZ    = 26
ELECTRIC_GUITAR_CLEAN   = 27
ELECTRIC_GUITAR_MUTED   = 28
OVERDRIVEN_GUITAR       = 29
DISTORTION_GUITAR       = 30
GUITAR_HARMONICS        = 31

# ── Bass (32–39) ─────────────────────────────────────────────────────────────

ACOUSTIC_BASS           = 32
ELECTRIC_BASS_FINGER    = 33
ELECTRIC_BASS_PICK      = 34
FRETLESS_BASS           = 35
SLAP_BASS_1             = 36
SLAP_BASS_2             = 37
SYNTH_BASS_1            = 38
SYNTH_BASS_2            = 39

# ── Strings (40–47) ──────────────────────────────────────────────────────────

VIOLIN                  = 40
VIOLA                   = 41
CELLO                   = 42
CONTRABASS              = 43
TREMOLO_STRINGS         = 44
PIZZICATO_STRINGS       = 45
ORCHESTRAL_HARP         = 46
TIMPANI                 = 47

# ── Ensemble (48–55) ─────────────────────────────────────────────────────────

STRING_ENSEMBLE_1       = 48
STRING_ENSEMBLE_2       = 49
SYNTH_STRINGS_1         = 50
SYNTH_STRINGS_2         = 51
CHOIR_AAHS              = 52
VOICE_OOHS              = 53
SYNTH_VOICE             = 54
ORCHESTRA_HIT           = 55

# ── Brass (56–63) ────────────────────────────────────────────────────────────

TRUMPET                 = 56
TROMBONE                = 57
TUBA                    = 58
MUTED_TRUMPET           = 59
FRENCH_HORN             = 60
BRASS_SECTION           = 61
SYNTH_BRASS_1           = 62
SYNTH_BRASS_2           = 63

# ── Reed (64–71) ─────────────────────────────────────────────────────────────

SOPRANO_SAX             = 64
ALTO_SAX                = 65
TENOR_SAX               = 66
BARITONE_SAX            = 67
OBOE                    = 68
ENGLISH_HORN            = 69
BASSOON                 = 70
CLARINET                = 71

# ── Pipe (72–79) ─────────────────────────────────────────────────────────────

PICCOLO                 = 72
FLUTE                   = 73
RECORDER                = 74
PAN_FLUTE               = 75
BLOWN_BOTTLE            = 76
SHAKUHACHI              = 77
WHISTLE                 = 78
OCARINA                 = 79

# ── Synth Lead (80–87) ───────────────────────────────────────────────────────

LEAD_1_SQUARE           = 80
LEAD_2_SAWTOOTH         = 81
LEAD_3_CALLIOPE         = 82
LEAD_4_CHIFF            = 83
LEAD_5_CHARANG          = 84
LEAD_6_VOICE            = 85
LEAD_7_FIFTHS           = 86
LEAD_8_BASS_LEAD        = 87

# ── Synth Pad (88–95) ────────────────────────────────────────────────────────

PAD_1_NEW_AGE           = 88
PAD_2_WARM              = 89
PAD_3_POLYSYNTH         = 90
PAD_4_CHOIR             = 91
PAD_5_BOWED             = 92
PAD_6_METALLIC          = 93
PAD_7_HALO              = 94
PAD_8_SWEEP             = 95

# ── Synth Effects (96–103) ───────────────────────────────────────────────────

FX_1_RAIN               = 96
FX_2_SOUNDTRACK         = 97
FX_3_CRYSTAL            = 98
FX_4_ATMOSPHERE         = 99
FX_5_BRIGHTNESS         = 100
FX_6_GOBLINS            = 101
FX_7_ECHOES             = 102
FX_8_SCI_FI             = 103

# ── Ethnic (104–111) ─────────────────────────────────────────────────────────

SITAR                   = 104
BANJO                   = 105
SHAMISEN                = 106
KOTO                    = 107
KALIMBA                 = 108
BAGPIPE                 = 109
FIDDLE                  = 110
SHANAI                  = 111

# ── Percussive (112–119) ─────────────────────────────────────────────────────

TINKLE_BELL             = 112
AGOGO                   = 113
STEEL_DRUMS             = 114
WOODBLOCK               = 115
TAIKO_DRUM              = 116
MELODIC_TOM             = 117
SYNTH_DRUM              = 118
REVERSE_CYMBAL          = 119

# ── Sound Effects (120–127) ──────────────────────────────────────────────────

GUITAR_FRET_NOISE       = 120
BREATH_NOISE            = 121
SEASHORE                = 122
BIRD_TWEET              = 123
TELEPHONE_RING          = 124
HELICOPTER              = 125
APPLAUSE                = 126
GUNSHOT                 = 127


# ── Human-readable instrument names ──────────────────────────────────────────
# Tuple of 128 instrument name strings indexed by program number.
# Names follow the official GM Level 1 specification.

GM_INSTRUMENT_NAMES: typing.Final[tuple[str, ...]] = (
	# Piano (0–7)
	"Acoustic Grand Piano", "Bright Acoustic Piano", "Electric Grand Piano",
	"Honky-tonk Piano", "Electric Piano 1", "Electric Piano 2",
	"Harpsichord", "Clavinet",

	# Chromatic Percussion (8–15)
	"Celesta", "Glockenspiel", "Music Box", "Vibraphone",
	"Marimba", "Xylophone", "Tubular Bells", "Dulcimer",

	# Organ (16–23)
	"Drawbar Organ", "Percussive Organ", "Rock Organ", "Church Organ",
	"Reed Organ", "Accordion", "Harmonica", "Tango Accordion",

	# Guitar (24–31)
	"Acoustic Guitar (nylon)", "Acoustic Guitar (steel)",
	"Electric Guitar (jazz)", "Electric Guitar (clean)",
	"Electric Guitar (muted)", "Overdriven Guitar",
	"Distortion Guitar", "Guitar Harmonics",

	# Bass (32–39)
	"Acoustic Bass", "Electric Bass (finger)", "Electric Bass (pick)",
	"Fretless Bass", "Slap Bass 1", "Slap Bass 2",
	"Synth Bass 1", "Synth Bass 2",

	# Strings (40–47)
	"Violin", "Viola", "Cello", "Contrabass",
	"Tremolo Strings", "Pizzicato Strings", "Orchestral Harp", "Timpani",

	# Ensemble (48–55)
	"String Ensemble 1", "String Ensemble 2", "Synth Strings 1",
	"Synth Strings 2", "Choir Aahs", "Voice Oohs",
	"Synth Voice", "Orchestra Hit",

	# Brass (56–63)
	"Trumpet", "Trombone", "Tuba", "Muted Trumpet",
	"French Horn", "Brass Section", "Synth Brass 1", "Synth Brass 2",

	# Reed (64–71)
	"Soprano Sax", "Alto Sax", "Tenor Sax", "Baritone Sax",
	"Oboe", "English Horn", "Bassoon", "Clarinet",

	# Pipe (72–79)
	"Piccolo", "Flute", "Recorder", "Pan Flute",
	"Blown Bottle", "Shakuhachi", "Whistle", "Ocarina",

	# Synth Lead (80–87)
	"Lead 1 (square)", "Lead 2 (sawtooth)", "Lead 3 (calliope)",
	"Lead 4 (chiff)", "Lead 5 (charang)", "Lead 6 (voice)",
	"Lead 7 (fifths)", "Lead 8 (bass + lead)",

	# Synth Pad (88–95)
	"Pad 1 (new age)", "Pad 2 (warm)", "Pad 3 (polysynth)",
	"Pad 4 (choir)", "Pad 5 (bowed)", "Pad 6 (metallic)",
	"Pad 7 (halo)", "Pad 8 (sweep)",

	# Synth Effects (96–103)
	"FX 1 (rain)", "FX 2 (soundtrack)", "FX 3 (crystal)",
	"FX 4 (atmosphere)", "FX 5 (brightness)", "FX 6 (goblins)",
	"FX 7 (echoes)", "FX 8 (sci-fi)",

	# Ethnic (104–111)
	"Sitar", "Banjo", "Shamisen", "Koto",
	"Kalimba", "Bagpipe", "Fiddle", "Shanai",

	# Percussive (112–119)
	"Tinkle Bell", "Agogo", "Steel Drums", "Woodblock",
	"Taiko Drum", "Melodic Tom", "Synth Drum", "Reverse Cymbal",

	# Sound Effects (120–127)
	"Guitar Fret Noise", "Breath Noise", "Seashore", "Bird Tweet",
	"Telephone Ring", "Helicopter", "Applause", "Gunshot",
)


# ── Lookup dictionary ────────────────────────────────────────────────────────
# Maps snake_case names to program numbers for string-based access.

GM_INSTRUMENT_MAP: typing.Final[dict[str, int]] = {
	# Piano
	"acoustic_grand_piano":     ACOUSTIC_GRAND_PIANO,
	"bright_acoustic_piano":    BRIGHT_ACOUSTIC_PIANO,
	"electric_grand_piano":     ELECTRIC_GRAND_PIANO,
	"honky_tonk_piano":         HONKY_TONK_PIANO,
	"electric_piano_1":         ELECTRIC_PIANO_1,
	"electric_piano_2":         ELECTRIC_PIANO_2,
	"harpsichord":              HARPSICHORD,
	"clavinet":                 CLAVINET,

	# Chromatic Percussion
	"celesta":                  CELESTA,
	"glockenspiel":             GLOCKENSPIEL,
	"music_box":                MUSIC_BOX,
	"vibraphone":               VIBRAPHONE,
	"marimba":                  MARIMBA,
	"xylophone":                XYLOPHONE,
	"tubular_bells":            TUBULAR_BELLS,
	"dulcimer":                 DULCIMER,

	# Organ
	"drawbar_organ":            DRAWBAR_ORGAN,
	"percussive_organ":         PERCUSSIVE_ORGAN,
	"rock_organ":               ROCK_ORGAN,
	"church_organ":             CHURCH_ORGAN,
	"reed_organ":               REED_ORGAN,
	"accordion":                ACCORDION,
	"harmonica":                HARMONICA,
	"tango_accordion":          TANGO_ACCORDION,

	# Guitar
	"acoustic_guitar_nylon":    ACOUSTIC_GUITAR_NYLON,
	"acoustic_guitar_steel":    ACOUSTIC_GUITAR_STEEL,
	"electric_guitar_jazz":     ELECTRIC_GUITAR_JAZZ,
	"electric_guitar_clean":    ELECTRIC_GUITAR_CLEAN,
	"electric_guitar_muted":    ELECTRIC_GUITAR_MUTED,
	"overdriven_guitar":        OVERDRIVEN_GUITAR,
	"distortion_guitar":        DISTORTION_GUITAR,
	"guitar_harmonics":         GUITAR_HARMONICS,

	# Bass
	"acoustic_bass":            ACOUSTIC_BASS,
	"electric_bass_finger":     ELECTRIC_BASS_FINGER,
	"electric_bass_pick":       ELECTRIC_BASS_PICK,
	"fretless_bass":            FRETLESS_BASS,
	"slap_bass_1":              SLAP_BASS_1,
	"slap_bass_2":              SLAP_BASS_2,
	"synth_bass_1":             SYNTH_BASS_1,
	"synth_bass_2":             SYNTH_BASS_2,

	# Strings
	"violin":                   VIOLIN,
	"viola":                    VIOLA,
	"cello":                    CELLO,
	"contrabass":               CONTRABASS,
	"tremolo_strings":          TREMOLO_STRINGS,
	"pizzicato_strings":        PIZZICATO_STRINGS,
	"orchestral_harp":          ORCHESTRAL_HARP,
	"timpani":                  TIMPANI,

	# Ensemble
	"string_ensemble_1":        STRING_ENSEMBLE_1,
	"string_ensemble_2":        STRING_ENSEMBLE_2,
	"synth_strings_1":          SYNTH_STRINGS_1,
	"synth_strings_2":          SYNTH_STRINGS_2,
	"choir_aahs":               CHOIR_AAHS,
	"voice_oohs":               VOICE_OOHS,
	"synth_voice":              SYNTH_VOICE,
	"orchestra_hit":            ORCHESTRA_HIT,

	# Brass
	"trumpet":                  TRUMPET,
	"trombone":                 TROMBONE,
	"tuba":                     TUBA,
	"muted_trumpet":            MUTED_TRUMPET,
	"french_horn":              FRENCH_HORN,
	"brass_section":            BRASS_SECTION,
	"synth_brass_1":            SYNTH_BRASS_1,
	"synth_brass_2":            SYNTH_BRASS_2,

	# Reed
	"soprano_sax":              SOPRANO_SAX,
	"alto_sax":                 ALTO_SAX,
	"tenor_sax":                TENOR_SAX,
	"baritone_sax":             BARITONE_SAX,
	"oboe":                     OBOE,
	"english_horn":             ENGLISH_HORN,
	"bassoon":                  BASSOON,
	"clarinet":                 CLARINET,

	# Pipe
	"piccolo":                  PICCOLO,
	"flute":                    FLUTE,
	"recorder":                 RECORDER,
	"pan_flute":                PAN_FLUTE,
	"blown_bottle":             BLOWN_BOTTLE,
	"shakuhachi":               SHAKUHACHI,
	"whistle":                  WHISTLE,
	"ocarina":                  OCARINA,

	# Synth Lead
	"lead_1_square":            LEAD_1_SQUARE,
	"lead_2_sawtooth":          LEAD_2_SAWTOOTH,
	"lead_3_calliope":          LEAD_3_CALLIOPE,
	"lead_4_chiff":             LEAD_4_CHIFF,
	"lead_5_charang":           LEAD_5_CHARANG,
	"lead_6_voice":             LEAD_6_VOICE,
	"lead_7_fifths":            LEAD_7_FIFTHS,
	"lead_8_bass_lead":         LEAD_8_BASS_LEAD,

	# Synth Pad
	"pad_1_new_age":            PAD_1_NEW_AGE,
	"pad_2_warm":               PAD_2_WARM,
	"pad_3_polysynth":          PAD_3_POLYSYNTH,
	"pad_4_choir":              PAD_4_CHOIR,
	"pad_5_bowed":              PAD_5_BOWED,
	"pad_6_metallic":           PAD_6_METALLIC,
	"pad_7_halo":               PAD_7_HALO,
	"pad_8_sweep":              PAD_8_SWEEP,

	# Synth Effects
	"fx_1_rain":                FX_1_RAIN,
	"fx_2_soundtrack":          FX_2_SOUNDTRACK,
	"fx_3_crystal":             FX_3_CRYSTAL,
	"fx_4_atmosphere":          FX_4_ATMOSPHERE,
	"fx_5_brightness":          FX_5_BRIGHTNESS,
	"fx_6_goblins":             FX_6_GOBLINS,
	"fx_7_echoes":              FX_7_ECHOES,
	"fx_8_sci_fi":              FX_8_SCI_FI,

	# Ethnic
	"sitar":                    SITAR,
	"banjo":                    BANJO,
	"shamisen":                 SHAMISEN,
	"koto":                     KOTO,
	"kalimba":                  KALIMBA,
	"bagpipe":                  BAGPIPE,
	"fiddle":                   FIDDLE,
	"shanai":                   SHANAI,

	# Percussive
	"tinkle_bell":              TINKLE_BELL,
	"agogo":                    AGOGO,
	"steel_drums":              STEEL_DRUMS,
	"woodblock":                WOODBLOCK,
	"taiko_drum":               TAIKO_DRUM,
	"melodic_tom":              MELODIC_TOM,
	"synth_drum":               SYNTH_DRUM,
	"reverse_cymbal":           REVERSE_CYMBAL,

	# Sound Effects
	"guitar_fret_noise":        GUITAR_FRET_NOISE,
	"breath_noise":             BREATH_NOISE,
	"seashore":                 SEASHORE,
	"bird_tweet":               BIRD_TWEET,
	"telephone_ring":           TELEPHONE_RING,
	"helicopter":               HELICOPTER,
	"applause":                 APPLAUSE,
	"gunshot":                  GUNSHOT,
}


# ── Instrument families ──────────────────────────────────────────────────────
# Maps family name to (first_program, last_program) inclusive range.
# Each family contains 8 instruments.

GM_FAMILIES: typing.Final[dict[str, tuple[int, int]]] = {
	"piano":                    (0, 7),
	"chromatic_percussion":     (8, 15),
	"organ":                    (16, 23),
	"guitar":                   (24, 31),
	"bass":                     (32, 39),
	"strings":                  (40, 47),
	"ensemble":                 (48, 55),
	"brass":                    (56, 63),
	"reed":                     (64, 71),
	"pipe":                     (72, 79),
	"synth_lead":               (80, 87),
	"synth_pad":                (88, 95),
	"synth_effects":            (96, 103),
	"ethnic":                   (104, 111),
	"percussive":               (112, 119),
	"sound_effects":            (120, 127),
}
