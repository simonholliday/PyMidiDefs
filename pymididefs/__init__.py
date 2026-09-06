"""PyMidiDefs — comprehensive MIDI 1.0 and 2.0 constant definitions for Python.

A zero-dependency reference library covering the MIDI 1.0 Detailed Specification,
General MIDI Level 1, Universal MIDI Packet (UMP) format, and MIDI-CI.

Those are specification facts: true for everybody, permanently. The library also
carries instrument definitions -- what a *particular model* of instrument does --
which are a different kind of claim and are read through an optional extra, so
that importing this package still pulls in nothing at all.

Modules
-------
notes   — MIDI note numbers and name/number conversion.
cc      — Control Change number assignments and 14-bit pack/unpack helpers.
rpn     — Standard Registered Parameter Numbers and the 14-bit parameter conventions shared with NRPN.
drums   — General MIDI percussion key map: GM Level 1, plus the extended GS/GM2 sounds.
gm      — General MIDI Level 1 instrument program numbers and families.
status  — MIDI 1.0 status bytes (channel voice, system common, system real-time).
meta    — Standard MIDI File meta-event type bytes, including the ones only real files carry.
ump     — MIDI 2.0 Universal MIDI Packet message types and constants.
ci      — MIDI 2.0 Capability Inquiry (MIDI-CI) constants.
instruments — what one model of instrument does; needs pymididefs[instruments].
"""

import importlib.metadata

import pymididefs.notes

# Version is derived from the latest git tag at build time via hatch-vcs;
# `importlib.metadata` then reads it from the installed package metadata.
# The fallback only fires if someone runs from a raw source checkout without
# installing the package (e.g. directly from a git clone with no `pip install`).
try:
	__version__ = importlib.metadata.version("pymididefs")
except importlib.metadata.PackageNotFoundError:
	__version__ = "0.0.0+unknown"

# Convenience re-exports for the most common operations.
note_to_name = pymididefs.notes.note_to_name
name_to_note = pymididefs.notes.name_to_note
