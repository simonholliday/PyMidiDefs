"""MIDI Control Change (CC) number assignments.

The MIDI specification defines 128 controller numbers (0–127).  This module
provides named constants for all controllers that have a defined function in
the MIDI 1.0 Detailed Specification.  Undefined/reserved numbers (3, 9, 14–15,
20–31, 85–90, 102–119) are omitted — they are available for general-purpose
use and do not have standard names.

Two ways to use this module::

	import pymididefs.cc

	# As named constants
	pymididefs.cc.SUSTAIN_PEDAL       # 64

	# As a lookup dictionary
	pymididefs.cc.CC_MAP["sustain_pedal"]  # 64

Source: MIDI 1.0 Detailed Specification, Table III — Control Change Messages.
"""

import typing


# ── MSB Controllers (0–31) ───────────────────────────────────────────────────
# High-resolution continuous controllers — most significant byte.
# Controllers 0–31 each have a corresponding LSB at CC 32–63.

BANK_SELECT_MSB     = 0   # Bank Select
MODULATION_WHEEL    = 1   # Modulation Wheel or Lever
BREATH_CONTROLLER   = 2   # Breath Controller
# CC 3: Undefined
FOOT_CONTROLLER     = 4   # Foot Controller
PORTAMENTO_TIME     = 5   # Portamento Time
DATA_ENTRY_MSB      = 6   # Data Entry MSB
VOLUME              = 7   # Channel Volume (formerly Main Volume)
BALANCE             = 8   # Balance
# CC 9: Undefined
PAN                 = 10  # Pan
EXPRESSION          = 11  # Expression Controller
EFFECT_CONTROL_1    = 12  # Effect Control 1
EFFECT_CONTROL_2    = 13  # Effect Control 2
# CC 14–15: Undefined
GENERAL_PURPOSE_1   = 16  # General Purpose Controller 1
GENERAL_PURPOSE_2   = 17  # General Purpose Controller 2
GENERAL_PURPOSE_3   = 18  # General Purpose Controller 3
GENERAL_PURPOSE_4   = 19  # General Purpose Controller 4
# CC 20–31: Undefined


# ── LSB Controllers (32–63) ──────────────────────────────────────────────────
# Low-resolution counterparts for CC 0–31.
# Only the most commonly referenced LSB values are named here.

BANK_SELECT_LSB         = 32  # Bank Select LSB
MODULATION_WHEEL_LSB    = 33  # Modulation Wheel LSB
BREATH_CONTROLLER_LSB   = 34  # Breath Controller LSB
# CC 35: Undefined LSB
FOOT_CONTROLLER_LSB     = 36  # Foot Controller LSB
PORTAMENTO_TIME_LSB     = 37  # Portamento Time LSB
DATA_ENTRY_LSB          = 38  # Data Entry LSB
VOLUME_LSB              = 39  # Channel Volume LSB
BALANCE_LSB             = 40  # Balance LSB
# CC 41: Undefined LSB
PAN_LSB                 = 42  # Pan LSB
EXPRESSION_LSB          = 43  # Expression LSB
EFFECT_CONTROL_1_LSB    = 44  # Effect Control 1 LSB
EFFECT_CONTROL_2_LSB    = 45  # Effect Control 2 LSB


# ── Switch Controllers (64–69) ───────────────────────────────────────────────
# On/off pedals and switches.  Values 0–63 = Off, 64–127 = On.

SUSTAIN_PEDAL       = 64  # Damper Pedal (Sustain)
PORTAMENTO_ON_OFF   = 65  # Portamento On/Off
SOSTENUTO_PEDAL     = 66  # Sostenuto
SOFT_PEDAL          = 67  # Soft Pedal
LEGATO_PEDAL        = 68  # Legato Footswitch
HOLD_2              = 69  # Hold 2


# ── Sound Controllers (70–79) ────────────────────────────────────────────────
# Defined by General MIDI Level 2 for real-time timbre adjustment.

