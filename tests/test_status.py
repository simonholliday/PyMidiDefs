"""Tests for pymididefs.status — MIDI 1.0 status bytes."""

import pymididefs.status


class TestChannelVoice:

	def test_values (self) -> None:
		"""Channel Voice status bytes are 0x80–0xE0 in steps of 0x10."""
		assert pymididefs.status.NOTE_OFF == 0x80
		assert pymididefs.status.NOTE_ON == 0x90
		assert pymididefs.status.POLY_AFTERTOUCH == 0xA0
		assert pymididefs.status.CONTROL_CHANGE == 0xB0
		assert pymididefs.status.PROGRAM_CHANGE == 0xC0
		assert pymididefs.status.CHANNEL_AFTERTOUCH == 0xD0
		assert pymididefs.status.PITCH_BEND == 0xE0

	def test_channel_voice_range (self) -> None:
		"""All Channel Voice messages have the upper nibble set and lower nibble clear."""
		messages = [
			pymididefs.status.NOTE_OFF,
			pymididefs.status.NOTE_ON,
			pymididefs.status.POLY_AFTERTOUCH,
			pymididefs.status.CONTROL_CHANGE,
			pymididefs.status.PROGRAM_CHANGE,
			pymididefs.status.CHANNEL_AFTERTOUCH,
			pymididefs.status.PITCH_BEND,
		]

		for msg in messages:
			assert 0x80 <= msg <= 0xE0
			assert msg & 0x0F == 0, f"0x{msg:02X} should have lower nibble = 0"


class TestSystemCommon:

	def test_sysex_bookends (self) -> None:
		"""SysEx starts at 0xF0 and ends at 0xF7."""
		assert pymididefs.status.SYSEX_START == 0xF0
		assert pymididefs.status.SYSEX_END == 0xF7

	def test_other_system_common (self) -> None:
		assert pymididefs.status.TIME_CODE == 0xF1
		assert pymididefs.status.SONG_POSITION == 0xF2
		assert pymididefs.status.SONG_SELECT == 0xF3
		assert pymididefs.status.TUNE_REQUEST == 0xF6


class TestSystemRealTime:

	def test_values (self) -> None:
		assert pymididefs.status.TIMING_CLOCK == 0xF8
		assert pymididefs.status.START == 0xFA
		assert pymididefs.status.CONTINUE == 0xFB
		assert pymididefs.status.STOP == 0xFC
		assert pymididefs.status.ACTIVE_SENSING == 0xFE
		assert pymididefs.status.SYSTEM_RESET == 0xFF

	def test_all_in_realtime_range (self) -> None:
		"""System Real-Time messages are 0xF8–0xFF."""
		realtime = [
			pymididefs.status.TIMING_CLOCK,
			pymididefs.status.START,
			pymididefs.status.CONTINUE,
			pymididefs.status.STOP,
			pymididefs.status.ACTIVE_SENSING,
			pymididefs.status.SYSTEM_RESET,
		]

		for msg in realtime:
			assert 0xF8 <= msg <= 0xFF
