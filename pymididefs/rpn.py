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

Source: MIDI 1.0 Detailed Specification (RPN definitions) and General MIDI 2
Specification (adds Modulation Depth Range RPN).
"""

import typing


# ── Parameter number range ───────────────────────────────────────────────────
# Both RPN and NRPN parameter numbers are 14-bit (0–16383).

PARAMETER_MAX = 16383


# ── Standard Registered Parameter Numbers ────────────────────────────────────
# Stored as the 14-bit integer (MSB << 7 | LSB).  All standard RPNs use
# MSB = 0, so these values equal their LSB.

PITCH_BEND_SENSITIVITY  = 0   # (0, 0) — required by GM1
CHANNEL_FINE_TUNING     = 1   # (0, 1) — required by GM1
CHANNEL_COARSE_TUNING   = 2   # (0, 2) — required by GM1
TUNING_PROGRAM_SELECT   = 3   # (0, 3)
TUNING_BANK_SELECT      = 4   # (0, 4)
MODULATION_DEPTH_RANGE  = 5   # (0, 5) — added in GM2


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
	"null_parameter":           NULL_PARAMETER,
}
