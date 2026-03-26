"""Tests for pymididefs.meta — Standard MIDI File meta-event type bytes."""

import pymididefs.meta


class TestMetaEvents:

	def test_text_events (self) -> None:
		"""Text-related meta-events are 0x01–0x07."""
		assert pymididefs.meta.TEXT == 0x01
		assert pymididefs.meta.COPYRIGHT == 0x02
		assert pymididefs.meta.TRACK_NAME == 0x03
		assert pymididefs.meta.INSTRUMENT_NAME == 0x04
		assert pymididefs.meta.LYRIC == 0x05
		assert pymididefs.meta.MARKER == 0x06
		assert pymididefs.meta.CUE_POINT == 0x07

	def test_sequence_number (self) -> None:
		assert pymididefs.meta.SEQUENCE_NUMBER == 0x00

	def test_control_events (self) -> None:
		assert pymididefs.meta.CHANNEL_PREFIX == 0x20
		assert pymididefs.meta.END_OF_TRACK == 0x2F

	def test_timing_events (self) -> None:
		assert pymididefs.meta.TEMPO == 0x51
		assert pymididefs.meta.SMPTE_OFFSET == 0x54
		assert pymididefs.meta.TIME_SIGNATURE == 0x58
		assert pymididefs.meta.KEY_SIGNATURE == 0x59

	def test_sequencer_specific (self) -> None:
		assert pymididefs.meta.SEQUENCER_SPECIFIC == 0x7F

	def test_all_values_are_single_byte (self) -> None:
		"""Meta-event type bytes fit in a single byte (0x00–0x7F)."""
		events = [
			pymididefs.meta.SEQUENCE_NUMBER,
			pymididefs.meta.TEXT,
			pymididefs.meta.COPYRIGHT,
			pymididefs.meta.TRACK_NAME,
			pymididefs.meta.INSTRUMENT_NAME,
			pymididefs.meta.LYRIC,
			pymididefs.meta.MARKER,
			pymididefs.meta.CUE_POINT,
			pymididefs.meta.CHANNEL_PREFIX,
			pymididefs.meta.END_OF_TRACK,
			pymididefs.meta.TEMPO,
			pymididefs.meta.SMPTE_OFFSET,
			pymididefs.meta.TIME_SIGNATURE,
			pymididefs.meta.KEY_SIGNATURE,
			pymididefs.meta.SEQUENCER_SPECIFIC,
		]

		for event in events:
			assert 0x00 <= event <= 0x7F
