"""Standard MIDI File (SMF) meta-event type bytes.

Meta-events appear only in Standard MIDI Files, not in real-time MIDI streams.
Each meta-event is preceded by the status byte 0xFF followed by the type byte
defined here, then a variable-length quantity indicating the data length.

::

	import pymididefs.meta
	pymididefs.meta.TEMPO           # 0x51
	pymididefs.meta.TIME_SIGNATURE  # 0x58

Most of these come from the SMF 1.0 specification.  Three do not, and are here
because files in the wild contain them — a reader that does not know them meets
an unrecognised type byte on ordinary input:

* ``PROGRAM_NAME`` (0x08) and ``DEVICE_NAME`` (0x09) are text events assigned by
  MMA Recommended Practice RP-019.  SMF 1.0 reserves 0x01–0x0F for text and
  leaves these two unassigned; RP-019 names them.
* ``MIDI_PORT`` (0x21) is not defined by any specification.  It is an obsolete
  convention that many sequencers wrote and some still do, and it is the one an
  SMF reader is most likely to actually encounter.

How far each of the three has actually been checked, since this package is only
worth using if its numbers are right:

* 0x09 and 0x21 are corroborated by ``mido``'s Standard MIDI File parser, which
  reads both from real files.
* **0x08 is not corroborated by anything to hand.**  ``mido`` does not implement
  it at all.  It is recorded here from secondary sources and should be confirmed
  against RP-019 itself before anybody relies on it.

Sources: Standard MIDI File (SMF) 1.0 Specification — Meta-Event Definitions;
MMA RP-019 (0x08, 0x09); de facto practice (0x21).
"""


# ── Sequence number (0x00) ───────────────────────────────────────────────────

SEQUENCE_NUMBER     = 0x00  # Sequence Number        (optional, 2 bytes: MSB, LSB)


# ── Text events (0x01–0x07) ──────────────────────────────────────────────────
# Variable-length text encoded as ASCII (or in practice, Latin-1 / UTF-8).

TEXT                = 0x01  # Text Event             (any text annotation)
COPYRIGHT           = 0x02  # Copyright Notice       (should be in first track, at time 0)
TRACK_NAME          = 0x03  # Sequence/Track Name
INSTRUMENT_NAME     = 0x04  # Instrument Name
LYRIC               = 0x05  # Lyric                  (a syllable or word to be sung)
MARKER              = 0x06  # Marker                 (rehearsal letter, section name)
CUE_POINT           = 0x07  # Cue Point              (description of an event in a film/video)


# ── Text events assigned by RP-019 (0x08–0x09) ───────────────────────────────
# Inside SMF 1.0's reserved text range, named by a later MMA recommendation.

PROGRAM_NAME        = 0x08  # Program Name    (the patch this track calls for)
                            # UNCONFIRMED — see the module docstring before relying on this
DEVICE_NAME         = 0x09  # Device Name     (the port or instrument it plays on)


# ── Control events ───────────────────────────────────────────────────────────

CHANNEL_PREFIX      = 0x20  # MIDI Channel Prefix    (1 byte: channel 0–15)
MIDI_PORT           = 0x21  # MIDI Port              (1 byte; obsolete, in no spec, but widely written)
END_OF_TRACK        = 0x2F  # End of Track           (mandatory, 0 data bytes)


# ── Timing events ────────────────────────────────────────────────────────────

TEMPO               = 0x51  # Set Tempo              (3 bytes: microseconds per quarter note)
SMPTE_OFFSET        = 0x54  # SMPTE Offset           (5 bytes: hr, mn, se, fr, ff)
TIME_SIGNATURE      = 0x58  # Time Signature         (4 bytes: nn, dd, cc, bb)
KEY_SIGNATURE       = 0x59  # Key Signature          (2 bytes: sf, mi)


# ── Manufacturer event ───────────────────────────────────────────────────────

SEQUENCER_SPECIFIC  = 0x7F  # Sequencer-Specific Meta-Event (variable-length data)
