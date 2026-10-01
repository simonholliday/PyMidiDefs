"""General MIDI percussion key map, with the common extended sounds.

Standard MIDI percussion assignments for channel 10 (0-indexed channel 9).

**Notes 35–81 are General MIDI Level 1**, and every GM Level 1 sound generator
is required to have them: GM1 asks for 'a minimum of 47 preset percussion
sounds conforming to the "GM Percussion Map"'.

**Notes 27–34 and 82–87 are not.** They are the fourteen extended sounds of
Roland's GS Standard Set, documented in 1991 and adopted by General MIDI 2 in
1999, and they bracket the GM Level 1 block on either side.  GS and GM2 devices
have them at these notes; a GM Level 1 device is not required to, and Yamaha's
XG puts most of them at other notes.  Check the target before using
``HIGH_Q``, ``CASTANETS`` or any of their neighbours.

Two ways to use this module::

	import pymididefs.drums

	# As named constants
	pymididefs.drums.KICK_1         # 36
	pymididefs.drums.HI_HAT_CLOSED  # 42

	# As a lookup dictionary
	pymididefs.drums.GM_DRUM_MAP["kick_1"]  # 36

Four sounds come in numbered pairs here — kick, snare, crash, ride — and each
also has an unnumbered *primary alias* pointing to its "1": the ``KICK`` /
``SNARE`` / ``CRASH`` / ``RIDE`` constants and the ``GM_DRUM_PRIMARY_ALIASES``
lookup, kept separate from ``GM_DRUM_MAP`` so the canonical key map stays one
name per note.

Sources: General MIDI System Level 1 (MMA RP-003), Table 3 — General MIDI
Percussion Map (35–81); General MIDI 2 and Roland's GS Standard Set (27–34 and
82–87).
Note range: 27 (High Q) through 87 (Open Surdo).
Channel: 10 (1-indexed) / 9 (0-indexed).
"""

import typing

# Everything this module defines, and nothing it imports.  A star-import
# brings the definitions only, and a name added to the module shows up here
# in the same diff, where a reader can see the public surface change.
__all__ = [
	"HIGH_Q", "SLAP", "SCRATCH_PUSH", "SCRATCH_PULL", "STICKS", "SQUARE_CLICK",
	"METRONOME_CLICK", "METRONOME_BELL", "KICK_2", "KICK_1", "SIDE_STICK",
	"SNARE_1", "HAND_CLAP", "SNARE_2", "LOW_FLOOR_TOM", "HI_HAT_CLOSED",
	"HIGH_FLOOR_TOM", "HI_HAT_PEDAL", "LOW_TOM", "HI_HAT_OPEN", "LOW_MID_TOM",
	"HIGH_MID_TOM", "CRASH_1", "HIGH_TOM", "RIDE_1", "CHINESE_CYMBAL",
	"RIDE_BELL", "TAMBOURINE", "SPLASH_CYMBAL", "COWBELL", "CRASH_2",
	"VIBRASLAP", "RIDE_2", "HIGH_BONGO", "LOW_BONGO", "MUTE_HIGH_CONGA",
	"OPEN_HIGH_CONGA", "LOW_CONGA", "HIGH_TIMBALE", "LOW_TIMBALE",
	"HIGH_AGOGO", "LOW_AGOGO", "CABASA", "MARACAS", "SHORT_WHISTLE",
	"LONG_WHISTLE", "SHORT_GUIRO", "LONG_GUIRO", "CLAVES", "HIGH_WOODBLOCK",
	"LOW_WOODBLOCK", "MUTE_CUICA", "OPEN_CUICA", "MUTE_TRIANGLE",
	"OPEN_TRIANGLE", "SHAKER", "JINGLE_BELL", "BELL_TREE", "CASTANETS",
	"MUTE_SURDO", "OPEN_SURDO", "GM_DRUM_MAP", "KICK", "SNARE", "CRASH",
	"RIDE", "GM_DRUM_PRIMARY_ALIASES", "GM_DRUM_NAMES", "GM2_DRUM_NAME_VARIANTS",
	"GM1_PERCUSSION_RANGE", "PERCUSSION_CHANNEL", "is_gm_level_1", "SOURCES",
]


