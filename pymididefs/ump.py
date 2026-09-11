"""MIDI 2.0 Universal MIDI Packet (UMP) message types and constants.

The Universal MIDI Packet is the transport-agnostic message format introduced
by MIDI 2.0.  Every UMP begins with a 32-bit word whose upper nibble
identifies the Message Type, determining the packet size and semantics.

MIDI 2.0 extends MIDI 1.0 rather than replacing it.  MIDI 1.0 Channel Voice
Messages are carried inside UMP Message Type 2; MIDI 2.0 Channel Voice Messages
(with higher resolution) use Message Type 4.  A device using the MIDI 2.0
Protocol does not send Type 2, except to a Function Block that declares a
MIDI 1.0 connection.

A field that is a nibble -- a message type, an opcode, a status -- is given
here as the nibble itself (0x9), never shifted into the byte it shares (0x90).
The wider fields are the 10-bit Stream status, the 8-bit Flex Data status bank
and status, the 8-bit note attribute type, and the 8-bit Protocol field of the
Stream Configuration messages.

::

	import pymididefs.ump
	pymididefs.ump.MIDI2_CHANNEL_VOICE  # 0x4
	pymididefs.ump.MIDI2_NOTE_ON        # 0x9  (an opcode, not the 0x90 status byte)

Source: M2-104-UM v1.1.2 — Universal MIDI Packet (UMP) Format and
MIDI 2.0 Protocol Specification.
"""


# ── UMP Message Types ────────────────────────────────────────────────────────
# 4-bit value occupying bits 31–28 of the first UMP word.
# Determines the total packet size (32, 64, 96, or 128 bits).
#
# Packet sizes, reserved types included:
#   32-bit  (1 word):  Types 0x0, 0x1, 0x2; reserved 0x6, 0x7
#   64-bit  (2 words): Types 0x3, 0x4; reserved 0x8, 0x9, 0xA
#   96-bit  (3 words): reserved 0xB, 0xC
#   128-bit (4 words): Types 0x5, 0xD, 0xF; reserved 0xE

UTILITY             = 0x0  # Utility Messages        (NOOP, jitter reduction, delta clockstamps)
SYSTEM              = 0x1  # System Common & Real-Time
MIDI1_CHANNEL_VOICE = 0x2  # MIDI 1.0 Channel Voice Messages (7-bit data; 14-bit pitch bend)
DATA_64             = 0x3  # Data Messages, 64-bit   (7-bit SysEx)
MIDI2_CHANNEL_VOICE = 0x4  # MIDI 2.0 Channel Voice Messages (full resolution)
DATA_128            = 0x5  # Data Messages, 128-bit  (8-bit SysEx, Mixed Data Set)
# 0x6–0xC: Reserved
FLEX_DATA           = 0xD  # Flex Data Messages      (tempo, signatures, chord names, text — UMP 1.1)
# 0xE: Reserved
STREAM              = 0xF  # Stream Messages         (endpoint discovery, configuration)


# ── Utility Message Status (Message Type 0x0) ────────────────────────────────
# 4-bit Status field in bits 23–20 of the 32-bit Utility message.  The Group
# field before it is reserved, so a Utility message belongs to no Group.

UTIL_NOOP                   = 0x0  # No Operation
UTIL_JR_CLOCK               = 0x1  # Jitter Reduction Clock      (16-bit sender clock)
UTIL_JR_TIMESTAMP           = 0x2  # Jitter Reduction Timestamp  (16-bit time on the sender's clock)
UTIL_DELTA_CLOCKSTAMP_TPQ   = 0x3  # Delta Clockstamp Ticks Per Quarter Note (16 bits; UMP 1.1, for MIDI Clip Files)
UTIL_DELTA_CLOCKSTAMP       = 0x4  # Delta Clockstamp: ticks since the last event (20 bits; UMP 1.1)


# ── MIDI 2.0 Channel Voice Message Opcodes (Message Type 0x4) ────────────────
# 4-bit opcode field in bits 23–20 of the first word.
# These extend the MIDI 1.0 opcodes with new per-note and registered
# controller messages.  MIDI 2.0 Channel Voice Messages are 64-bit (2 words).
#
# The five opcodes that share a name with a MIDI 1.0 status byte carry a
# MIDI2_ prefix.  A UMP opcode is a nibble (0x9) and a status byte is a whole
# byte (0x90), so a caller who ends up with the wrong one has a number that
# looks plausible and is not a status byte at all.

REGISTERED_PER_NOTE_CC  = 0x0  # Registered Per-Note Controller
ASSIGNABLE_PER_NOTE_CC  = 0x1  # Assignable Per-Note Controller
REGISTERED_CC           = 0x2  # Registered Controller (replaces RPN)
ASSIGNABLE_CC           = 0x3  # Assignable Controller (replaces NRPN)
RELATIVE_REGISTERED_CC  = 0x4  # Relative Registered Controller
RELATIVE_ASSIGNABLE_CC  = 0x5  # Relative Assignable Controller
PER_NOTE_PITCH_BEND     = 0x6  # Per-Note Pitch Bend
# 0x7: Reserved
MIDI2_NOTE_OFF          = 0x8  # Note Off            (+ 16-bit velocity, attribute)
MIDI2_NOTE_ON           = 0x9  # Note On             (+ 16-bit velocity, attribute)
POLY_PRESSURE           = 0xA  # Poly Pressure       (32-bit pressure)
MIDI2_CONTROL_CHANGE    = 0xB  # Control Change      (32-bit value)
MIDI2_PROGRAM_CHANGE    = 0xC  # Program Change      (+ optional bank select)
CHANNEL_PRESSURE        = 0xD  # Channel Pressure    (32-bit pressure)
MIDI2_PITCH_BEND        = 0xE  # Pitch Bend          (32-bit value)
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

