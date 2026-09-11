"""Standard MIDI File (SMF) meta-event type bytes.

Meta-events appear only in Standard MIDI Files, not in real-time MIDI streams.
Each meta-event is preceded by the status byte 0xFF followed by the type byte
defined here, then a variable-length quantity indicating the data length.

::

	import pymididefs.meta
	pymididefs.meta.TEMPO           # 0x51
	pymididefs.meta.TIME_SIGNATURE  # 0x58

Most of these come from the SMF 1.0 specification (RP-001).  Four do not:

* ``PROGRAM_NAME`` (0x08) and ``DEVICE_NAME`` (0x09) are text events assigned
  by MMA Recommended Practice RP-019.  SMF 1.0 reserves 0x01–0x0F for text and
  leaves both unassigned; RP-019 names them.
* ``XMF_PATCH_TYPE_PREFIX`` (0x60) is assigned by RP-032.  Its one data byte
  says which instruments a track in an XMF file was written for: 0x01 General
  MIDI 1, 0x02 General MIDI 2, 0x03 DLS.  A track that does not begin with one
  is taken to mean General MIDI 1.
* ``MIDI_PORT`` (0x21) is not defined by any specification.  It is an
  unofficial convention, now obsolete -- Cakewalk is the sequencer sources name
  as writing it -- and it is here because files in the wild still carry it.

The first three are read in each specification's own text.  ``MIDI_PORT`` has
no specification to read, so it rests on implementations instead: ``mido``'s
Standard MIDI File parser reads it from real files, as it does 0x09.  This
package is only worth using if its numbers are right, so nothing goes in that
cannot be checked against either a specification or a working implementation.

Sources: Standard MIDI File (SMF) 1.0 Specification (RP-001) -- Meta-Event
Definitions; MMA RP-019 (0x08, 0x09); MMA/AMEI RP-032 (0x60); de facto practice
(0x21).
"""


# ── Sequence number (0x00) ───────────────────────────────────────────────────

SEQUENCE_NUMBER     = 0x00  # Sequence Number        (optional, 2 bytes: MSB, LSB)


# ── Text events (0x01–0x07) ──────────────────────────────────────────────────
# Variable-length text.  SMF 1.0 asks for printable ASCII "for maximum
# interchange".

TEXT                = 0x01  # Text Event             (any text annotation)
COPYRIGHT           = 0x02  # Copyright Notice       (should be in first track, at time 0)
TRACK_NAME          = 0x03  # Sequence/Track Name
INSTRUMENT_NAME     = 0x04  # Instrument Name
LYRIC               = 0x05  # Lyric                  (a syllable or word to be sung)
MARKER              = 0x06  # Marker                 (rehearsal letter, section name)
CUE_POINT           = 0x07  # Cue Point              (something happening on a film or video screen or stage)


# ── Text events assigned by RP-019 (0x08–0x09) ───────────────────────────────
# Inside SMF 1.0's reserved text range, named by a later MMA recommendation.

PROGRAM_NAME        = 0x08  # Program Name           (names the program the following bank select and program change call up)
DEVICE_NAME         = 0x09  # Device Name            (the device this track is intended to address)


# ── Control events ───────────────────────────────────────────────────────────

CHANNEL_PREFIX      = 0x20  # MIDI Channel Prefix    (1 byte: channel 0–15)
MIDI_PORT           = 0x21  # MIDI Port              (1 byte; obsolete, in no spec, but still in files)
END_OF_TRACK        = 0x2F  # End of Track           (mandatory, 0 data bytes)


# ── Timing events ────────────────────────────────────────────────────────────

TEMPO               = 0x51  # Set Tempo              (3 bytes: microseconds per quarter note)
SMPTE_OFFSET        = 0x54  # SMPTE Offset           (5 bytes: hr, mn, se, fr, ff)
TIME_SIGNATURE      = 0x58  # Time Signature         (4 bytes: nn, dd, cc, bb)
KEY_SIGNATURE       = 0x59  # Key Signature          (2 bytes: sf, mi)


# ── XMF instrument set (0x60) ────────────────────────────────────────────────
# Assigned by RP-032, for SMF tracks carried inside an XMF file.

XMF_PATCH_TYPE_PREFIX = 0x60  # XMF Patch Type Prefix (1 byte: 0x01 GM1, 0x02 GM2, 0x03 DLS)


# ── Manufacturer event ───────────────────────────────────────────────────────

SEQUENCER_SPECIFIC  = 0x7F  # Sequencer-Specific Meta-Event (variable-length data)
