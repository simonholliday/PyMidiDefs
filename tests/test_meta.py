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

	def test_rp019_text_event (self) -> None:
		"""Device Name sits in SMF's reserved text range, named by RP-019."""
		assert pymididefs.meta.DEVICE_NAME == 0x09

	def test_program_name_is_absent (self) -> None:
		"""0x08 stays out until somebody confirms it against RP-019.

		Pinned so it is a decision rather than an oversight: the value is
		believed to be Program Name and is corroborated by nothing to hand, so
		it is left out rather than shipped on a recollection.
		"""
		assert not hasattr(pymididefs.meta, "PROGRAM_NAME")

	def test_control_events (self) -> None:
		assert pymididefs.meta.CHANNEL_PREFIX == 0x20
		assert pymididefs.meta.END_OF_TRACK == 0x2F

	def test_midi_port (self) -> None:
		"""MIDI Port is obsolete and undocumented, and real files still carry it."""
		assert pymididefs.meta.MIDI_PORT == 0x21

	def test_timing_events (self) -> None:
		assert pymididefs.meta.TEMPO == 0x51
		assert pymididefs.meta.SMPTE_OFFSET == 0x54
		assert pymididefs.meta.TIME_SIGNATURE == 0x58
		assert pymididefs.meta.KEY_SIGNATURE == 0x59

	def test_sequencer_specific (self) -> None:
		assert pymididefs.meta.SEQUENCER_SPECIFIC == 0x7F

	def test_all_values_are_single_byte (self) -> None:
		"""Meta-event type bytes fit in a single byte (0x00–0x7F).

		Swept from the module rather than listed by hand, so a constant added
		later is covered without anyone remembering to add it here.
		"""
		events = {
			name: value
			for name, value in vars(pymididefs.meta).items()
			if name.isupper() and isinstance(value, int)
		}

		assert events, "no meta-event constants found"

		for name, value in events.items():
			assert 0x00 <= value <= 0x7F, f"{name} = {value:#x} is not a single byte"

	def test_no_duplicate_type_bytes (self) -> None:
		"""Each meta-event constant names a distinct type byte."""
		values = [
			value
			for name, value in vars(pymididefs.meta).items()
			if name.isupper() and isinstance(value, int)
		]

		assert len(values) == len(set(values))
