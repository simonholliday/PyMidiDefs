"""Tests for invariants that hold across the whole package, not within one module."""

import importlib
import typing

import pymididefs


MODULES: typing.Final[tuple[str, ...]] = (
	"notes", "cc", "rpn", "drums", "gm", "status", "meta", "ump", "ci",
)


def _int_constants (module_name: str) -> dict[str, int]:

	"""Return the public integer constants a module defines, by name."""

	module = importlib.import_module(f"pymididefs.{module_name}")

	return {
		name: value
		for name, value in vars(module).items()
		if name.isupper() and isinstance(value, int)
	}


class TestNoNameCollisions:

	def test_no_constant_is_defined_in_two_modules (self) -> None:
		"""One name must mean one thing across the package.

		No module declares ``__all__``, so a caller who star-imports two of them
		gets whichever came last, silently and in import order.  That is only
		survivable while no name appears twice — a UMP opcode is a nibble and a
		status byte is a whole byte, so the wrong one is a plausible-looking
		number rather than an error.
		"""
		owners: dict[str, list[str]] = {}

		for module_name in MODULES:
			for name in _int_constants(module_name):
				owners.setdefault(name, []).append(module_name)

		collisions = {name: mods for name, mods in owners.items() if len(mods) > 1}

		assert collisions == {}, f"names defined in more than one module: {collisions}"


class TestPackageSurface:

	def test_convenience_reexports_are_the_real_functions (self) -> None:
		"""The two names re-exported at package level are not copies."""
		assert pymididefs.note_to_name is pymididefs.notes.note_to_name
		assert pymididefs.name_to_note is pymididefs.notes.name_to_note

	def test_version_is_a_string (self) -> None:
		"""__version__ resolves whether or not the package was pip-installed."""
		assert isinstance(pymididefs.__version__, str)
		assert pymididefs.__version__
