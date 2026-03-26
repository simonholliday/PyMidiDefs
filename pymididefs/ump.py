"""MIDI 2.0 Universal MIDI Packet (UMP) message types and constants.

The Universal MIDI Packet is the transport-agnostic message format introduced
by MIDI 2.0.  Every UMP begins with a 32-bit word whose upper nibble
identifies the Message Type, determining the packet size and semantics.

MIDI 2.0 is a strict superset of MIDI 1.0 — all MIDI 1.0 definitions remain
valid.  MIDI 1.0 Channel Voice Messages are carried inside UMP Message Type 2;
MIDI 2.0 Channel Voice Messages (with higher resolution) use Message Type 4.

::

	import pymididefs.ump
	pymididefs.ump.MIDI2_CHANNEL_VOICE  # 0x4
	pymididefs.ump.NOTE_ON              # 0x9

Source: M2-104-UM v1.1 — Universal MIDI Packet (UMP) Format and
MIDI 2.0 Protocol Specification.
"""


# ── UMP Message Types ────────────────────────────────────────────────────────
# 4-bit value occupying bits 31–28 of the first UMP word.
# Determines the total packet size (32, 64, 96, or 128 bits).
#
# Packet sizes:
#   32-bit  (1 word):  Types 0x0, 0x1, 0x2
#   64-bit  (2 words): Types 0x3, 0x4
#   128-bit (4 words): Types 0x5, 0xD, 0xF

UTILITY             = 0x0  # Utility Messages        (JR Clock, JR Timestamp)
SYSTEM              = 0x1  # System Common & Real-Time
MIDI1_CHANNEL_VOICE = 0x2  # MIDI 1.0 Channel Voice Messages (7-bit resolution)
DATA_64             = 0x3  # Data Messages, 64-bit   (7-bit SysEx)
MIDI2_CHANNEL_VOICE = 0x4  # MIDI 2.0 Channel Voice Messages (full resolution)
DATA_128            = 0x5  # Data Messages, 128-bit  (8-bit SysEx, Mixed Data Set)
# 0x6–0xC: Reserved
FLEX_DATA           = 0xD  # Flex Data Messages      (text, lyrics, metadata — UMP 1.1)
# 0xE: Reserved
STREAM              = 0xF  # Stream Messages         (endpoint discovery, configuration)


# ── Utility Message Status (Message Type 0x0) ────────────────────────────────
# Status field occupies bits 19–16 of the 32-bit Utility message.

UTIL_NOOP           = 0x00  # No Operation
UTIL_JR_CLOCK       = 0x10  # Jitter Reduction Clock      (16-bit sender clock)
UTIL_JR_TIMESTAMP   = 0x20  # Jitter Reduction Timestamp  (16-bit delta time)


# ── MIDI 2.0 Channel Voice Message Opcodes (Message Type 0x4) ────────────────
# 4-bit opcode field in bits 23–20 of the first word.
# These extend the MIDI 1.0 opcodes with new per-note and registered
# controller messages.  MIDI 2.0 Channel Voice Messages are 64-bit (2 words).

REGISTERED_PER_NOTE_CC  = 0x0  # Registered Per-Note Controller
ASSIGNABLE_PER_NOTE_CC  = 0x1  # Assignable Per-Note Controller
REGISTERED_CC           = 0x2  # Registered Controller (replaces RPN)
ASSIGNABLE_CC           = 0x3  # Assignable Controller (replaces NRPN)
RELATIVE_REGISTERED_CC  = 0x4  # Relative Registered Controller
RELATIVE_ASSIGNABLE_CC  = 0x5  # Relative Assignable Controller
PER_NOTE_PITCH_BEND     = 0x6  # Per-Note Pitch Bend
# 0x7: Reserved
NOTE_OFF                = 0x8  # Note Off            (+ 16-bit velocity)
NOTE_ON                 = 0x9  # Note On             (+ 16-bit velocity, attribute)
POLY_PRESSURE           = 0xA  # Poly Pressure       (32-bit pressure)
CONTROL_CHANGE          = 0xB  # Control Change      (32-bit value)
PROGRAM_CHANGE          = 0xC  # Program Change      (+ optional bank select)
CHANNEL_PRESSURE        = 0xD  # Channel Pressure    (32-bit pressure)
PITCH_BEND              = 0xE  # Pitch Bend          (32-bit value)
PER_NOTE_MANAGEMENT     = 0xF  # Per-Note Management (detach / reset flags)


# ── Note Attribute Types ─────────────────────────────────────────────────────
# 8-bit field in MIDI 2.0 Note On and Note Off messages specifying
# the interpretation of the 16-bit attribute data field.

ATTR_NONE               = 0x00  # No attribute data
ATTR_MANUFACTURER       = 0x01  # Manufacturer Specific
ATTR_PROFILE            = 0x02  # Profile Specific
ATTR_PITCH_7_9          = 0x03  # Pitch 7.9 (7-bit semitone + 9-bit fraction)


# ── Per-Note Management Flags ────────────────────────────────────────────────
# Bit flags in the Per-Note Management message (opcode 0xF).

PNM_RESET               = 0x01  # Reset / re-articulate the note
PNM_DETACH              = 0x02  # Detach note from controllers


# ── Data Message Status (Message Types 0x3 and 0x5) ─────────────────────────
# 4-bit status field indicating SysEx segmentation.

DATA_COMPLETE           = 0x0  # Complete SysEx in a single packet
DATA_START              = 0x1  # First packet of a multi-packet SysEx
DATA_CONTINUE           = 0x2  # Continuation packet
DATA_END                = 0x3  # Final packet of a multi-packet SysEx


# ── Stream Message Status (Message Type 0xF) ─────────────────────────────────
# 10-bit status/format field.  Used for endpoint discovery, function block
# queries, and stream configuration.

ENDPOINT_DISCOVERY      = 0x00  # Endpoint Discovery request
ENDPOINT_INFO           = 0x01  # Endpoint Info Notification reply
DEVICE_IDENTITY         = 0x02  # Device Identity Notification
ENDPOINT_NAME           = 0x03  # Endpoint Name Notification
PRODUCT_INSTANCE_ID     = 0x04  # Product Instance ID Notification
STREAM_CONFIG_REQUEST   = 0x05  # Stream Configuration Request
STREAM_CONFIG_NOTIFY    = 0x06  # Stream Configuration Notification

FUNCTION_BLOCK_DISCOVERY = 0x10  # Function Block Discovery request
FUNCTION_BLOCK_INFO     = 0x11  # Function Block Info Notification
FUNCTION_BLOCK_NAME     = 0x12  # Function Block Name Notification


# ── Protocol Type Identifiers ────────────────────────────────────────────────
# Used in Stream Configuration messages to negotiate the active protocol.

PROTOCOL_MIDI1          = 0x01  # MIDI 1.0 Protocol
PROTOCOL_MIDI2          = 0x02  # MIDI 2.0 Protocol


# ── Jitter Reduction Extension Flags ─────────────────────────────────────────
# Bit flags in Endpoint Info and Stream Configuration messages.

JR_TRANSMIT             = 0x01  # Endpoint transmits JR Timestamps
JR_RECEIVE              = 0x02  # Endpoint receives JR Timestamps
