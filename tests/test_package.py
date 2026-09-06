"""Tests for invariants that hold across the whole package, not within one module."""

import importlib
import importlib.metadata
import pkgutil
import subprocess
import sys
import typing

import pytest

import pymididefs


def _modules () -> list[str]:

	"""Every module in the package, derived rather than listed.

	Derived on purpose: the previous version of this file named nine modules by
	hand, which worked until there were ten. A guard that silently stops
	covering new code is worse than no guard, because it is trusted.
	"""

	found = [
		info.name
		for info in pkgutil.walk_packages(pymididefs.__path__, prefix = "pymididefs.")
	]

	return [pymididefs.__name__, *found]


def _int_constants (module_name: str) -> dict[str, int]:

	"""Return the public integer constants a module defines, by name."""

	module = importlib.import_module(module_name)

	return {
		name: value
		for name, value in vars(module).items()
		if name.isupper() and isinstance(value, int) and not isinstance(value, bool)
	}


class TestNoNameCollisions:

	def test_the_package_has_more_than_one_module (self) -> None:
		"""If the walk ever returns nothing, the collision test below proves nothing."""
		assert len(_modules()) > 5

	def test_no_constant_is_defined_in_two_modules (self) -> None:
		"""One name must mean one thing across the package.

		No module declares ``__all__``, so a caller who star-imports two of them
		gets whichever came last, silently and in import order. That is only
		survivable while no name appears twice — a UMP opcode is a nibble and a
		status byte is a whole byte, so the wrong one is a plausible-looking
		number rather than an error.
		"""
		owners: dict[str, list[str]] = {}

		for module_name in _modules():
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


class TestBaseInstall:

	"""The base install pulls in nothing, and nothing else here can check that.

	Instrument definitions are read with a YAML parser that ships as an optional
	extra. The property this protects is that ``import pymididefs`` still works,
	and still pulls in nothing, for somebody who installed the base package —
	so these tests are the whole verification, and they run either way.
	"""

	def test_the_package_declares_no_runtime_dependencies (self) -> None:
		"""Everything declared is behind an extra, never required outright."""
		required = importlib.metadata.requires("pymididefs") or []
		unconditional = [need for need in required if "extra ==" not in need]

		assert unconditional == [], f"these would be installed for everybody: {unconditional}"

	def test_importing_the_package_never_needs_a_yaml_parser (self) -> None:
		"""Proved in a fresh interpreter with the parser made unimportable.

		In-process this would only prove that something else had already
		imported it.
		"""
		code = (
			"import sys; sys.modules['yaml'] = None; "
			"import pymididefs, pymididefs.instruments; "
			"print(pymididefs.instruments.load.__name__)"
		)
		finished = subprocess.run(
			[sys.executable, "-c", code], capture_output = True, text = True, check = False)

		assert finished.returncode == 0, finished.stderr
		assert finished.stdout.strip() == "load"

	def test_reading_a_definition_without_one_names_the_extra (
		self, monkeypatch: pytest.MonkeyPatch,
	) -> None:
		"""The error has to say what to install, because that is the whole fix."""
		import pymididefs.instruments

		monkeypatch.setitem(sys.modules, "yaml", typing.cast(typing.Any, None))

		with pytest.raises(ImportError) as raised:
			pymididefs.instruments.parse("definition: 1", source = "x.yaml")

		assert "pip install pymididefs[instruments]" in str(raised.value)
