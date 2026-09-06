"""Tests for pymididefs.instruments.midnam — starting a definition from a MIDNAM.

Deliberately not skipped when the YAML extra is absent: reading a MIDNAM needs
no YAML parser, and only the round-trip test below does.
"""

import pathlib

import pytest

import pymididefs.instruments.midnam
import pymididefs.instruments.validation


MINITAUR = """<?xml version="1.0" encoding="UTF-8"?>
<MIDINameDocument>
  <MasterDeviceNames>
    <Manufacturer>Moog Music</Manufacturer>
    <Model>Minitaur</Model>
    <ChannelNameSet Name="Names">
      <PatchBank Name="Presets">
        <PatchNameList>
          <Patch Number="1" Name="Bass" ProgramChange="0"/>
          <Patch Number="2" Name="Lead" ProgramChange="1"/>
        </PatchNameList>
      </PatchBank>
    </ChannelNameSet>
    <ValueNameList Name="Glide Type">
      <Value Number="0" Name="LCR"/>
      <Value Number="43" Name="LCT"/>
      <Value Number="85" Name="Exponential"/>
    </ValueNameList>
    <ValueNameList Name="Switch">
      <Value Number="0" Name="Off"/>
      <Value Number="64" Name="On"/>
    </ValueNameList>
    <ControlNameList Name="Controls">
      <Control Type="7bit" Number="5" Name="Glide Rate"/>
      <Control Type="7bit" Number="92" Name="Glide Type">
        <Values Min="0" Max="127" ValueNameList="Glide Type"/>
      </Control>
      <Control Type="7bit" Number="65" Name="Glide Switch">
        <Values Min="0" Max="127" ValueNameList="Switch"/>
      </Control>
      <Control Type="14bit" Number="19" Name="Cutoff"/>
      <Control Type="7bit" Number="3" Name="Glide Rate"/>
      <Control Type="7bit" Number="900" Name="Nonsense"/>
      <Control Type="7bit" Number="70" Name="16' Octave"/>
    </ControlNameList>
    <NoteNameList Name="Voices">
      <Note Number="36" Name="Kick"/>
      <Note Number="38" Name="Snare"/>
    </NoteNameList>
  </MasterDeviceNames>
</MIDINameDocument>
"""


class TestReading:

	def test_identity_comes_across (self) -> None:
		definition = pymididefs.instruments.midnam.read(MINITAUR, source = "Moog_Minitaur.midnam")

		assert definition.model.name == "Minitaur"
		assert definition.model.manufacturer == "Moog Music"
		assert pymididefs.instruments.midnam.suggested_stem(definition) == "moog_music_minitaur"

	def test_an_import_is_marked_unverified (self) -> None:
		"""An import is an on-ramp, never an authority, and says so about itself."""
		definition = pymididefs.instruments.midnam.read(MINITAUR, source = "Moog_Minitaur.midnam")

		assert definition.source == "imported from Moog_Minitaur.midnam, unverified"
		assert definition.is_unverified

	def test_bands_arrive_verbatim (self) -> None:
		"""A MIDNAM Value Number is the low end of its band, as a definition wants."""
		definition = pymididefs.instruments.midnam.read(MINITAUR, source = "x.midnam")
		glide = definition.controls["glide_type"]

		assert glide.cc == 92
		assert glide.values == {"lcr": 0, "lct": 43, "exponential": 85}
		assert glide.band("lct") == (43, 84)

	def test_a_14_bit_control_says_its_pair_is_missing (self) -> None:
		"""MIDNAM never pairs the coarse number with the fine one."""
		definition = pymididefs.instruments.midnam.read(MINITAUR, source = "x.midnam")

		assert definition.controls["cutoff"].lsb is None
		assert any("14bit" in warning for warning in definition.warnings)

	def test_everything_a_midnam_cannot_carry_is_named (self) -> None:
		"""No polyphony, no note range, no velocity, no aftertouch — say so once."""
		definition = pymididefs.instruments.midnam.read(MINITAUR, source = "x.midnam")

		assert any("added by hand" in warning for warning in definition.warnings)
		assert definition.voice.polyphony is None
		assert definition.voice.note_range is None

	def test_repeated_control_names_do_not_collapse (self) -> None:
		"""Two controls quietly becoming one is a loss nobody would notice."""
		definition = pymididefs.instruments.midnam.read(MINITAUR, source = "x.midnam")

		assert definition.controls["glide_rate"].cc == 5
		assert definition.controls["glide_rate_2"].cc == 3

	def test_a_name_starting_with_a_digit_is_kept_not_dropped (self) -> None:
		"""16' Octave is a real control, and renaming beats losing it."""
		definition = pymididefs.instruments.midnam.read(MINITAUR, source = "x.midnam")
		matching = [name for name in definition.controls if name.endswith("16_octave")]

		assert matching, f"the octave control was dropped: {list(definition.controls)}"

	def test_an_impossible_control_number_is_skipped_with_a_warning (self) -> None:
		definition = pymididefs.instruments.midnam.read(MINITAUR, source = "x.midnam")

		assert all(control.cc is not None and control.cc <= 127
			for control in definition.controls.values())
		assert any("not 0-127" in warning for warning in definition.warnings)

	def test_notes_become_voices (self) -> None:
		definition = pymididefs.instruments.midnam.read(MINITAUR, source = "x.midnam")

		assert definition.voice.addressing == "voices"
		assert definition.voice.voices == {"kick": 36, "snare": 38}

	def test_patches_are_counted_as_presets (self) -> None:
		definition = pymididefs.instruments.midnam.read(MINITAUR, source = "x.midnam")

		assert definition.midi.program_change is not None
		assert definition.midi.program_change.presets == 2

	def test_a_namespaced_document_still_reads (self) -> None:
		"""Some MIDNAM files carry a namespace and most do not."""
		namespaced = MINITAUR.replace(
			"<MIDINameDocument>", '<MIDINameDocument xmlns="http://www.midi.org/dtds">')
		definition = pymididefs.instruments.midnam.read(namespaced, source = "x.midnam")

		assert definition.model.name == "Minitaur"


