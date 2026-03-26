"""Standard MIDI File (SMF) meta-event type bytes.

Meta-events appear only in Standard MIDI Files, not in real-time MIDI streams.
Each meta-event is preceded by the status byte 0xFF followed by the type byte
defined here, then a variable-length quantity indicating the data length.

::

	import pymididefs.meta
	pymididefs.meta.TEMPO           # 0x51
	pymididefs.meta.TIME_SIGNATURE  # 0x58

Source: Standard MIDI File (SMF) 1.0 Specification — Meta-Event Definitions.
"""


# ── Text events (0x01–0x07) ──────────────────────────────────────────────────
# Variable-length text encoded as ASCII (or in practice, Latin-1 / UTF-8).

SEQUENCE_NUMBER     = 0x00  # Sequence Number        (optional, 2 bytes: MSB, LSB)
TEXT                = 0x01  # Text Event             (any text annotation)
COPYRIGHT           = 0x02  # Copyright Notice       (should be in first track, at time 0)
TRACK_NAME          = 0x03  # Sequence/Track Name
INSTRUMENT_NAME     = 0x04  # Instrument Name
LYRIC               = 0x05  # Lyric                  (a syllable or word to be sung)
MARKER              = 0x06  # Marker                 (rehearsal letter, section name)
CUE_POINT           = 0x07  # Cue Point              (description of an event in a film/video)


# ── Control events ───────────────────────────────────────────────────────────

CHANNEL_PREFIX      = 0x20  # MIDI Channel Prefix    (1 byte: channel 0–15)
END_OF_TRACK        = 0x2F  # End of Track           (mandatory, 0 data bytes)


# ── Timing events ────────────────────────────────────────────────────────────

TEMPO               = 0x51  # Set Tempo              (3 bytes: microseconds per quarter note)
SMPTE_OFFSET        = 0x54  # SMPTE Offset           (5 bytes: hr, mn, se, fr, ff)
TIME_SIGNATURE      = 0x58  # Time Signature         (4 bytes: nn, dd, cc, bb)
KEY_SIGNATURE       = 0x59  # Key Signature          (2 bytes: sf, mi)


# ── Manufacturer event ───────────────────────────────────────────────────────

SEQUENCER_SPECIFIC  = 0x7F  # Sequencer-Specific Meta-Event (variable-length data)
