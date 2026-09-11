"""Tests for pymididefs.ump — MIDI 2.0 Universal MIDI Packet constants."""

import pymididefs.ump


class TestMessageTypes:

	def test_message_type_values (self) -> None:
		"""UMP Message Type nibble values per M2-104-UM v1.1."""
		assert pymididefs.ump.UTILITY == 0x0
		assert pymididefs.ump.SYSTEM == 0x1
		assert pymididefs.ump.MIDI1_CHANNEL_VOICE == 0x2
		assert pymididefs.ump.DATA_64 == 0x3
		assert pymididefs.ump.MIDI2_CHANNEL_VOICE == 0x4
		assert pymididefs.ump.DATA_128 == 0x5
		assert pymididefs.ump.FLEX_DATA == 0xD
		assert pymididefs.ump.STREAM == 0xF

	def test_all_fit_in_4_bits (self) -> None:
		"""Message Types are a 4-bit field (0x0–0xF)."""
		types = [
			pymididefs.ump.UTILITY,
			pymididefs.ump.SYSTEM,
			pymididefs.ump.MIDI1_CHANNEL_VOICE,
			pymididefs.ump.DATA_64,
			pymididefs.ump.MIDI2_CHANNEL_VOICE,
			pymididefs.ump.DATA_128,
			pymididefs.ump.FLEX_DATA,
			pymididefs.ump.STREAM,
		]

		for t in types:
			assert 0x0 <= t <= 0xF


class TestUtilityStatus:

	def test_values (self) -> None:
		"""The status is the nibble in bits 23–20, as M2-104-UM Appendix G gives it."""
		assert pymididefs.ump.UTIL_NOOP == 0x0
		assert pymididefs.ump.UTIL_JR_CLOCK == 0x1
		assert pymididefs.ump.UTIL_JR_TIMESTAMP == 0x2
		assert pymididefs.ump.UTIL_DELTA_CLOCKSTAMP_TPQ == 0x3
		assert pymididefs.ump.UTIL_DELTA_CLOCKSTAMP == 0x4

	def test_not_shifted_into_a_byte (self) -> None:
		"""0.4 and earlier gave 0x10 and 0x20, the nibble shifted into its byte."""
		for status in (
			pymididefs.ump.UTIL_NOOP,
			pymididefs.ump.UTIL_JR_CLOCK,
			pymididefs.ump.UTIL_JR_TIMESTAMP,
			pymididefs.ump.UTIL_DELTA_CLOCKSTAMP_TPQ,
			pymididefs.ump.UTIL_DELTA_CLOCKSTAMP,
		):
			assert 0x0 <= status <= 0xF


class TestMIDI2ChannelVoiceOpcodes:

	def test_note_messages (self) -> None:
		"""MIDI 2.0 Note On/Off opcodes match MIDI 1.0 upper nibble convention."""
		assert pymididefs.ump.MIDI2_NOTE_OFF == 0x8
		assert pymididefs.ump.MIDI2_NOTE_ON == 0x9

	def test_controller_opcodes (self) -> None:
		assert pymididefs.ump.REGISTERED_PER_NOTE_CC == 0x0
		assert pymididefs.ump.ASSIGNABLE_PER_NOTE_CC == 0x1
		assert pymididefs.ump.REGISTERED_CC == 0x2
		assert pymididefs.ump.ASSIGNABLE_CC == 0x3
		assert pymididefs.ump.RELATIVE_REGISTERED_CC == 0x4
		assert pymididefs.ump.RELATIVE_ASSIGNABLE_CC == 0x5

	def test_per_note_messages (self) -> None:
		assert pymididefs.ump.PER_NOTE_PITCH_BEND == 0x6
		assert pymididefs.ump.PER_NOTE_MANAGEMENT == 0xF

	def test_all_fit_in_4_bits (self) -> None:
		"""Opcodes are a 4-bit field."""
		opcodes = [
			pymididefs.ump.REGISTERED_PER_NOTE_CC,
			pymididefs.ump.ASSIGNABLE_PER_NOTE_CC,
			pymididefs.ump.REGISTERED_CC,
			pymididefs.ump.ASSIGNABLE_CC,
			pymididefs.ump.RELATIVE_REGISTERED_CC,
			pymididefs.ump.RELATIVE_ASSIGNABLE_CC,
			pymididefs.ump.PER_NOTE_PITCH_BEND,
			pymididefs.ump.MIDI2_NOTE_OFF,
			pymididefs.ump.MIDI2_NOTE_ON,
			pymididefs.ump.POLY_PRESSURE,
			pymididefs.ump.MIDI2_CONTROL_CHANGE,
			pymididefs.ump.MIDI2_PROGRAM_CHANGE,
			pymididefs.ump.CHANNEL_PRESSURE,
			pymididefs.ump.MIDI2_PITCH_BEND,
			pymididefs.ump.PER_NOTE_MANAGEMENT,
		]

		for op in opcodes:
			assert 0x0 <= op <= 0xF


class TestNoteAttributes:

	def test_values (self) -> None:
		assert pymididefs.ump.ATTR_NONE == 0x00
		assert pymididefs.ump.ATTR_MANUFACTURER == 0x01
		assert pymididefs.ump.ATTR_PROFILE == 0x02
		assert pymididefs.ump.ATTR_PITCH_7_9 == 0x03


