"""PyMidiDefs — comprehensive MIDI 1.0 and 2.0 constant definitions for Python.

A zero-dependency reference library covering the MIDI 1.0 Detailed Specification,
General MIDI Level 1, Universal MIDI Packet (UMP) format, and MIDI-CI.

Modules
-------
notes   — MIDI note numbers and name/number conversion.
cc      — Control Change number assignments and 14-bit pack/unpack helpers.
rpn     — Standard Registered Parameter Numbers and the 14-bit parameter conventions shared with NRPN.
drums   — General MIDI Level 1 percussion key map.
gm      — General MIDI Level 1 instrument program numbers and families.
status  — MIDI 1.0 status bytes (channel voice, system common, system real-time).
meta    — Standard MIDI File meta-event type bytes.
ump     — MIDI 2.0 Universal MIDI Packet message types and constants.
ci      — MIDI 2.0 Capability Inquiry (MIDI-CI) constants.
"""

import pymididefs.notes

__version__ = "0.2.0"

# Convenience re-exports for the most common operations.
note_to_name = pymididefs.notes.note_to_name
name_to_note = pymididefs.notes.name_to_note