# ── Percussion Key Map (notes 27–87) ─────────────────────────────────────────
# Organised by instrument family for readability.  Notes 35–81 are GM Level 1;
# the groups marked "extended" below are GS / GM2 and may be missing on a
# GM Level 1 device.

# Electronic percussion / effects (27–34) — extended, not GM Level 1
HIGH_Q              = 27  # High Q
SLAP                = 28  # Slap
SCRATCH_PUSH        = 29  # Scratch Push
SCRATCH_PULL        = 30  # Scratch Pull
STICKS              = 31  # Sticks
SQUARE_CLICK        = 32  # Square Click
METRONOME_CLICK     = 33  # Metronome Click
METRONOME_BELL      = 34  # Metronome Bell

# Kick drums (35–36)
KICK_2              = 35  # Acoustic Bass Drum
KICK_1              = 36  # Bass Drum 1

# Snare and side stick (37–40)
SIDE_STICK          = 37  # Side Stick
SNARE_1             = 38  # Acoustic Snare
HAND_CLAP           = 39  # Hand Clap
SNARE_2             = 40  # Electric Snare

# Toms (41, 43, 45, 47, 48, 50)
LOW_FLOOR_TOM       = 41  # Low Floor Tom
HI_HAT_CLOSED       = 42  # Closed Hi Hat
HIGH_FLOOR_TOM      = 43  # High Floor Tom
HI_HAT_PEDAL        = 44  # Pedal Hi-Hat
LOW_TOM             = 45  # Low Tom
HI_HAT_OPEN         = 46  # Open Hi-Hat
LOW_MID_TOM         = 47  # Low-Mid Tom
HIGH_MID_TOM        = 48  # Hi Mid Tom
CRASH_1             = 49  # Crash Cymbal 1
HIGH_TOM            = 50  # High Tom

# Cymbals (51–53, 55, 57, 59)
RIDE_1              = 51  # Ride Cymbal 1
CHINESE_CYMBAL      = 52  # Chinese Cymbal
RIDE_BELL           = 53  # Ride Bell
TAMBOURINE          = 54  # Tambourine
SPLASH_CYMBAL       = 55  # Splash Cymbal
COWBELL             = 56  # Cowbell
CRASH_2             = 57  # Crash Cymbal 2
VIBRASLAP           = 58  # Vibraslap
RIDE_2              = 59  # Ride Cymbal 2

# Latin percussion (60–69)
HIGH_BONGO          = 60  # Hi Bongo
LOW_BONGO           = 61  # Low Bongo
MUTE_HIGH_CONGA     = 62  # Mute Hi Conga
OPEN_HIGH_CONGA     = 63  # Open Hi Conga
LOW_CONGA           = 64  # Low Conga
HIGH_TIMBALE        = 65  # High Timbale
LOW_TIMBALE         = 66  # Low Timbale
HIGH_AGOGO          = 67  # High Agogo
LOW_AGOGO           = 68  # Low Agogo
CABASA              = 69  # Cabasa

# Shakers and small percussion (70–79)
MARACAS             = 70  # Maracas
SHORT_WHISTLE       = 71  # Short Whistle
LONG_WHISTLE        = 72  # Long Whistle
SHORT_GUIRO         = 73  # Short Guiro
LONG_GUIRO          = 74  # Long Guiro
CLAVES              = 75  # Claves
HIGH_WOODBLOCK      = 76  # Hi Wood Block
LOW_WOODBLOCK       = 77  # Low Wood Block
MUTE_CUICA          = 78  # Mute Cuica
OPEN_CUICA          = 79  # Open Cuica

# Triangle and bells (80–87) — 82–87 are extended, not GM Level 1
MUTE_TRIANGLE       = 80  # Mute Triangle
OPEN_TRIANGLE       = 81  # Open Triangle
SHAKER              = 82  # Shaker
JINGLE_BELL         = 83  # Jingle Bell
BELL_TREE           = 84  # Bell Tree
CASTANETS           = 85  # Castanets
MUTE_SURDO          = 86  # Mute Surdo
OPEN_SURDO          = 87  # Open Surdo