SOUND_VARIATION     = 70  # Sound Controller 1  (default: Sound Variation)
FILTER_RESONANCE    = 71  # Sound Controller 2  (default: Timbre / Filter Resonance)
RELEASE_TIME        = 72  # Sound Controller 3  (default: Release Time)
ATTACK_TIME         = 73  # Sound Controller 4  (default: Attack Time)
FILTER_CUTOFF       = 74  # Sound Controller 5  (default: Brightness / Filter Cutoff)
SOUND_CONTROL_6     = 75  # Sound Controller 6  (default: Decay Time — GM2)
SOUND_CONTROL_7     = 76  # Sound Controller 7  (default: Vibrato Rate — GM2)
SOUND_CONTROL_8     = 77  # Sound Controller 8  (default: Vibrato Depth — GM2)
SOUND_CONTROL_9     = 78  # Sound Controller 9  (default: Vibrato Delay — GM2)
SOUND_CONTROL_10    = 79  # Sound Controller 10 (default: undefined)


# ── General Purpose Controllers (80–83) ──────────────────────────────────────

GENERAL_PURPOSE_5   = 80  # General Purpose Controller 5
GENERAL_PURPOSE_6   = 81  # General Purpose Controller 6
GENERAL_PURPOSE_7   = 82  # General Purpose Controller 7
GENERAL_PURPOSE_8   = 83  # General Purpose Controller 8


# ── Effects Send Levels (91–95) ──────────────────────────────────────────────
# CC 84 is Portamento Control; CC 85–90 are undefined.

PORTAMENTO_CONTROL  = 84  # Portamento Control (source note for portamento)
# CC 85–90: Undefined
REVERB_DEPTH        = 91  # Effects 1 Depth (default: Reverb Send Level)
TREMOLO_DEPTH       = 92  # Effects 2 Depth (default: Tremolo Depth)
CHORUS_DEPTH        = 93  # Effects 3 Depth (default: Chorus Send Level)
CELESTE_DEPTH       = 94  # Effects 4 Depth (default: Celeste / Detune Depth)
PHASER_DEPTH        = 95  # Effects 5 Depth (default: Phaser Depth)


# ── Parameter Control (96–101) ───────────────────────────────────────────────
# Used for RPN / NRPN parameter addressing and data manipulation.

DATA_INCREMENT      = 96   # Data Increment (Data Entry +1)
DATA_DECREMENT      = 97   # Data Decrement (Data Entry -1)
NRPN_LSB            = 98   # Non-Registered Parameter Number LSB
NRPN_MSB            = 99   # Non-Registered Parameter Number MSB
RPN_LSB             = 100  # Registered Parameter Number LSB
RPN_MSB             = 101  # Registered Parameter Number MSB

# CC 102–119: Undefined


# ── Channel Mode Messages (120–127) ─────────────────────────────────────────
# These use the Control Change status byte but function as channel mode
# commands rather than continuous controllers.

ALL_SOUND_OFF           = 120  # All Sound Off (value = 0)
RESET_ALL_CONTROLLERS   = 121  # Reset All Controllers (value = 0)
LOCAL_CONTROL_ON_OFF    = 122  # Local Control On/Off (0 = Off, 127 = On)
ALL_NOTES_OFF           = 123  # All Notes Off (value = 0)
OMNI_MODE_OFF           = 124  # Omni Mode Off (+ All Notes Off)
OMNI_MODE_ON            = 125  # Omni Mode On (+ All Notes Off)
MONO_MODE_ON            = 126  # Mono Mode On (+ All Notes Off)
POLY_MODE_ON            = 127  # Poly Mode On (+ All Notes Off)


# ── Lookup dictionary ────────────────────────────────────────────────────────
# Maps snake_case names to CC numbers for string-based access.