class TestRefusals:

	def test_broken_xml_is_refused (self) -> None:
		with pytest.raises(pymididefs.instruments.validation.DefinitionError) as raised:
			pymididefs.instruments.midnam.read("<not xml", source = "x.midnam")

		assert "not valid XML" in str(raised.value)

	def test_a_document_with_no_model_is_refused (self) -> None:
		"""Without a model name there is nothing to file the result under."""
		with pytest.raises(pymididefs.instruments.validation.DefinitionError) as raised:
			pymididefs.instruments.midnam.read(
				"<MIDINameDocument><Manufacturer>X</Manufacturer></MIDINameDocument>",
				source = "x.midnam")

		assert "no <Model>" in str(raised.value)


class TestDraftFile:

	def test_the_draft_it_writes_loads_back (self, tmp_path: pathlib.Path) -> None:
		"""An importer that emits a file this package cannot read is worth nothing."""
		pytest.importorskip("yaml", reason = "loading the draft back needs the extra")

		import pymididefs.instruments

		definition = pymididefs.instruments.midnam.read(MINITAUR, source = "Moog_Minitaur.midnam")
		path = tmp_path / f"{pymididefs.instruments.midnam.suggested_stem(definition)}.yaml"
		path.write_text(pymididefs.instruments.midnam.to_yaml(definition), encoding = "utf-8")

		reloaded = pymididefs.instruments.load_file(path)

		assert reloaded.model.name == "Minitaur"
		assert reloaded.controls["glide_type"].values == {"lcr": 0, "lct": 43, "exponential": 85}
		assert reloaded.is_unverified

	def test_off_and_on_are_quoted_on_the_way_out (self) -> None:
		"""Otherwise YAML reads them back as false and true, and the file will not load.

		Every switch in the world has bands called off and on, so an emitter that
		does not quote them writes files that cannot be read.
		"""
		definition = pymididefs.instruments.midnam.read(MINITAUR, source = "x.midnam")
		text = pymididefs.instruments.midnam.to_yaml(definition)

		assert '"off": 0' in text
		assert '"on": 64' in text

	def test_the_draft_says_it_is_a_draft (self) -> None:
		definition = pymididefs.instruments.midnam.read(MINITAUR, source = "x.midnam")
		text = pymididefs.instruments.midnam.to_yaml(definition)

		assert text.startswith("# A DRAFT.")
		assert "unverified" in text
