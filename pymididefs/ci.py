"""MIDI 2.0 Capability Inquiry (MIDI-CI) constants.

MIDI-CI enables bidirectional communication between MIDI devices for
capability discovery, profile configuration, and property exchange.
MIDI-CI messages are transported as Universal System Exclusive (Non-Real-Time).

::

	import pymididefs.ci
	pymididefs.ci.DISCOVERY      # 0x70
	pymididefs.ci.CI_SUB_ID      # 0x0D

Source: M2-101-UM v1.2 — MIDI-CI Specification.
"""


# ── Universal SysEx Framing ──────────────────────────────────────────────────
# MIDI-CI messages are wrapped in Universal Non-Real-Time SysEx:
#   F0 7E <device_id> 0D <sub_id_2> <data...> F7

UNIVERSAL_NON_REALTIME  = 0x7E  # Universal Non-Real-Time SysEx ID byte
UNIVERSAL_REALTIME      = 0x7F  # Universal Real-Time SysEx ID byte
CI_SUB_ID               = 0x0D  # MIDI-CI Sub-ID #1 (identifies CI messages)
BROADCAST_ADDRESS       = 0x7F  # Device ID for broadcast (all devices on port)


# ── MIDI-CI Message Types (Sub-ID #2) ────────────────────────────────────────
# These identify the specific MIDI-CI message within the SysEx payload.

# Management messages
DISCOVERY               = 0x70  # Discovery Inquiry
DISCOVERY_REPLY         = 0x71  # Reply to Discovery
INVALIDATE_MUID         = 0x7E  # Invalidate MUID (device going offline)
NAK                     = 0x7F  # NAK (negative acknowledgement)

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
PROPERTY_GET                = 0x34  # Get Property Data Inquiry
PROPERTY_GET_REPLY          = 0x35  # Reply to Get Property Data
PROPERTY_SET                = 0x36  # Set Property Data Inquiry
PROPERTY_SET_REPLY          = 0x37  # Reply to Set Property Data
PROPERTY_SUBSCRIBE          = 0x38  # Subscription Inquiry
PROPERTY_SUBSCRIBE_REPLY    = 0x39  # Reply to Subscription
PROPERTY_NOTIFY             = 0x3F  # Notify (subscription update)

# Process Inquiry messages (MIDI-CI 1.2)
PROCESS_INQUIRY             = 0x40  # Process Inquiry
PROCESS_INQUIRY_REPLY       = 0x41  # Reply to Process Inquiry
PROCESS_MIDI_REPORT         = 0x42  # MIDI Message Report
PROCESS_MIDI_REPORT_REPLY   = 0x43  # Reply to MIDI Message Report
PROCESS_MIDI_REPORT_END     = 0x44  # End of MIDI Message Report


# ── Broadcast MUID ───────────────────────────────────────────────────────────
# 28-bit MUID (Message Unique Identifier) value used for broadcast discovery.
# Sent as 4 bytes in the SysEx payload (7 bits each, totalling 28 bits).

BROADCAST_MUID          = 0x0FFFFFFF  # All-ones 28-bit MUID (broadcast)


# ── MIDI-CI Version ──────────────────────────────────────────────────────────
# Version byte included in Discovery and Reply to Discovery messages.

CI_VERSION_1_1          = 0x01  # MIDI-CI version 1.1
CI_VERSION_1_2          = 0x02  # MIDI-CI version 1.2
