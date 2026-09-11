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

PyMidiDefs gives you a single, authoritative package with every protocol
constant taken directly from the official MIDI specifications. It has no
runtime dependencies and works with any MIDI library or framework --
python-rtmidi, mido, pygame.midi, or your own socket-level implementation.

It holds only what the specifications define. What a *particular model* of
synth or drum machine answers to -- its controls, its note range, its voicing --
is a different kind of fact, read out of manufacturers' manuals rather than
transcribed from a standard, and it lives in
[PyMidiInstrumentDefs](https://github.com/simonholliday/PyMidiInstrumentDefs),
which builds on this package. Version 0.4.0 carried it here as
`pymididefs.instruments`.

## About MIDI

MIDI (Musical Instrument Digital Interface) is a technical standard for
communication between electronic musical instruments, computers, and audio
devices. It began in 1981, when Ikutaro Kakehashi of Roland proposed an
international standard for synthesizers to talk to each other, and Dave Smith
of Sequential Circuits outlined a Universal Synthesizer Interface, developed
with Chet Wood and presented to the Audio Engineering Society that autumn. The
MIDI 1.0 specification was published in August 1983,
with its copyright assigned to the International MIDI Association (IMA) --
one of three bodies, with the MIDI Manufacturers Association (MMA) and Japan's
JMSC, that formed independently to manage MIDI's development. It has remained
backwards-compatible ever since.

General MIDI (GM), standardised in 1991, defined a common set of 128
instrument sounds and a percussion key map so that a MIDI file created on
one device would sound broadly similar on another. The Standard MIDI File
(SMF) format, first published in 1988, became the universal way
to store and exchange MIDI sequences.

In January 2020, the MIDI Association and AMEI adopted the core specifications
of MIDI 2.0 -- the first major update to the protocol in nearly four decades --
and published them the following month. MIDI 2.0 introduces the Universal MIDI
Packet (UMP) format with higher-resolution velocity and controller values,
per-note controllers, and bidirectional communication via MIDI-CI (Capability
Inquiry) for automatic device configuration, profile negotiation, and property
exchange. It extends MIDI 1.0 rather than replacing it: MIDI 1.0 messages
remain valid, and the Universal MIDI Packet carries them too.

## Installation

```bash
pip install pymididefs
```

Requires Python 3.10 or later. There are no runtime dependencies.

To install the latest unreleased code straight from the repository:

```bash
pip install git+https://github.com/simonholliday/PyMidiDefs.git
```

## Modules

| Module | Description |
|--------|-------------|
| `pymididefs.notes` | MIDI note numbers (C-1 to G9) and name/number conversion |
| `pymididefs.cc` | Control Change number assignments (0-127), plus 14-bit pack/unpack helpers |
| `pymididefs.rpn` | Registered Parameter Numbers (RPN), including MPE and the 3D Sound Controllers, and the 14-bit parameter conventions shared with NRPN |
| `pymididefs.drums` | General MIDI percussion key map — GM Level 1 (notes 35-81) plus the extended GS/GM2 sounds |
| `pymididefs.gm` | General MIDI Level 1 instrument program numbers and families |
| `pymididefs.status` | MIDI 1.0 status bytes (channel voice, system common, system real-time) |
| `pymididefs.meta` | Standard MIDI File meta-event type bytes, including RP-019, RP-032 and the obsolete MIDI Port event |
| `pymididefs.ump` | MIDI 2.0 Universal MIDI Packet message types and constants, including Flex Data |
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
pymididefs.drums.KICK                # 36  (unnumbered "primary" alias of KICK_1)
pymididefs.drums.GM_DRUM_PRIMARY_ALIASES["crash"]  # 49

# GM instruments
pymididefs.gm.ACOUSTIC_GRAND_PIANO   # 0
pymididefs.gm.VIOLIN                 # 40
pymididefs.gm.GM_INSTRUMENT_NAMES[40]    # "Violin"
pymididefs.gm.GM_INSTRUMENT_MAP["flute"]  # 73
```

### RPN and 14-bit values

```python
import pymididefs.rpn
import pymididefs.cc

# Standard Registered Parameter Numbers
pymididefs.rpn.PITCH_BEND_SENSITIVITY  # 0
pymididefs.rpn.MODULATION_DEPTH_RANGE  # 5  (CA-026; required by GM2)
pymididefs.rpn.NULL_PARAMETER          # 16383  (sent as MSB=127, LSB=127)

# 14-bit pack/unpack — works for any MIDI 1.0 14-bit value
# (Bank Select, Data Entry, RPN/NRPN parameter numbers, pitch bend, ...)
pymididefs.cc.pack_14bit(8192)         # (64, 0)   pitch bend centre
pymididefs.cc.unpack_14bit(64, 0)      # 8192
```

### MIDI 2.0

```python
import pymididefs.ump
import pymididefs.ci

# Universal MIDI Packet message types
pymididefs.ump.MIDI2_CHANNEL_VOICE  # 0x4
pymididefs.ump.MIDI2_NOTE_ON        # 0x9   (a UMP opcode, not the 0x90 status byte)
pymididefs.ump.PROTOCOL_MIDI2       # 0x02

# MIDI-CI
pymididefs.ci.DISCOVERY       # 0x70
pymididefs.ci.PROFILE_INQUIRY # 0x20
```

## Sources

Every constant is transcribed from the specifications published by the
[MIDI Association](https://midi.org/specs) and AMEI, its Japanese counterpart:

- [MIDI 1.0 Detailed Specification](https://midi.org/midi-1-0-detailed-specification) (MMA/AMEI), with what later documents added to it: CA-026 (Modulation Depth Range), CA-031 (High Resolution Velocity Prefix), CA-034 and the MPE specification (the MPE Configuration Message), RP-021 and RP-023 (controller defaults), and RP-049 (3D Sound Controllers)
- [General MIDI Level 1 Specification](https://midi.org/general-midi-level-1) (RP-003)
- [General MIDI 2 Specification](https://midi.org/general-midi-2)
- [Standard MIDI File 1.0 Specification](https://midi.org/standard-midi-files) (RP-001), with RP-019 (Program Name, Device Name) and RP-032 (XMF Patch Type Prefix)
- [M2-104-UM v1.1.2 — Universal MIDI Packet (UMP) Format and MIDI 2.0 Protocol Specification](https://midi.org/universal-midi-packet-ump-and-midi-2-0-protocol-specification)
- [M2-101-UM v1.2 — MIDI-CI Specification](https://midi.org/midi-ci-specification). midi.org now serves v1.2.1, which is not publicly readable and has not been compared; the constants here were checked against v1.2

Some specifications require a free [MIDI Association membership](https://midi.org/membership)
to download.

A few things are not transcribed from those documents, and the modules that
hold them say so:

- **`pymididefs.meta.MIDI_PORT` (0x21) is in no specification.** It is an
  unofficial convention, now obsolete, and it is here because real files still
  carry it and a reader should be able to name what it meets.
- **The drum numbering `KICK_1`/`KICK_2` and `SNARE_1`/`SNARE_2` is Roland
  GS's.** General MIDI names those notes Acoustic Bass Drum, Bass Drum 1,
  Acoustic Snare and Electric Snare, and numbers only its crashes and rides as
  pairs. The unnumbered `KICK`, `SNARE`, `CRASH` and `RIDE` aliases are this
  package's own choice.
- **The octave names are a convention.** The specifications fix note 60 as
  middle C but name no octaves; this package calls it C4.

The values here, and the prose around them, were last checked against these
documents in September 2026.

## License

MIT -- you are free to use, copy, modify, merge, publish, distribute,
sublicense, and sell copies of this software in any project, including
commercial and closed-source applications. The only requirement is that you include the
LICENSE file when redistributing the software. See
[LICENSE](https://github.com/simonholliday/PyMidiDefs/blob/main/LICENSE)
for the full text.
