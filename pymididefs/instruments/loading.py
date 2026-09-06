"""Finding an instrument definition and reading it.

A reader takes a **search path** and returns the first match, so a definition
sitting beside the piece always beats one in a library, and a library one always
beats the set that ships here.  That is the whole answer to "how do I add my own
synth": drop a file.  No index to edit, no registration, no pull request, and
what you write always wins over what we shipped.

The YAML parser is an optional extra.  It is imported inside the function that
parses rather than at the top of this module, so that ``import pymididefs`` and
``import pymididefs.instruments`` both keep working for somebody who installed
the base package, and only *reading a file* asks for anything.
"""

# Annotations here name sibling modules by their full path, which cannot be
# resolved while this package is still importing itself. Deferring them keeps
# the house import style intact; every runtime use below happens after import.
from __future__ import annotations

import os
import pathlib
import sys
import typing

import pymididefs.instruments.definition
import pymididefs.instruments.validation


SUFFIX: typing.Final[str] = ".yaml"

# Where the definitions that ship with this package live.
BUNDLED: typing.Final[pathlib.Path] = pathlib.Path(__file__).parent / "corpus"

_EXTRA: typing.Final[str] = (
	"Reading an instrument definition needs a YAML parser, which the base "
	"install deliberately does not pull in.\n"
	"Install it with:  pip install pymididefs[instruments]"
)


class DefinitionNotFound(LookupError):

	"""No definition of that name was anywhere on the search path."""


def user_library () -> pathlib.Path:

	"""Where this person's own definitions live, by their platform's convention.

	One place per person, so a definition written once is found by every tool
	they run.  Nothing has to exist here; it is simply looked in.
	"""

	if sys.platform == "win32":
		base = pathlib.Path(os.environ.get("APPDATA", pathlib.Path.home() / "AppData" / "Roaming"))
		return base / "pymididefs" / "instruments"

	if sys.platform == "darwin":
		return pathlib.Path.home() / "Library" / "Application Support" / "pymididefs" / "instruments"

	base = pathlib.Path(os.environ.get("XDG_DATA_HOME", pathlib.Path.home() / ".local" / "share"))

	return base / "pymididefs" / "instruments"


def search_path (beside: pathlib.Path | None = None) -> tuple[pathlib.Path, ...]:

	"""The places a definition is looked for, nearest first.

	``beside`` is the directory holding the piece being worked on; its
	``instruments/`` subdirectory is searched before anything else.  These are
	recommendations rather than requirements — pass your own path to ``load``
	and none of this applies.
	"""

	here = (beside or pathlib.Path.cwd()) / "instruments"

	return (here, user_library(), BUNDLED)


def available (search: typing.Sequence[pathlib.Path] | None = None) -> list[str]:

	"""The names of every definition on the search path, nearest first, once each."""

	found: list[str] = []

	for directory in (search if search is not None else search_path()):
		if not directory.is_dir():
			continue

		for candidate in sorted(directory.glob(f"*{SUFFIX}")):
			if candidate.stem not in found:
				found.append(candidate.stem)

	return found


def locate (name: str, search: typing.Sequence[pathlib.Path] | None = None) -> pathlib.Path:

	"""The file a name resolves to, first match winning.

	Raises ``DefinitionNotFound``, naming every place that was looked in — a
	"not found" that does not say where it looked is a riddle.
	"""

	directories = tuple(search if search is not None else search_path())

	for directory in directories:
		candidate = directory / f"{name}{SUFFIX}"

		if candidate.is_file():
			return candidate

	looked = "\n".join(f"  {directory}" for directory in directories)

	raise DefinitionNotFound(f"No definition called {name!r}. Looked in:\n{looked}")


def parse (text: str, *, source: str, path: pathlib.Path | None = None) -> pymididefs.instruments.definition.Definition:

	"""Read a definition from YAML text that is already in hand.

	Raises ``ImportError`` naming the extra when no YAML parser is installed,
	because that is a thing the person running this can fix and the message
	should tell them how.
	"""

	try:
		import yaml
	except ImportError as absent:
		raise ImportError(_EXTRA) from absent

	try:
		document = yaml.safe_load(text)
	except yaml.YAMLError as broken:
		raise pymididefs.instruments.validation.DefinitionError(f"{source}: not valid YAML: {broken}") from broken

	return pymididefs.instruments.validation.build(document, source = source, path = path)


def load_file (path: pathlib.Path | str) -> pymididefs.instruments.definition.Definition:

	"""Read one definition from a named file."""

	file = pathlib.Path(path)

	pymididefs.instruments.validation.check_stem(file.stem, str(file))

	return parse(file.read_text(encoding = "utf-8"), source = str(file), path = file)


def load (
	name: str,
	search: typing.Sequence[pathlib.Path] | None = None,
) -> pymididefs.instruments.definition.Definition:

	"""Find a definition by name and read it, nearest copy winning."""

	return load_file(locate(name, search))
