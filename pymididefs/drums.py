"""General MIDI Level 1 percussion key map.

Standard MIDI percussion assignments for channel 10 (0-indexed channel 9).
These note numbers are defined by the General MIDI Level 1 specification and
are supported by virtually all GM-compatible instruments, drum machines, and
DAWs.

Two ways to use this module::

	import pymididefs.drums

	# As named constants
	pymididefs.drums.KICK_1         # 36
	pymididefs.drums.HI_HAT_CLOSED  # 42

	# As a lookup dictionary
	pymididefs.drums.GM_DRUM_MAP["kick_1"]  # 36

Source: General MIDI Level 1 Specification — Percussion Key Map.
Note range: 27 (High Q) through 87 (Open Surdo).
Channel: 10 (1-indexed) / 9 (0-indexed).
"""

import typing


# ── GM Level 1 Percussion Key Map (notes 27–87) ─────────────────────────────
# Organised by instrument family for readability.

# Electronic percussion / effects (27–34)
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
HI_HAT_CLOSED       = 42  # Closed Hi-Hat
HIGH_FLOOR_TOM      = 43  # High Floor Tom
HI_HAT_PEDAL        = 44  # Pedal Hi-Hat
LOW_TOM             = 45  # Low Tom
HI_HAT_OPEN         = 46  # Open Hi-Hat
LOW_MID_TOM         = 47  # Low-Mid Tom
HIGH_MID_TOM        = 48  # Hi-Mid Tom
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

# Triangle and bells (80–87)
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