CC_MAP: typing.Final[dict[str, int]] = {
	# MSB controllers
	"bank_select_msb":      BANK_SELECT_MSB,
	"modulation_wheel":     MODULATION_WHEEL,
	"breath_controller":    BREATH_CONTROLLER,
	"foot_controller":      FOOT_CONTROLLER,
	"portamento_time":      PORTAMENTO_TIME,
	"data_entry_msb":       DATA_ENTRY_MSB,
	"volume":               VOLUME,
	"balance":              BALANCE,
	"pan":                  PAN,
	"expression":           EXPRESSION,
	"effect_control_1":     EFFECT_CONTROL_1,
	"effect_control_2":     EFFECT_CONTROL_2,
	"general_purpose_1":    GENERAL_PURPOSE_1,
	"general_purpose_2":    GENERAL_PURPOSE_2,
	"general_purpose_3":    GENERAL_PURPOSE_3,
	"general_purpose_4":    GENERAL_PURPOSE_4,

	# LSB controllers
	"bank_select_lsb":          BANK_SELECT_LSB,
	"modulation_wheel_lsb":     MODULATION_WHEEL_LSB,
	"breath_controller_lsb":    BREATH_CONTROLLER_LSB,
	"foot_controller_lsb":      FOOT_CONTROLLER_LSB,
	"portamento_time_lsb":      PORTAMENTO_TIME_LSB,
	"data_entry_lsb":           DATA_ENTRY_LSB,
	"volume_lsb":               VOLUME_LSB,
	"balance_lsb":              BALANCE_LSB,
	"pan_lsb":                  PAN_LSB,
	"expression_lsb":           EXPRESSION_LSB,
	"effect_control_1_lsb":     EFFECT_CONTROL_1_LSB,
	"effect_control_2_lsb":     EFFECT_CONTROL_2_LSB,

	# Switch controllers
	"sustain_pedal":        SUSTAIN_PEDAL,
	"portamento_on_off":    PORTAMENTO_ON_OFF,
	"sostenuto_pedal":      SOSTENUTO_PEDAL,
	"soft_pedal":           SOFT_PEDAL,
	"legato_pedal":         LEGATO_PEDAL,
	"hold_2":               HOLD_2,

	# Sound controllers
	"sound_variation":      SOUND_VARIATION,
	"filter_resonance":     FILTER_RESONANCE,
	"release_time":         RELEASE_TIME,
	"attack_time":          ATTACK_TIME,
	"filter_cutoff":        FILTER_CUTOFF,
	"sound_control_6":      SOUND_CONTROL_6,
	"sound_control_7":      SOUND_CONTROL_7,
	"sound_control_8":      SOUND_CONTROL_8,
	"sound_control_9":      SOUND_CONTROL_9,
	"sound_control_10":     SOUND_CONTROL_10,

	# General purpose controllers
	"general_purpose_5":    GENERAL_PURPOSE_5,
	"general_purpose_6":    GENERAL_PURPOSE_6,
	"general_purpose_7":    GENERAL_PURPOSE_7,
	"general_purpose_8":    GENERAL_PURPOSE_8,

	# Effects send levels
	"portamento_control":   PORTAMENTO_CONTROL,
	"reverb_depth":         REVERB_DEPTH,
	"tremolo_depth":        TREMOLO_DEPTH,
	"chorus_depth":         CHORUS_DEPTH,
	"celeste_depth":        CELESTE_DEPTH,
	"phaser_depth":         PHASER_DEPTH,

	# Parameter control
	"data_increment":       DATA_INCREMENT,
	"data_decrement":       DATA_DECREMENT,
	"nrpn_lsb":             NRPN_LSB,
	"nrpn_msb":             NRPN_MSB,
	"rpn_lsb":              RPN_LSB,
	"rpn_msb":              RPN_MSB,

	# Channel mode messages
	"all_sound_off":            ALL_SOUND_OFF,
	"reset_all_controllers":    RESET_ALL_CONTROLLERS,
	"local_control_on_off":     LOCAL_CONTROL_ON_OFF,
	"all_notes_off":            ALL_NOTES_OFF,
	"omni_mode_off":            OMNI_MODE_OFF,
	"omni_mode_on":             OMNI_MODE_ON,
	"mono_mode_on":             MONO_MODE_ON,
	"poly_mode_on":             POLY_MODE_ON,
}
