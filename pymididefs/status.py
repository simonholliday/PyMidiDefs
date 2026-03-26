"""MIDI 1.0 status bytes.

Status bytes occupy the range 0x80–0xFF and identify the type of MIDI message.
Channel Voice and Channel Mode messages use the upper nibble as the message
type and the lower nibble as the channel number (0–15).  System messages use
the full byte.

::

	import pymididefs.status
	pymididefs.status.NOTE_ON           # 0x90
	pymididefs.status.TIMING_CLOCK      # 0xF8

Source: MIDI 1.0 Detailed Specification, Table I — Summary of Status Bytes.
"""


# ── Channel Voice Messages (0x80–0xEF) ──────────────────────────────────────
# Upper nibble = message type, lower nibble = channel (0–15).
# Values here are for channel 0; add the channel number to get the
# actual status byte (e.g. NOTE_ON | 5 = 0x95 for channel 5).

NOTE_OFF            = 0x80  # Note Off                 (+ note number, velocity)
NOTE_ON             = 0x90  # Note On                  (+ note number, velocity)
POLY_AFTERTOUCH     = 0xA0  # Polyphonic Key Pressure  (+ note number, pressure)
CONTROL_CHANGE      = 0xB0  # Control Change           (+ controller number, value)
PROGRAM_CHANGE      = 0xC0  # Program Change           (+ program number)
CHANNEL_AFTERTOUCH  = 0xD0  # Channel Pressure         (+ pressure)
PITCH_BEND          = 0xE0  # Pitch Bend Change        (+ LSB, MSB)


# ── System Common Messages (0xF0–0xF7) ──────────────────────────────────────
# Not channel-specific.  Intended for all receivers on the MIDI bus.

SYSEX_START         = 0xF0  # System Exclusive start     (followed by data, then SYSEX_END)
TIME_CODE           = 0xF1  # MIDI Time Code Quarter Frame (+ data)
SONG_POSITION       = 0xF2  # Song Position Pointer      (+ LSB, MSB)
SONG_SELECT         = 0xF3  # Song Select                (+ song number)
# 0xF4: Undefined
# 0xF5: Undefined
TUNE_REQUEST        = 0xF6  # Tune Request               (no data bytes)
SYSEX_END           = 0xF7  # End of Exclusive (EOX)


# ── System Real-Time Messages (0xF8–0xFF) ────────────────────────────────────
# Single-byte messages for timing and synchronisation.
# May be interleaved within any other message.

TIMING_CLOCK        = 0xF8  # Timing Clock   (24 clocks per quarter note)
# 0xF9: Undefined
START               = 0xFA  # Start          (start playback from beginning)
CONTINUE            = 0xFB  # Continue       (resume playback from current position)
STOP                = 0xFC  # Stop           (stop playback)
# 0xFD: Undefined
ACTIVE_SENSING      = 0xFE  # Active Sensing (heartbeat; optional)
SYSTEM_RESET        = 0xFF  # System Reset   (reset all receivers to power-up state)