PNM_RESET               = 0x01  # S: Reset (Set) Per-Note Controllers to default values
PNM_DETACH              = 0x02  # D: Detach Per-Note Controllers from previously received notes


# ── Data Message Status (Message Types 0x3 and 0x5) ─────────────────────────
# 4-bit Status field.  0x0–0x3 place a System Exclusive packet within its
# message, for both 7-bit (Type 0x3) and 8-bit (Type 0x5) SysEx.

DATA_COMPLETE           = 0x0  # Complete SysEx in a single packet
DATA_START              = 0x1  # First packet of a multi-packet SysEx
DATA_CONTINUE           = 0x2  # Continuation packet
DATA_END                = 0x3  # Final packet of a multi-packet SysEx

# Type 0x5 only.
MIXED_DATA_SET_HEADER   = 0x8  # Mixed Data Set Header
MIXED_DATA_SET_PAYLOAD  = 0x9  # Mixed Data Set Payload


# ── Format (Message Types 0xD and 0xF) ───────────────────────────────────────
# 2-bit Format field of Flex Data and Stream messages: whether this packet is a
# whole message or one part of a message that spans several.

FORMAT_COMPLETE         = 0x0  # Complete message in one UMP
FORMAT_START            = 0x1  # Start of a message spanning two or more UMPs
FORMAT_CONTINUE         = 0x2  # Continuing a message spanning three or more UMPs
FORMAT_END              = 0x3  # End of a message spanning two or more UMPs


# ── Stream Message Status (Message Type 0xF) ─────────────────────────────────
# 10-bit Status field, after the 2-bit Format field.  Used for endpoint
# discovery, function block queries, and stream configuration.

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

START_OF_CLIP           = 0x20  # Start of Clip (the first event of a MIDI Clip File's sequence)
END_OF_CLIP             = 0x21  # End of Clip


# ── Protocol Type Identifiers ────────────────────────────────────────────────
# Used in Stream Configuration Request and Notification messages to select the
# active protocol.  This replaces MIDI-CI's Protocol Negotiation.

PROTOCOL_MIDI1          = 0x01  # MIDI 1.0 Protocol
PROTOCOL_MIDI2          = 0x02  # MIDI 2.0 Protocol


# ── Jitter Reduction Extension Flags ─────────────────────────────────────────
# Bit flags in Endpoint Info and Stream Configuration messages.

JR_TRANSMIT             = 0x01  # Endpoint transmits JR Timestamps
JR_RECEIVE              = 0x02  # Endpoint receives JR Timestamps


# ── Flex Data (Message Type 0xD) ─────────────────────────────────────────────
# After the Format field come a 2-bit Address field, a 4-bit Channel field, an
# 8-bit Status Bank and an 8-bit Status.  Status values repeat from bank to
# bank, so a status is only meaningful beside its bank.  Text in banks 0x01 and
# 0x02 is UTF-8.

FLEX_ADDRESS_CHANNEL        = 0x0  # Sent to the Channel in the Channel field
FLEX_ADDRESS_GROUP          = 0x1  # Sent to the Group (Channel field ignored)

FLEX_BANK_SETUP_PERFORMANCE = 0x00  # Setup & Performance Events (no text)
FLEX_BANK_METADATA_TEXT     = 0x01  # Metadata Text
FLEX_BANK_PERFORMANCE_TEXT  = 0x02  # Performance Text Events (including lyrics)

# Bank 0x00, Setup & Performance Events
FLEX_SET_TEMPO              = 0x00  # Set Tempo (10-nanosecond units per quarter note)
FLEX_SET_TIME_SIGNATURE     = 0x01  # Set Time Signature
FLEX_SET_METRONOME          = 0x02  # Set Metronome
FLEX_SET_KEY_SIGNATURE      = 0x05  # Set Key Signature
FLEX_SET_CHORD_NAME         = 0x06  # Set Chord Name

# Bank 0x01, Metadata Text
FLEX_UNKNOWN_METADATA_TEXT      = 0x00  # Unknown Metadata Text Event
FLEX_PROJECT_NAME               = 0x01  # Project Name
FLEX_COMPOSITION_NAME           = 0x02  # Composition (Song) Name
FLEX_MIDI_CLIP_NAME             = 0x03  # MIDI Clip Name
FLEX_COPYRIGHT_NOTICE           = 0x04  # Copyright Notice
FLEX_COMPOSER_NAME              = 0x05  # Composer Name
FLEX_LYRICIST_NAME              = 0x06  # Lyricist Name
FLEX_ARRANGER_NAME              = 0x07  # Arranger Name
FLEX_PUBLISHER_NAME             = 0x08  # Publisher Name
FLEX_PRIMARY_PERFORMER_NAME     = 0x09  # Primary Performer Name
FLEX_ACCOMPANYING_PERFORMER_NAME = 0x0A  # Accompanying Performer Name
FLEX_RECORDING_DATE             = 0x0B  # Recording/Concert Date
FLEX_RECORDING_LOCATION         = 0x0C  # Recording/Concert Location

# Bank 0x02, Performance Text Events
FLEX_UNKNOWN_PERFORMANCE_TEXT   = 0x00  # Unknown Performance Text Event
FLEX_LYRICS                     = 0x01  # Lyrics
FLEX_LYRICS_LANGUAGE            = 0x02  # Lyrics Language
FLEX_RUBY                       = 0x03  # Ruby
FLEX_RUBY_LANGUAGE              = 0x04  # Ruby Language