# ── Lookup dictionary ────────────────────────────────────────────────────────
# Maps snake_case names to MIDI note numbers for string-based access.

GM_DRUM_MAP: typing.Final[dict[str, int]] = {
	# Electronic percussion / effects
	"high_q":           HIGH_Q,
	"slap":             SLAP,
	"scratch_push":     SCRATCH_PUSH,
	"scratch_pull":     SCRATCH_PULL,
	"sticks":           STICKS,
	"square_click":     SQUARE_CLICK,
	"metronome_click":  METRONOME_CLICK,
	"metronome_bell":   METRONOME_BELL,

	# Kick drums
	"kick_2":           KICK_2,
	"kick_1":           KICK_1,

	# Snare and side stick
	"side_stick":       SIDE_STICK,
	"snare_1":          SNARE_1,
	"hand_clap":        HAND_CLAP,
	"snare_2":          SNARE_2,

	# Toms and hi-hats
	"low_floor_tom":    LOW_FLOOR_TOM,
	"hi_hat_closed":    HI_HAT_CLOSED,
	"high_floor_tom":   HIGH_FLOOR_TOM,
	"hi_hat_pedal":     HI_HAT_PEDAL,
	"low_tom":          LOW_TOM,
	"hi_hat_open":      HI_HAT_OPEN,
	"low_mid_tom":      LOW_MID_TOM,
	"high_mid_tom":     HIGH_MID_TOM,
	"high_tom":         HIGH_TOM,

	# Cymbals
	"crash_1":          CRASH_1,
	"ride_1":           RIDE_1,
	"chinese_cymbal":   CHINESE_CYMBAL,
	"ride_bell":        RIDE_BELL,
	"tambourine":       TAMBOURINE,
	"splash_cymbal":    SPLASH_CYMBAL,
	"cowbell":          COWBELL,
	"crash_2":          CRASH_2,
	"vibraslap":        VIBRASLAP,
	"ride_2":           RIDE_2,

	# Latin percussion
	"high_bongo":       HIGH_BONGO,
	"low_bongo":        LOW_BONGO,
	"mute_high_conga":  MUTE_HIGH_CONGA,
	"open_high_conga":  OPEN_HIGH_CONGA,
	"low_conga":        LOW_CONGA,
	"high_timbale":     HIGH_TIMBALE,
	"low_timbale":      LOW_TIMBALE,
	"high_agogo":       HIGH_AGOGO,
	"low_agogo":        LOW_AGOGO,
	"cabasa":           CABASA,

	# Shakers and small percussion
	"maracas":          MARACAS,
	"short_whistle":    SHORT_WHISTLE,
	"long_whistle":     LONG_WHISTLE,
	"short_guiro":      SHORT_GUIRO,
	"long_guiro":       LONG_GUIRO,
	"claves":           CLAVES,
	"high_woodblock":   HIGH_WOODBLOCK,
	"low_woodblock":    LOW_WOODBLOCK,
	"mute_cuica":       MUTE_CUICA,
	"open_cuica":       OPEN_CUICA,

	# Triangle and bells
	"mute_triangle":    MUTE_TRIANGLE,
	"open_triangle":    OPEN_TRIANGLE,
	"shaker":           SHAKER,
	"jingle_bell":      JINGLE_BELL,
	"bell_tree":        BELL_TREE,
	"castanets":        CASTANETS,
	"mute_surdo":       MUTE_SURDO,
	"open_surdo":       OPEN_SURDO,
}


# ── Primary aliases ──────────────────────────────────────────────────────────
# General MIDI numbers two of these pairs itself: Crash Cymbal 1 and 2 (49, 57)
# and Ride Cymbal 1 and 2 (51, 59).  It does not number the kicks or snares as
# pairs — it calls them Acoustic Bass Drum and Bass Drum 1 (35, 36), and
# Acoustic Snare and Electric Snare (38, 40).  The KICK_1/KICK_2 and
# SNARE_1/SNARE_2 numbering is Roland GS's, whose Standard Set calls them Kick
# Drum 2 and Kick Drum 1, and Snare Drum 1 and Snare Drum 2.
#
# No specification designates a primary.  These unnumbered aliases point at
# the "1" of each pair — Bass Drum 1, Acoustic Snare, Crash Cymbal 1, Ride
# Cymbal 1 — by this package's choice, so ``KICK`` can mean "the kick" without
# choosing between the two.
#
# Kept separate from GM_DRUM_MAP, which stays one name per note (the canonical
# percussion key map).  Only these four sounds come in numbered pairs; the
# single-instance voices (closed/open/pedal hi-hat, side stick, cowbell, …) are
# already unnumbered.  Ambiguous cases with no clear primary (e.g. the six toms)
# are deliberately not aliased.

