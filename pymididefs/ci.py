"""MIDI 2.0 Capability Inquiry (MIDI-CI) constants.

MIDI-CI enables bidirectional communication between MIDI devices for
capability discovery, profile configuration, and property exchange.
MIDI-CI messages are transported as Universal System Exclusive (Non-Real-Time).

::

	import pymididefs.ci
	pymididefs.ci.DISCOVERY      # 0x70
	pymididefs.ci.CI_SUB_ID      # 0x0D

Source: M2-101-UM v1.2 — MIDI-CI Specification.  Message names follow its
Appendix D.
"""


# ── Universal SysEx Framing ──────────────────────────────────────────────────
# MIDI-CI messages are wrapped in Universal Non-Real-Time SysEx:
#   F0 7E <device_id> 0D <sub_id_2> <data...> F7

UNIVERSAL_NON_REALTIME  = 0x7E  # Universal Non-Real-Time SysEx ID byte
UNIVERSAL_REALTIME      = 0x7F  # Universal Real-Time SysEx ID byte (MIDI-CI does not use it)
CI_SUB_ID               = 0x0D  # MIDI-CI Sub-ID #1 (identifies CI messages)


# ── Device ID ────────────────────────────────────────────────────────────────
# The <device_id> byte says what a message is to or from.  0x00–0x0F are MIDI
# channels 1–16; these two are not channelized, and address a whole Group or
# Function Block.

DEVICE_ID_GROUP          = 0x7E  # To/from Group
DEVICE_ID_FUNCTION_BLOCK = 0x7F  # To/from Function Block (the whole block, not channelized)


# ── MIDI-CI Message Types (Sub-ID #2) ────────────────────────────────────────
# These identify the specific MIDI-CI message within the SysEx payload.

# Protocol Negotiation messages -- every one deprecated as of MIDI-CI 1.2,
# which leaves selecting a protocol to UMP Stream messages.  A device that
# supports Protocol Negotiation must still be able to parse them: MIDI-CI
# requires every earlier version of each function a device supports to stay
# readable, "even if Inquiries from previous versions have been deprecated".
PROTOCOL_NEGOTIATION        = 0x10  # Initiate Protocol Negotiation (deprecated)
PROTOCOL_NEGOTIATION_REPLY  = 0x11  # Reply to Initiate Protocol Negotiation (deprecated)
SET_NEW_PROTOCOL            = 0x12  # Set New Selected Protocol (deprecated)
TEST_NEW_PROTOCOL_I_TO_R    = 0x13  # Test New Protocol Initiator to Responder (deprecated)
TEST_NEW_PROTOCOL_R_TO_I    = 0x14  # Test New Protocol Responder to Initiator (deprecated)
CONFIRM_NEW_PROTOCOL        = 0x15  # Confirmation Protocol Established (deprecated)

# Profile Configuration messages
PROFILE_INQUIRY             = 0x20  # Profile Inquiry
PROFILE_INQUIRY_REPLY       = 0x21  # Reply to Profile Inquiry
SET_PROFILE_ON              = 0x22  # Set Profile On
SET_PROFILE_OFF             = 0x23  # Set Profile Off
PROFILE_ENABLED             = 0x24  # Profile Enabled Report
PROFILE_DISABLED            = 0x25  # Profile Disabled Report
PROFILE_ADDED               = 0x26  # Profile Added Report
PROFILE_REMOVED             = 0x27  # Profile Removed Report
PROFILE_DETAILS_INQUIRY     = 0x28  # Profile Details Inquiry
PROFILE_DETAILS_REPLY       = 0x29  # Reply to Profile Details Inquiry
PROFILE_SPECIFIC_DATA       = 0x2F  # Profile Specific Data

# Property Exchange messages
PROPERTY_CAPABILITIES       = 0x30  # Inquiry: Property Exchange Capabilities
PROPERTY_CAPABILITIES_REPLY = 0x31  # Reply to Property Exchange Capabilities
# 0x32–0x33: Has Property Data (reserved)
PROPERTY_GET                = 0x34  # Inquiry: Get Property Data
PROPERTY_GET_REPLY          = 0x35  # Reply to Get Property Data
PROPERTY_SET                = 0x36  # Inquiry: Set Property Data
PROPERTY_SET_REPLY          = 0x37  # Reply to Set Property Data
PROPERTY_SUBSCRIBE          = 0x38  # Subscription (from either side; the Responder also sends updates to subscribed data with it)
PROPERTY_SUBSCRIBE_REPLY    = 0x39  # Reply to Subscription
PROPERTY_NOTIFY             = 0x3F  # Notify (informative: errors and other information)

# Process Inquiry messages (MIDI-CI 1.2)
PROCESS_INQUIRY             = 0x40  # Inquiry: Process Inquiry Capabilities
PROCESS_INQUIRY_REPLY       = 0x41  # Reply to Process Inquiry Capabilities
PROCESS_MIDI_REPORT         = 0x42  # Inquiry: MIDI Message Report
PROCESS_MIDI_REPORT_REPLY   = 0x43  # Reply to MIDI Message Report
PROCESS_MIDI_REPORT_END     = 0x44  # End of MIDI Message Report

# Management messages
DISCOVERY                   = 0x70  # Discovery
DISCOVERY_REPLY             = 0x71  # Reply to Discovery
ENDPOINT_INFO_INQUIRY       = 0x72  # Inquiry: Endpoint Information
ENDPOINT_INFO_REPLY         = 0x73  # Reply to Endpoint Information
ACK                         = 0x7D  # MIDI-CI ACK
INVALIDATE_MUID             = 0x7E  # Invalidate MUID (a MUID is no longer in use)
NAK                         = 0x7F  # MIDI-CI NAK


# ── Broadcast MUID ───────────────────────────────────────────────────────────
# 28-bit MUID (Message Unique Identifier) that addresses every device, sent as
# four 7-bit bytes: 7F 7F 7F 7F.  Discovery is sent to it, and so are Invalidate
# MUID and several Profile messages.  0x0FFFFF00–0x0FFFFFFE are reserved.

BROADCAST_MUID          = 0x0FFFFFFF  # All-ones 28-bit MUID (broadcast)


# ── MIDI-CI Version ──────────────────────────────────────────────────────────
# The Message Version/Format byte that every MIDI-CI message carries.

CI_VERSION_1_1          = 0x01  # MIDI-CI version 1.1
CI_VERSION_1_2          = 0x02  # MIDI-CI version 1.2