class TestPerNoteManagementFlags:

	def test_flags (self) -> None:
		assert pymididefs.ump.PNM_RESET == 0x01
		assert pymididefs.ump.PNM_DETACH == 0x02

	def test_independent_bits (self) -> None:
		"""Flags occupy separate bits and can be combined."""
		assert pymididefs.ump.PNM_RESET & pymididefs.ump.PNM_DETACH == 0


class TestDataMessageStatus:

	def test_values (self) -> None:
		assert pymididefs.ump.DATA_COMPLETE == 0x0
		assert pymididefs.ump.DATA_START == 0x1
		assert pymididefs.ump.DATA_CONTINUE == 0x2
		assert pymididefs.ump.DATA_END == 0x3

	def test_mixed_data_set (self) -> None:
		assert pymididefs.ump.MIXED_DATA_SET_HEADER == 0x8
		assert pymididefs.ump.MIXED_DATA_SET_PAYLOAD == 0x9


class TestFormat:

	def test_values (self) -> None:
		"""The 2-bit Format field shared by Stream and Flex Data messages."""
		assert pymididefs.ump.FORMAT_COMPLETE == 0x0
		assert pymididefs.ump.FORMAT_START == 0x1
		assert pymididefs.ump.FORMAT_CONTINUE == 0x2
		assert pymididefs.ump.FORMAT_END == 0x3


class TestStreamMessages:

	def test_endpoint_messages (self) -> None:
		assert pymididefs.ump.ENDPOINT_DISCOVERY == 0x00
		assert pymididefs.ump.ENDPOINT_INFO == 0x01
		assert pymididefs.ump.DEVICE_IDENTITY == 0x02
		assert pymididefs.ump.ENDPOINT_NAME == 0x03
		assert pymididefs.ump.PRODUCT_INSTANCE_ID == 0x04

	def test_stream_config (self) -> None:
		assert pymididefs.ump.STREAM_CONFIG_REQUEST == 0x05
		assert pymididefs.ump.STREAM_CONFIG_NOTIFY == 0x06

	def test_function_block_messages (self) -> None:
		assert pymididefs.ump.FUNCTION_BLOCK_DISCOVERY == 0x10
		assert pymididefs.ump.FUNCTION_BLOCK_INFO == 0x11
		assert pymididefs.ump.FUNCTION_BLOCK_NAME == 0x12

	def test_clip_messages (self) -> None:
		assert pymididefs.ump.START_OF_CLIP == 0x20
		assert pymididefs.ump.END_OF_CLIP == 0x21


class TestFlexData:

	def test_address (self) -> None:
		assert pymididefs.ump.FLEX_ADDRESS_CHANNEL == 0x0
		assert pymididefs.ump.FLEX_ADDRESS_GROUP == 0x1

	def test_status_banks (self) -> None:
		assert pymididefs.ump.FLEX_BANK_SETUP_PERFORMANCE == 0x00
		assert pymididefs.ump.FLEX_BANK_METADATA_TEXT == 0x01
		assert pymididefs.ump.FLEX_BANK_PERFORMANCE_TEXT == 0x02

	def test_setup_and_performance (self) -> None:
		"""Bank 0x00 skips 0x03 and 0x04, as Appendix G does."""
		assert pymididefs.ump.FLEX_SET_TEMPO == 0x00
		assert pymididefs.ump.FLEX_SET_TIME_SIGNATURE == 0x01
		assert pymididefs.ump.FLEX_SET_METRONOME == 0x02
		assert pymididefs.ump.FLEX_SET_KEY_SIGNATURE == 0x05
		assert pymididefs.ump.FLEX_SET_CHORD_NAME == 0x06

	def test_metadata_text_runs_0x00_to_0x0c (self) -> None:
		in_order = [
			pymididefs.ump.FLEX_UNKNOWN_METADATA_TEXT,
			pymididefs.ump.FLEX_PROJECT_NAME,
			pymididefs.ump.FLEX_COMPOSITION_NAME,
			pymididefs.ump.FLEX_MIDI_CLIP_NAME,
			pymididefs.ump.FLEX_COPYRIGHT_NOTICE,
			pymididefs.ump.FLEX_COMPOSER_NAME,
			pymididefs.ump.FLEX_LYRICIST_NAME,
			pymididefs.ump.FLEX_ARRANGER_NAME,
			pymididefs.ump.FLEX_PUBLISHER_NAME,
			pymididefs.ump.FLEX_PRIMARY_PERFORMER_NAME,
			pymididefs.ump.FLEX_ACCOMPANYING_PERFORMER_NAME,
			pymididefs.ump.FLEX_RECORDING_DATE,
			pymididefs.ump.FLEX_RECORDING_LOCATION,
		]

		assert in_order == list(range(0x0D))

	def test_performance_text_runs_0x00_to_0x04 (self) -> None:
		in_order = [
			pymididefs.ump.FLEX_UNKNOWN_PERFORMANCE_TEXT,
			pymididefs.ump.FLEX_LYRICS,
			pymididefs.ump.FLEX_LYRICS_LANGUAGE,
			pymididefs.ump.FLEX_RUBY,
			pymididefs.ump.FLEX_RUBY_LANGUAGE,
		]

		assert in_order == list(range(0x05))


class TestProtocol:

	def test_protocol_identifiers (self) -> None:
		assert pymididefs.ump.PROTOCOL_MIDI1 == 0x01
		assert pymididefs.ump.PROTOCOL_MIDI2 == 0x02

	def test_jitter_reduction_flags (self) -> None:
		assert pymididefs.ump.JR_TRANSMIT == 0x01
		assert pymididefs.ump.JR_RECEIVE == 0x02