KICK  = KICK_1   # Bass Drum 1 (36)
SNARE = SNARE_1  # Acoustic Snare (38)
CRASH = CRASH_1  # Crash Cymbal 1 (49)
RIDE  = RIDE_1   # Ride Cymbal 1 (51)

GM_DRUM_PRIMARY_ALIASES: typing.Final[dict[str, int]] = {
	"kick":  KICK_1,
	"snare": SNARE_1,
	"crash": CRASH_1,
	"ride":  RIDE_1,
}


# ── The sounds as their specifications name them ─────────────────────────────
# The constants above each carry a name in a trailing comment, which no program
# can read.  These are the same names as data, so a reader can be shown
# "Acoustic Bass Drum" instead of 35.
#
# Each is the name printed by the document that defines that note: General MIDI
# Level 1 (RP-003, Table 3) for 35–81, and General MIDI 2 (RP-024, Appendix B,
# STANDARD Set) for the extended sounds either side of them.  GM2 marks
# mutually exclusive sounds "[EXC1]" and so on; that says how a sound behaves
# rather than what it is called, and it is not reproduced here.
#
# The spellings are the documents' own, inconsistencies included: "Closed Hi
# Hat" beside "Pedal Hi-Hat" is how RP-003 prints them, and "Hi Bongo" beside
# "High Timbale" likewise.

GM_DRUM_NAMES: typing.Final[dict[int, str]] = {
	# Electronic percussion / effects — General MIDI 2
	HIGH_Q:           "High Q",
	SLAP:             "Slap",
	SCRATCH_PUSH:     "Scratch Push",
	SCRATCH_PULL:     "Scratch Pull",
	STICKS:           "Sticks",
	SQUARE_CLICK:     "Square Click",
	METRONOME_CLICK:  "Metronome Click",
	METRONOME_BELL:   "Metronome Bell",

	# General MIDI Level 1 — RP-003, Table 3
	KICK_2:           "Acoustic Bass Drum",
	KICK_1:           "Bass Drum 1",
	SIDE_STICK:       "Side Stick",
	SNARE_1:          "Acoustic Snare",
	HAND_CLAP:        "Hand Clap",
	SNARE_2:          "Electric Snare",
	LOW_FLOOR_TOM:    "Low Floor Tom",
	HI_HAT_CLOSED:    "Closed Hi Hat",
	HIGH_FLOOR_TOM:   "High Floor Tom",
	HI_HAT_PEDAL:     "Pedal Hi-Hat",
	LOW_TOM:          "Low Tom",
	HI_HAT_OPEN:      "Open Hi-Hat",
	LOW_MID_TOM:      "Low-Mid Tom",
	HIGH_MID_TOM:     "Hi Mid Tom",
	CRASH_1:          "Crash Cymbal 1",
	HIGH_TOM:         "High Tom",
	RIDE_1:           "Ride Cymbal 1",
	CHINESE_CYMBAL:   "Chinese Cymbal",
	RIDE_BELL:        "Ride Bell",
	TAMBOURINE:       "Tambourine",
	SPLASH_CYMBAL:    "Splash Cymbal",
	COWBELL:          "Cowbell",
	CRASH_2:          "Crash Cymbal 2",
	VIBRASLAP:        "Vibraslap",
	RIDE_2:           "Ride Cymbal 2",
	HIGH_BONGO:       "Hi Bongo",
	LOW_BONGO:        "Low Bongo",
	MUTE_HIGH_CONGA:  "Mute Hi Conga",
	OPEN_HIGH_CONGA:  "Open Hi Conga",
	LOW_CONGA:        "Low Conga",
	HIGH_TIMBALE:     "High Timbale",
	LOW_TIMBALE:      "Low Timbale",
	HIGH_AGOGO:       "High Agogo",
	LOW_AGOGO:        "Low Agogo",
	CABASA:           "Cabasa",
	MARACAS:          "Maracas",
	SHORT_WHISTLE:    "Short Whistle",
	LONG_WHISTLE:     "Long Whistle",
	SHORT_GUIRO:      "Short Guiro",
	LONG_GUIRO:       "Long Guiro",
	CLAVES:           "Claves",
	HIGH_WOODBLOCK:   "Hi Wood Block",
	LOW_WOODBLOCK:    "Low Wood Block",
	MUTE_CUICA:       "Mute Cuica",
	OPEN_CUICA:       "Open Cuica",
	MUTE_TRIANGLE:    "Mute Triangle",
	OPEN_TRIANGLE:    "Open Triangle",

	# Triangle and bells above the Level 1 block — General MIDI 2
	SHAKER:           "Shaker",
	JINGLE_BELL:      "Jingle Bell",
	BELL_TREE:        "Bell Tree",
	CASTANETS:        "Castanets",
	MUTE_SURDO:       "Mute Surdo",
	OPEN_SURDO:       "Open Surdo",
}


