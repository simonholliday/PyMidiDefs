# PyMidiDefs

Comprehensive MIDI 1.0 and 2.0 constant definitions for Python.

A zero-dependency reference library providing named constants, lookup
dictionaries, and utility functions for the MIDI specification. Covers
note numbers, Control Change assignments, General MIDI instruments and
percussion, status bytes, Standard MIDI File meta-events, MIDI 2.0
Universal MIDI Packet (UMP) message types, and MIDI-CI capability inquiry
constants.

## Why PyMidiDefs?

If you're building a Python synthesiser, sequencer, DAW, MIDI controller
interface, music generator, or any application that sends or receives MIDI
messages, you need the same set of protocol constants: note numbers, CC
assignments, program change values, status bytes. These numbers are defined
by the MIDI specification and never change, yet most projects end up
re-defining them from scratch or copying them from unreliable sources.

PyMidiDefs gives you a single, authoritative package with every constant
sourced directly from the official MIDI specifications. It
has no runtime dependencies and works with any MIDI library or framework --
python-rtmidi, mido, pygame.midi, or your own socket-level implementation.

## About MIDI

MIDI (Musical Instrument Digital Interface) is a technical standard for
communication between electronic musical instruments, computers, and audio
devices. It was conceived in the early 1980s by Dave Smith of Sequential
Circuits and Ikutaro Kakehashi of Roland, who proposed a Universal
Synthesizer Interface to allow instruments from different manufacturers to
talk to each other. The MIDI 1.0 Detailed Specification was published in
August 1983 by the International MIDI Association (now the MIDI
Manufacturers Association, MMA) and has remained backwards-compatible ever
since.

General MIDI (GM), standardised in 1991, defined a common set of 128
instrument sounds and a percussion key map so that a MIDI file created on
one device would sound broadly similar on another. The Standard MIDI File
(SMF) format, also formalised in the early 1990s, became the universal way
to store and exchange MIDI sequences.

In January 2020, the MIDI Association announced MIDI 2.0 -- the first major
update to the protocol in nearly four decades. MIDI 2.0 introduces the
Universal MIDI Packet (UMP) format with higher-resolution velocity and
controller values, per-note controllers, and bidirectional communication via
MIDI-CI (Capability Inquiry) for automatic device configuration, profile
negotiation, and property exchange. MIDI 2.0 is a strict superset of MIDI
1.0; all existing MIDI 1.0 definitions remain valid.

## Installation

```bash
pip install git+https://github.com/simonholliday/PyMidiDefs.git
```

## Modules

| Module | Description |
|--------|-------------|
| `pymididefs.notes` | MIDI note numbers (C-1 to G9) and name/number conversion |
| `pymididefs.cc` | Control Change number assignments (0-127) |
| `pymididefs.drums` | General MIDI Level 1 percussion key map |
| `pymididefs.gm` | General MIDI Level 1 instrument program numbers and families |
| `pymididefs.status` | MIDI 1.0 status bytes (channel voice, system common, system real-time) |
| `pymididefs.meta` | Standard MIDI File meta-event type bytes |
| `pymididefs.ump` | MIDI 2.0 Universal MIDI Packet message types and constants |
| `pymididefs.ci` | MIDI 2.0 Capability Inquiry (MIDI-CI) constants |

## Usage

```python
import pymididefs.notes
import pymididefs.cc
import pymididefs.drums
import pymididefs.gm

# Note constants
pymididefs.notes.C4    # 60  (Middle C)
pymididefs.notes.A4    # 69  (Concert pitch)

# Note name conversion
pymididefs.notes.note_to_name(60)     # "C4"
pymididefs.notes.name_to_note("Db4")  # 61

# Control Change numbers
pymididefs.cc.SUSTAIN_PEDAL    # 64
pymididefs.cc.FILTER_CUTOFF    # 74
pymididefs.cc.CC_MAP["pan"]    # 10

# GM percussion
pymididefs.drums.KICK_1              # 36
pymididefs.drums.HI_HAT_CLOSED       # 42
pymididefs.drums.GM_DRUM_MAP["snare_1"]  # 38

# GM instruments
pymididefs.gm.ACOUSTIC_GRAND_PIANO   # 0
pymididefs.gm.VIOLIN                 # 40
pymididefs.gm.GM_INSTRUMENT_NAMES[40]    # "Violin"
pymididefs.gm.GM_INSTRUMENT_MAP["flute"]  # 73
```

### MIDI 2.0

```python
import pymididefs.ump
import pymididefs.ci

# Universal MIDI Packet message types
pymididefs.ump.MIDI2_CHANNEL_VOICE  # 0x4
pymididefs.ump.NOTE_ON              # 0x9
pymididefs.ump.PROTOCOL_MIDI2       # 0x02

# MIDI-CI
pymididefs.ci.DISCOVERY       # 0x70
pymididefs.ci.PROFILE_INQUIRY # 0x20
```

## Sources

All definitions are sourced from the official MIDI specifications published by
the [MIDI Association](https://midi.org/specs):

- [MIDI 1.0 Detailed Specification](https://midi.org/midi-1-0-detailed-specification) (MMA/AMEI)
- [General MIDI Level 1 Specification](https://midi.org/general-midi-level-1)
- [Standard MIDI File 1.0 Specification](https://midi.org/standard-midi-files)
- [M2-104-UM v1.1 — Universal MIDI Packet (UMP) Format and MIDI 2.0 Protocol Specification](https://midi.org/universal-midi-packet-ump-and-midi-2-0-protocol-specification)
- [M2-101-UM v1.2 — MIDI-CI Specification](https://midi.org/midi-ci-specification)

Some specifications require a free [MIDI Association membership](https://midi.org/membership)
to download.

## License

MIT
