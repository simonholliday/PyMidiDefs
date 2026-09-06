"""Importing a MIDNAM file into an instrument definition.

MIDNAM is the one machine-readable description of an instrument that already
exists in quantity -- Ardour alone bundles several hundred -- so it is the
cheapest way to get a definition started.  It is not a way to get one finished.

**An import is an on-ramp, never an authority.**  MIDNAM carries the control
map and nothing else: no polyphony, no note range, no velocity response, no
aftertouch.  Everything in the ``midi`` and ``voice`` sections has to be added
by a person reading the manual.  And the control map itself can simply be
wrong -- the widely shared Moog Minitaur file gives a key-priority band the
manufacturer's own firmware addendum contradicts.

So an import is marked ``unverified`` in its own ``source`` line, the validator
keeps saying so, and it stays said until somebody replaces that line with the
manual and the page they checked it against.

Reading a MIDNAM needs no YAML parser; only loading the result back does.
"""

# Annotations here name sibling modules by their full path, which cannot be
# resolved while this package is still importing itself. Deferring them keeps
# the house import style intact; every runtime use below happens after import.
from __future__ import annotations

import pathlib
import re
import typing
import xml.etree.ElementTree

import pymididefs.instruments.definition
import pymididefs.instruments.validation


# Bare words YAML 1.1 reads as true or false rather than as text, so a name that
# is any of these has to be quoted on the way out or the file will not load.
YAML_KEYWORDS: typing.Final[frozenset[str]] = frozenset({
	"y", "yes", "n", "no", "true", "false", "on", "off", "null", "none", "~",
})


def _local (tag: str) -> str:

	"""The tag name without whatever namespace the document happened to use."""

	return tag.rsplit("}", 1)[-1]


def _find_all (root: xml.etree.ElementTree.Element, name: str) -> list[xml.etree.ElementTree.Element]:

	"""Every element with this tag name, at any depth and in any namespace."""

	return [element for element in root.iter() if _local(element.tag) == name]


def _text_of (root: xml.etree.ElementTree.Element, name: str) -> str | None:

	"""The text of the first element with this tag name, if there is one."""

	for element in _find_all(root, name):
		if element.text and element.text.strip():
			return element.text.strip()

	return None


def _slug (text: str, prefix: str) -> str:

	"""Turn a human label into an addressable name.

	Names must start with a letter, so anything beginning with a digit takes the
	given prefix rather than being dropped -- "16' Octave" is a real control and
	losing it would be worse than renaming it.
	"""

	cleaned = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")

	if not cleaned:
		return ""

	return cleaned if cleaned[0].isalpha() else f"{prefix}_{cleaned}"


def _unique (name: str, taken: typing.Container[str]) -> str:

	"""A name not already used, by numbering the repeats.

	MIDNAM does not require control names to be distinct, and two controls
	quietly becoming one is the kind of loss nobody notices.
	"""

	if name not in taken:
		return name

	for suffix in range(2, 1000):
		candidate = f"{name}_{suffix}"

		if candidate not in taken:
			return candidate

	return name


def _value_lists (root: xml.etree.ElementTree.Element) -> dict[str, dict[str, int]]:

	"""Every named list of values in the document, keyed by its MIDNAM name.

	A ``Value``'s ``Number`` is the lowest of its band, running to the next entry
	minus one -- the same convention a definition file uses, so nothing has to be
	converted here.
	"""

	lists: dict[str, dict[str, int]] = {}

	for element in _find_all(root, "ValueNameList"):
		name = element.get("Name")

		if not name:
			continue

		values: dict[str, int] = {}

		for value in _find_all(element, "Value"):
			label = value.get("Name") or ""
			number = value.get("Number")

			if number is None:
				continue

			try:
				low = int(number)
			except ValueError:
				continue

			key = _unique(_slug(label, "value") or f"value_{low}", values)
			values[key] = low

		if values:
			lists[name] = values

	return lists


