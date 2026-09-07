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

PyMidiDefs gives you a single package with every protocol constant taken
directly from the official MIDI specifications. It has no runtime dependencies
and works with any MIDI library or framework -- python-rtmidi, mido, pygame.midi,
or your own socket-level implementation.

It also carries **instrument definitions**: what a *particular model* of synth
or drum machine answers to. Those are a different kind of claim, and the next
section says how they differ.

## Two kinds of fact

Most of this package holds **specification** facts. CC 7 is Volume; note 60 is
C4. They are true for everybody, permanently, they are transcribed from
published standards, and they cannot be wrong about the world.

`pymididefs.instruments` holds **model** facts. A Minitaur ignores notes above
72; a Matriarch's CC 94 switches it between one, two and four voices. They are
true for everybody who owns that model, and they change when the manufacturer
ships firmware.

The difference matters when you are deciding how much to trust a number. **A
model fact is a report, and reports are wrong in the wild.** For one parameter
on one common synth -- the Minitaur's key priority -- the manual, the firmware
addendum, and the `.midnam` file everybody shares give three different answers.
So every instrument definition carries a `source` saying which manual and which
page it came from, and one imported automatically stays marked `unverified`
until a person has checked it. [Sources](#sources), below, says where each of
the bundled ones came from and gives that Minitaur disagreement in full.

**Rig facts are not here and never will be.** Which channel *your* Minitaur is
on, which port it is plugged into, which notes you have chosen to play -- those
belong to your own project, not to a definition shared by everyone who owns the
same box.

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
pip install pymididefs
```

Requires Python 3.10 or later. There are no runtime dependencies.

Reading instrument definitions needs a YAML parser, which is an optional extra
so that the base install keeps pulling in nothing:

```bash
pip install pymididefs[instruments]
```

To install the latest unreleased code straight from the repository:

```bash
pip install git+https://github.com/simonholliday/PyMidiDefs.git
```

## Modules

| Module | Description |
|--------|-------------|
| `pymididefs.notes` | MIDI note numbers (C-1 to G9) and name/number conversion |
| `pymididefs.cc` | Control Change number assignments (0-127), plus 14-bit pack/unpack helpers |
| `pymididefs.rpn` | Standard Registered Parameter Numbers (RPN) and the 14-bit parameter conventions shared with NRPN |
| `pymididefs.drums` | General MIDI percussion key map — GM Level 1 (notes 35-81) plus the extended GS/GM2 sounds |
| `pymididefs.gm` | General MIDI Level 1 instrument program numbers and families |
| `pymididefs.status` | MIDI 1.0 status bytes (channel voice, system common, system real-time) |
| `pymididefs.meta` | Standard MIDI File meta-event type bytes, including RP-019 and the obsolete MIDI Port event |
| `pymididefs.ump` | MIDI 2.0 Universal MIDI Packet message types and constants |
| `pymididefs.ci` | MIDI 2.0 Capability Inquiry (MIDI-CI) constants |
| `pymididefs.instruments` | What a particular model of instrument does -- its controls, voicing and note range. Needs the `instruments` extra |

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
pymididefs.rpn.MODULATION_DEPTH_RANGE  # 5  (added in GM2)
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

### Instrument definitions

```python
import pymididefs.instruments

matriarch = pymididefs.instruments.load("moog_matriarch")

matriarch.voice.voicing_modes            # (1, 2, 4)  switchable voicing
matriarch.voice.plays_note(60)           # True
matriarch.controls["glide_type"].kind    # 'choice'

# What to send to put a banded control into a named state. Definitions record
# the band boundaries as manuals print them; working out the number is this
# library's job.
matriarch.controls["glide_type"].value_for("exp")   # 106

pymididefs.instruments.available()       # what is on the search path
```

Definitions are looked for beside your composition first, then in your own
library, then in the small set bundled here -- so **a file you drop always beats
one we shipped**. That is the whole answer to adding your own synth: no index to
edit, no registration, no pull request. A definition is one self-contained YAML
file, and you share it by sending it.

The bundled set is deliberately small and is a starting point rather than a
catalogue. `moog_dfam.yaml` is five lines, because the DFAM has no MIDI at all
and saying so is worth more than saying nothing.

If your instrument has a `.midnam` file -- Ardour bundles several hundred --
`pymididefs.instruments.midnam` will start a definition from it:

```python
import pymididefs.instruments.midnam

draft = pymididefs.instruments.midnam.read_file("Moog_Minitaur.midnam")
print(pymididefs.instruments.midnam.to_yaml(draft))
```

What that lands is a **draft**, and it says so in its own first line. MIDNAM
carries a control map and nothing else -- no polyphony, no note range, no
velocity response -- and the numbers it does carry are worth checking against
the manual. It stays marked `unverified` until you replace the `source` line
with what you checked it against.

## Sources

### The protocol constants

Every constant in `notes`, `cc`, `rpn`, `drums`, `gm`, `status`, `meta`, `ump`
and `ci` is transcribed from the official MIDI specifications published by
the [MIDI Association](https://midi.org/specs):

- [MIDI 1.0 Detailed Specification](https://midi.org/midi-1-0-detailed-specification) (MMA/AMEI)
- [General MIDI Level 1 Specification](https://midi.org/general-midi-level-1)
- [General MIDI 2 Specification](https://midi.org/general-midi-2)
- [Standard MIDI File 1.0 Specification](https://midi.org/standard-midi-files)
- [M2-104-UM v1.1 — Universal MIDI Packet (UMP) Format and MIDI 2.0 Protocol Specification](https://midi.org/universal-midi-packet-ump-and-midi-2-0-protocol-specification)
- [M2-101-UM v1.2 — MIDI-CI Specification](https://midi.org/midi-ci-specification)

Some specifications require a free [MIDI Association membership](https://midi.org/membership)
to download.

Where a module carries anything from outside those documents it says so in its
own docstring. `pymididefs.meta` is the one that does: it holds two Standard
MIDI File meta-events that no specification defines, because real files contain
them and a reader that does not know them fails on ordinary input.

### The instrument definitions

These come from somewhere else, and it matters which. **A definition is only as
good as its `source` line, and that line is the authority -- not this README.**

```python
matriarch = pymididefs.instruments.load("moog_matriarch")

matriarch.source        # the manual and the pages, in the file's own words
matriarch.is_unverified # True if nobody has checked it yet
matriarch.warnings      # what the validator thought worth saying
```

The definitions bundled here were read out of **manufacturers' own user
manuals**, page by page, and each names the manual and the pages it came from.
Two of the four were checked against a second source as well: the Minitaur
against Moog's firmware v2.1 addendum, and the DRM1's note map against a working
implementation of the same machine.

The Minitaur is the worked example of why that second source matters. Its
manual prints the key-priority bands as `0-42`, `43-84`, `87-127` -- leaving 85
and 86 assigned to nothing -- and the firmware addendum corrects the third band
to **86**. This package carries 86, and the file says why it differs from the
printed table. That is the level of care every bundled definition is held to,
and it is why a `source` line records pages rather than saying "the manual".

**Anything imported is a draft, and is not held to that at all.**
`pymididefs.instruments.midnam` starts a definition from a `.midnam` file, and
what it lands says `imported from <file>, unverified` in its own source line,
keeps saying it, and is reported by the validator until a person replaces it.

That is not a reason to avoid importing -- it is a good way to start and a poor
place to stop, and it is worth being precise about which. Comparing the widely
shared `Moog_Minitaur.midnam` against the same instrument's manual and firmware
addendum, on the one instrument where this package holds both:

- **all 37 control-change numbers agree**, and
- **all 17 14-bit pairings agree**, which is the tedious half of a definition and
  the half most easily mistyped by hand;
- **4 of the 11 comparable band boundaries differ**, including the key-priority
  band it gives as `85` where the manual says `87` and the addendum says `86`.

None of those four changes what gets *sent*, because a band is transmitted as its
midpoint rather than its edge. They do change what gets *read back*: ask that
imported definition what a value of 85 means on key priority and it says `last`,
where the corrected file says `high`. So an import is reliable about which
controller does what, and not yet reliable about what its values mean.

**And a definition you supply yourself is yours.** Files you drop beside your
composition or into your own library beat the ones bundled here, by design, and
this package makes no claim about where their numbers came from.

## License

MIT -- you are free to use, copy, modify, merge, publish, distribute,
sublicense, and sell copies of this software in any project, including
commercial and closed-source applications. The only requirement is that you include the
LICENSE file when redistributing the software. See
[LICENSE](https://github.com/simonholliday/PyMidiDefs/blob/main/LICENSE)
for the full text.