# ── Where General MIDI 2 spells a Level 1 sound differently ──────────────────
# GM2 reprints the Level 1 map in its own Appendix B and regularises six of the
# names, tidying away the inconsistencies RP-003 left.  Somebody reading a GM2
# device's documentation meets these spellings instead, so both are worth
# having; ``GM_DRUM_NAMES`` keeps RP-003's, because RP-003 defines those notes.
#
# Only the six that differ are here.  For every other note in 35–81 the two
# documents agree, and for 27–34 and 82–87 only GM2 names the sound at all.

GM2_DRUM_NAME_VARIANTS: typing.Final[dict[int, str]] = {
	HI_HAT_CLOSED:  "Closed Hi-hat",
	HI_HAT_PEDAL:   "Pedal Hi-hat",
	HI_HAT_OPEN:    "Open Hi-hat",
	HIGH_MID_TOM:   "High Mid Tom",
	VIBRASLAP:      "Vibra-slap",
	HIGH_BONGO:     "High Bongo",
}


# ── What General MIDI Level 1 requires, and where ─────────────────────────────
# RP-003 asks a Level 1 sound generator for "a minimum of 47 preset percussion
# sounds conforming to the 'GM Percussion Map'", which is notes 35 to 81
# inclusive.  Everything outside that range in this module is a GS and GM2
# extension that a Level 1 device need not have.

GM1_PERCUSSION_RANGE: typing.Final[tuple[int, int]] = (35, 81)

# "Key-based Percussion is always on channel 10" (RP-003), counting channels
# from 1 as the specifications do.  The nibble in a status byte is one less.
PERCUSSION_CHANNEL = 10


def is_gm_level_1 (note: int) -> bool:

	"""Is this note one a General MIDI Level 1 sound generator must have?

	True for 35–81, the GM Percussion Map proper.  False for the GS and GM2
	extensions this module also carries, and false for any note outside the map
	entirely — a Level 1 device is not required to make a sound there either.

	>>> is_gm_level_1(36)    # Bass Drum 1
	True
	>>> is_gm_level_1(27)    # High Q, a GS/GM2 extension
	False
	"""

	lowest, highest = GM1_PERCUSSION_RANGE

	return lowest <= note <= highest


# ── Where these facts come from ──────────────────────────────────────────────
# Each entry is a document and the page that serves it, so a reader can be shown
# the source of what they are reading.  The URL is empty where there is no
# public page.

SOURCES: typing.Final[tuple[tuple[str, str], ...]] = (
	("General MIDI System Level 1 (MMA RP-003), Table 3 — General MIDI Percussion Map",
	 "https://midi.org/general-midi-level-1"),
	("General MIDI 2 (MMA RP-024), Appendix B — GM2 Percussion Sound Set, STANDARD Set",
	 "https://midi.org/general-midi-2"),
)