def read (
	text: str,
	*,
	source: str,
	path: pathlib.Path | None = None,
) -> pymididefs.instruments.definition.Definition:

	"""Read a MIDNAM document into a definition, marked unverified.

	Raises ``DefinitionError`` if the document is not parseable XML, or carries
	no model name -- without one there is nothing to file the result under.
	"""

	try:
		root = xml.etree.ElementTree.fromstring(text)
	except xml.etree.ElementTree.ParseError as broken:
		raise pymididefs.instruments.validation.DefinitionError(
			f"{source}: not valid XML: {broken}") from broken

	name = _text_of(root, "Model")

	if not name:
		raise pymididefs.instruments.validation.DefinitionError(
			f"{source}: no <Model> element, so there is no instrument to name")

	warnings: list[str] = []
	named_values = _value_lists(root)
	controls: dict[str, pymididefs.instruments.definition.Control] = {}

	for element in _find_all(root, "Control"):
		number = element.get("Number")
		label = element.get("Name") or ""

		if number is None:
			continue

		try:
			cc = int(number)
		except ValueError:
			continue

		if not 0 <= cc <= 127:
			warnings.append(f"{source}: control {label!r} has number {cc}, which is not 0-127 — skipped")
			continue

		key = _unique(_slug(label, "control") or f"control_{cc}", controls)
		extent = (0, 127)
		values: dict[str, int] = {}

		for holder in _find_all(element, "Values"):
			low, high = holder.get("Min"), holder.get("Max")

			if low is not None and high is not None:
				try:
					extent = (int(low), int(high))
				except ValueError:
					pass

			listed = holder.get("ValueNameList")

			if listed and listed in named_values:
				values = named_values[listed]

		if element.get("Type") == "14bit":
			warnings.append(
				f"{source}: {key} is marked 14bit — MIDNAM does not pair the coarse "
				f"number with its fine one, so `lsb` has to be added by hand"
			)

		controls[key] = pymididefs.instruments.definition.Control(
			name   = key,
			label  = label or key.replace("_", " "),
			cc     = cc,
			values = {inner: low for inner, low in values.items() if extent[0] <= low <= extent[1]},
			range  = extent,
		)

	voices: dict[str, int] = {}

	for element in _find_all(root, "Note"):
		number = element.get("Number")
		label = element.get("Name") or ""

		if number is None:
			continue

		try:
			note = int(number)
		except ValueError:
			continue

		if not 0 <= note <= 127:
			continue

		voices[_unique(_slug(label, "voice") or f"voice_{note}", voices)] = note

	presets = len(_find_all(root, "Patch")) or None

	warnings.append(
		f"{source}: everything in `midi` and `voice` has to be added by hand — MIDNAM "
		f"carries no polyphony, note range, velocity response or aftertouch"
	)

	return pymididefs.instruments.definition.Definition(
		version = pymididefs.instruments.validation.VERSION,
		model   = pymididefs.instruments.definition.Model(
			name         = name,
			manufacturer = _text_of(root, "Manufacturer"),
		),
		source = f"imported from {pathlib.Path(source).name}, unverified",
		midi = pymididefs.instruments.definition.Midi(
			program_change = None if presets is None
				else pymididefs.instruments.definition.ProgramChange(presets = presets),
		),
		voice = pymididefs.instruments.definition.Voice(
			addressing = "voices" if voices else None,
			voices     = voices,
		),
		controls = controls,
		path     = path,
		warnings = tuple(warnings),
	)


def read_file (path: pathlib.Path | str) -> pymididefs.instruments.definition.Definition:

	"""Read one MIDNAM file into a definition, marked unverified."""

	file = pathlib.Path(path)

	return read(file.read_text(encoding = "utf-8", errors = "replace"), source = str(file), path = file)


def suggested_stem (definition: pymididefs.instruments.definition.Definition) -> str:

	"""What to call the file this definition should be saved as."""

	maker = _slug(definition.model.manufacturer or "", "m")
	model = _slug(definition.model.name, "m")

	return f"{maker}_{model}".strip("_") if maker else model


def _key (name: str) -> str:

	"""A mapping key, quoted if YAML would read it as something other than text.

	``off`` and ``on`` are the ones that actually happen: they are band names on
	every switch in the world, and YAML 1.1 turns them into false and true.
	"""

	return f'"{name}"' if name.lower() in YAML_KEYWORDS else name


def _scalar (text: str) -> str:

	"""A text value, always quoted, so nothing in a label can change its meaning."""

	escaped = text.replace("\\", "\\\\").replace('"', '\\"')

	return f'"{escaped}"'


def to_yaml (definition: pymididefs.instruments.definition.Definition) -> str:

	"""Write a definition out as the draft file an import lands.

	Deliberately plain: no dependency on a YAML writer, and an ordering that
	matches how the format is documented, because the next thing that happens to
	this file is a person editing it.
	"""

	lines: list[str] = []

	lines.append("# A DRAFT. Nobody has checked this against a manual yet.")
	lines.append("#")
	lines.append("# MIDNAM carries a control map and nothing else. Everything below in `midi`")
	lines.append("# and `voice` has to be filled in by hand, and every number here is worth")
	lines.append("# checking: the most widely shared MIDNAM for a common synth disagrees with")
	lines.append("# its own manufacturer's firmware addendum.")
	lines.append("#")
	lines.append("# Replace the `source` line with the manual and page you checked, and this")
	lines.append("# stops being a draft.")

	for warning in definition.warnings:
		lines.append(f"#   - {warning.split(': ', 1)[-1]}")

	lines.append("")
	lines.append(f"definition: {definition.version}")
	lines.append("")
	lines.append("model:")

	if definition.model.manufacturer:
		lines.append(f"  manufacturer: {_scalar(definition.model.manufacturer)}")

	lines.append(f"  name: {_scalar(definition.model.name)}")
	lines.append("")

	if definition.source:
		lines.append(f"source: {_scalar(definition.source)}")
		lines.append("")

	if definition.midi.program_change and definition.midi.program_change.presets:
		lines.append("midi:")
		lines.append("  program_change:")
		lines.append(f"    presets: {definition.midi.program_change.presets}")
		lines.append("")

	if definition.voice.addressing or definition.voice.voices:
		lines.append("voice:")

		if definition.voice.addressing:
			lines.append(f"  addressing: {definition.voice.addressing}")

		if definition.voice.voices:
			lines.append("  voices:")

			for name, note in definition.voice.voices.items():
				lines.append(f"    {_key(name)}: {note}")

		lines.append("")

	if definition.controls:
		lines.append("controls:")

		for control in definition.controls.values():
			lines.append("")
			lines.append(f"  {_key(control.name)}:")
			lines.append(f"    label: {_scalar(control.label)}")
			lines.append(f"    cc: {control.cc}")

			if control.range != (0, 127):
				lines.append(f"    range: [{control.range[0]}, {control.range[1]}]")

			if control.values:
				pairs = ", ".join(f"{_key(name)}: {low}" for name, low in control.values.items())
				lines.append(f"    values: {{{pairs}}}")

	return "\n".join(lines).rstrip() + "\n"
