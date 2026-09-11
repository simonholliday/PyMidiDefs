"""Standard MIDI RPN (Registered Parameter Number) constants.

RPN and NRPN are conventions layered on regular Control Change messages: the
parameter number is selected via CC 101/100 (RPN) or CC 99/98 (NRPN), the
value is sent via Data Entry MSB/LSB (CC 6/38), and the selection is cleared
with the NULL parameter (127, 127).  See ``pymididefs.cc`` for the controller
numbers and ``pymididefs.cc.pack_14bit`` / ``unpack_14bit`` for the 7+7-bit
encoding used by parameter numbers and data values.

Two ways to use this module::

	import pymididefs.rpn

	pymididefs.rpn.PITCH_BEND_SENSITIVITY          # 0
	pymididefs.rpn.RPN_MAP["channel_fine_tuning"]  # 1

The MIDI 2.0 successor to RPN/NRPN is the Registered Controller / Assignable
Controller message type — see ``pymididefs.ump.REGISTERED_CC`` and
``ASSIGNABLE_CC``.

Sources: MIDI 1.0 Detailed Specification (RPN definitions); MMA CA-026, which
defines Modulation Depth Range, and General MIDI 2, which requires it; CA-034
and the MPE specification (the MPE Configuration Message); RP-049 (the 3D
Sound Controllers).  midi.org's public Control Change page carries the whole
registered parameter table.
"""

import typing


# ── Parameter number range ───────────────────────────────────────────────────
# Both RPN and NRPN parameter numbers are 14-bit (0–16383).

PARAMETER_MAX = 16383


# ── Registered Parameter Numbers under MSB 0 ─────────────────────────────────
# Stored as the 14-bit integer (MSB << 7 | LSB).  These all have MSB 0, so each
# equals its LSB.

PITCH_BEND_SENSITIVITY  = 0   # (0, 0) — required by GM1
CHANNEL_FINE_TUNING     = 1   # (0, 1) — required by GM1
CHANNEL_COARSE_TUNING   = 2   # (0, 2) — required by GM1
TUNING_PROGRAM_SELECT   = 3   # (0, 3)
TUNING_BANK_SELECT      = 4   # (0, 4)
MODULATION_DEPTH_RANGE  = 5   # (0, 5) — CA-026; required by GM2
MPE_CONFIGURATION       = 6   # (0, 6) — MPE Configuration Message, CA-034


# ── Three Dimensional Sound Controllers, under MSB 0x3D (RP-049) ─────────────
# Stored the same way, so each is 0x3D << 7 | LSB, from 7808 to 7816.

SOUND_3D_AZIMUTH_ANGLE              = 7808  # (0x3D, 0x00) — Azimuth Angle
SOUND_3D_ELEVATION_ANGLE            = 7809  # (0x3D, 0x01) — Elevation Angle
SOUND_3D_GAIN                       = 7810  # (0x3D, 0x02) — Gain
SOUND_3D_DISTANCE_RATIO             = 7811  # (0x3D, 0x03) — Distance Ratio
SOUND_3D_MAXIMUM_DISTANCE           = 7812  # (0x3D, 0x04) — Maximum Distance
SOUND_3D_GAIN_AT_MAXIMUM_DISTANCE   = 7813  # (0x3D, 0x05) — Gain at Maximum Distance
SOUND_3D_REFERENCE_DISTANCE_RATIO   = 7814  # (0x3D, 0x06) — Reference Distance Ratio
SOUND_3D_PAN_SPREAD_ANGLE           = 7815  # (0x3D, 0x07) — Pan Spread Angle
SOUND_3D_ROLL_ANGLE                 = 7816  # (0x3D, 0x08) — Roll Angle


# ── NULL parameter ───────────────────────────────────────────────────────────
# Sent as MSB = 127, LSB = 127 to deselect the currently active RPN/NRPN.
# Defensive practice: send NULL after a Data Entry sequence so a stray CC 6/38
# is not misinterpreted as a value for the previously selected parameter.

NULL_PARAMETER = 16383


# ── snake_case lookup ────────────────────────────────────────────────────────

RPN_MAP: typing.Final[dict[str, int]] = {
	"pitch_bend_sensitivity":   PITCH_BEND_SENSITIVITY,
	"channel_fine_tuning":      CHANNEL_FINE_TUNING,
	"channel_coarse_tuning":    CHANNEL_COARSE_TUNING,
	"tuning_program_select":    TUNING_PROGRAM_SELECT,
	"tuning_bank_select":       TUNING_BANK_SELECT,
	"modulation_depth_range":   MODULATION_DEPTH_RANGE,
	"mpe_configuration":        MPE_CONFIGURATION,

	"sound_3d_azimuth_angle":               SOUND_3D_AZIMUTH_ANGLE,
	"sound_3d_elevation_angle":             SOUND_3D_ELEVATION_ANGLE,
	"sound_3d_gain":                        SOUND_3D_GAIN,
	"sound_3d_distance_ratio":              SOUND_3D_DISTANCE_RATIO,
	"sound_3d_maximum_distance":            SOUND_3D_MAXIMUM_DISTANCE,
	"sound_3d_gain_at_maximum_distance":    SOUND_3D_GAIN_AT_MAXIMUM_DISTANCE,
	"sound_3d_reference_distance_ratio":    SOUND_3D_REFERENCE_DISTANCE_RATIO,
	"sound_3d_pan_spread_angle":            SOUND_3D_PAN_SPREAD_ANGLE,
	"sound_3d_roll_angle":                  SOUND_3D_ROLL_ANGLE,

	"null_parameter":           NULL_PARAMETER,
}
