"""Tests for pymididefs.ci — MIDI 2.0 Capability Inquiry (MIDI-CI) constants."""

import pymididefs.ci


class TestSysExFraming:

	def test_universal_ids (self) -> None:
		assert pymididefs.ci.UNIVERSAL_NON_REALTIME == 0x7E
		assert pymididefs.ci.UNIVERSAL_REALTIME == 0x7F

	def test_ci_sub_id (self) -> None:
		assert pymididefs.ci.CI_SUB_ID == 0x0D

	def test_device_ids (self) -> None:
		"""M2-101-UM v1.2 Table 5: "7E: To/from Group", "7F: To/from Function Block"."""
		assert pymididefs.ci.DEVICE_ID_GROUP == 0x7E
		assert pymididefs.ci.DEVICE_ID_FUNCTION_BLOCK == 0x7F

	def test_the_misleading_name_is_gone (self) -> None:
		"""0x7F addresses a Function Block, not every device, so it is not called broadcast."""
		assert not hasattr(pymididefs.ci, "BROADCAST_ADDRESS")


class TestProtocolNegotiation:

	def test_deprecated_messages_are_still_named (self) -> None:
		"""Deprecated in MIDI-CI 1.2, and a device supporting them must still parse them."""
		assert pymididefs.ci.PROTOCOL_NEGOTIATION == 0x10
		assert pymididefs.ci.PROTOCOL_NEGOTIATION_REPLY == 0x11
		assert pymididefs.ci.SET_NEW_PROTOCOL == 0x12
		assert pymididefs.ci.TEST_NEW_PROTOCOL_I_TO_R == 0x13
		assert pymididefs.ci.TEST_NEW_PROTOCOL_R_TO_I == 0x14
		assert pymididefs.ci.CONFIRM_NEW_PROTOCOL == 0x15


class TestDiscovery:

	def test_discovery_messages (self) -> None:
		assert pymididefs.ci.DISCOVERY == 0x70
		assert pymididefs.ci.DISCOVERY_REPLY == 0x71

	def test_endpoint_information (self) -> None:
		assert pymididefs.ci.ENDPOINT_INFO_INQUIRY == 0x72
		assert pymididefs.ci.ENDPOINT_INFO_REPLY == 0x73

	def test_management_messages (self) -> None:
		assert pymididefs.ci.ACK == 0x7D
		assert pymididefs.ci.INVALIDATE_MUID == 0x7E
		assert pymididefs.ci.NAK == 0x7F

	def test_sub_ids_are_distinct (self) -> None:
		"""Every Sub-ID #2 names a different message.

		Swept from the module, skipping the framing and addressing bytes, which
		share values with Sub-IDs by coincidence rather than by meaning.
		"""
		framing = {
			"UNIVERSAL_NON_REALTIME", "UNIVERSAL_REALTIME", "CI_SUB_ID",
			"DEVICE_ID_GROUP", "DEVICE_ID_FUNCTION_BLOCK",
			"BROADCAST_MUID", "CI_VERSION_1_1", "CI_VERSION_1_2",
		}
		sub_ids = [
			value
			for name, value in vars(pymididefs.ci).items()
			if name.isupper() and isinstance(value, int) and name not in framing
		]

		assert len(sub_ids) == 38
		assert len(sub_ids) == len(set(sub_ids))


class TestProfileConfiguration:

	def test_profile_inquiry (self) -> None:
		assert pymididefs.ci.PROFILE_INQUIRY == 0x20
		assert pymididefs.ci.PROFILE_INQUIRY_REPLY == 0x21

	def test_profile_control (self) -> None:
		assert pymididefs.ci.SET_PROFILE_ON == 0x22
		assert pymididefs.ci.SET_PROFILE_OFF == 0x23

	def test_profile_reports (self) -> None:
		assert pymididefs.ci.PROFILE_ENABLED == 0x24
		assert pymididefs.ci.PROFILE_DISABLED == 0x25
		assert pymididefs.ci.PROFILE_ADDED == 0x26
		assert pymididefs.ci.PROFILE_REMOVED == 0x27

	def test_profile_details (self) -> None:
		assert pymididefs.ci.PROFILE_DETAILS_INQUIRY == 0x28
		assert pymididefs.ci.PROFILE_DETAILS_REPLY == 0x29
		assert pymididefs.ci.PROFILE_SPECIFIC_DATA == 0x2F


class TestPropertyExchange:

	def test_capabilities (self) -> None:
		assert pymididefs.ci.PROPERTY_CAPABILITIES == 0x30
		assert pymididefs.ci.PROPERTY_CAPABILITIES_REPLY == 0x31

	def test_get_set (self) -> None:
		assert pymididefs.ci.PROPERTY_GET == 0x34
		assert pymididefs.ci.PROPERTY_GET_REPLY == 0x35
		assert pymididefs.ci.PROPERTY_SET == 0x36
		assert pymididefs.ci.PROPERTY_SET_REPLY == 0x37

	def test_subscription (self) -> None:
		assert pymididefs.ci.PROPERTY_SUBSCRIBE == 0x38
		assert pymididefs.ci.PROPERTY_SUBSCRIBE_REPLY == 0x39
		assert pymididefs.ci.PROPERTY_NOTIFY == 0x3F


class TestProcessInquiry:

	def test_values (self) -> None:
		assert pymididefs.ci.PROCESS_INQUIRY == 0x40
		assert pymididefs.ci.PROCESS_INQUIRY_REPLY == 0x41
		assert pymididefs.ci.PROCESS_MIDI_REPORT == 0x42
		assert pymididefs.ci.PROCESS_MIDI_REPORT_REPLY == 0x43
		assert pymididefs.ci.PROCESS_MIDI_REPORT_END == 0x44


class TestBroadcastMUID:

	def test_value (self) -> None:
		"""28-bit broadcast MUID is all ones."""
		assert pymididefs.ci.BROADCAST_MUID == 0x0FFFFFFF

	def test_fits_in_28_bits (self) -> None:
		assert pymididefs.ci.BROADCAST_MUID < (1 << 28)


class TestVersions:

	def test_ci_versions (self) -> None:
		assert pymididefs.ci.CI_VERSION_1_1 == 0x01
		assert pymididefs.ci.CI_VERSION_1_2 == 0x02
