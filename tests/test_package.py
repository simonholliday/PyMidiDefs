"""Tests for invariants that hold across the whole package, not within one module."""

import importlib
import importlib.metadata
import pathlib
import pkgutil
import types

import pytest

import pymididefs


def _modules () -> list[str]:

	"""Every module in the package, derived rather than listed.

	Derived on purpose: an earlier version of this file named nine modules by
	hand, which worked until there were ten. A guard that silently stops
	covering new code is worse than no guard, because it is trusted.
	"""

	found = [
		info.name
		for info in pkgutil.walk_packages(pymididefs.__path__, prefix = "pymididefs.")
	]

	return [pymididefs.__name__, *found]


def _defined_names (module: types.ModuleType) -> set[str]:

	"""Return the public names a module defines, which is never a module.

	``import typing`` leaves ``typing`` in a module's namespace, where a
	star-import would hand it over. A submodule is the same case: ``cc``
	appears on the package as soon as anything imports ``pymididefs.cc``, so
	which submodules are bound there depends on what ran first. A module is
	reached by importing it, never by star-importing its parent.
	"""

	return {
		name
		for name, value in vars(module).items()
		if not name.startswith("_") and not isinstance(value, types.ModuleType)
	}


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

		Every module declares ``__all__``, so a star-import brings its own
		definitions and nothing else. Two of them star-imported together still
		collide on a shared name, though: the caller gets whichever came last,
		silently and in import order. A UMP opcode is a nibble and a status
		byte is a whole byte, so the wrong one is a plausible-looking number
		rather than an error.
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
		"""__version__ is always a non-empty string."""
		assert isinstance(pymididefs.__version__, str)
		assert pymididefs.__version__


class TestNoDependencies:

	"""Installing this package installs nothing else.

	A constants package that pulled in a MIDI library, or anything at all, would
	be unusable by somebody who had already chosen a different one. The README
	promises this, and nothing but this test checks it.
	"""

	def test_the_package_declares_no_runtime_dependencies (self) -> None:
		"""Everything declared is behind an extra, never required outright."""
		required = importlib.metadata.requires("pymididefs") or []
		unconditional = [need for need in required if "extra ==" not in need]

		assert unconditional == [], f"these would be installed for everybody: {unconditional}"

	def test_pyproject_declares_no_runtime_dependencies (self) -> None:
		"""The next build's source agrees, whatever the installed metadata says.

		Installed metadata can be stale: an editable install keeps what was true
		when it was made, so the test above can pass against an old copy.
		pyproject.toml is what the next build reads.
		"""
		tomllib = pytest.importorskip("tomllib")
		pyproject = pathlib.Path(__file__).resolve().parent.parent / "pyproject.toml"
		project = tomllib.loads(pyproject.read_text())["project"]

		assert project.get("dependencies", []) == []


class TestPublicNames:

	"""Every module declares ``__all__``, and it says what that module defines.

	Star-importing a constants module is a real use rather than a hypothetical
	one: Subsequence re-exports four of these through shims written that way.
	Without ``__all__`` such an import also hands over whatever the module
	imported, and a constant added here lands in the consumer's namespace with
	nothing in the diff to show it, where it can shadow a name they define
	themselves.

	The lists are written out rather than computed, so that adding a public name
	changes ``__all__`` in the same diff and a reader sees the surface move. The
	tests below are what stop a written list falling behind the module it
	describes, which a list in a docstring here once did.
	"""

	def test_every_module_declares_all (self) -> None:
		"""Nothing is left to the default, which exports whatever is lying about."""
		missing = [
			module_name
			for module_name in _modules()
			if not hasattr(importlib.import_module(module_name), "__all__")
		]

		assert missing == [], f"these modules declare no __all__: {missing}"

	def test_every_name_in_all_is_defined (self) -> None:
		"""A name listed but not defined breaks the star-import for everybody."""
		for module_name in _modules():
			module = importlib.import_module(module_name)
			absent = [name for name in module.__all__ if not hasattr(module, name)]

			assert absent == [], f"{module_name} lists names it does not define: {absent}"

	def test_all_hands_over_nothing_the_module_imported (self) -> None:
		"""``typing`` is not part of this package's public surface."""
		for module_name in _modules():
			module = importlib.import_module(module_name)
			foreign = [
				name
				for name in module.__all__
				if isinstance(getattr(module, name), types.ModuleType)
			]

			assert foreign == [], f"{module_name} would hand over: {foreign}"

	def test_all_lists_every_public_definition (self) -> None:
		"""The written list cannot fall behind the module without this failing.

		This is the test that earns the written-out lists. A constant added to a
		module and not added to its ``__all__`` would otherwise go unnoticed:
		the module still works, the star-import simply stops carrying it.
		"""
		for module_name in _modules():
			module = importlib.import_module(module_name)
			defined = _defined_names(module)

			assert set(module.__all__) == defined, (
				f"{module_name}: __all__ omits {sorted(defined - set(module.__all__))}, "
				f"and names {sorted(set(module.__all__) - defined)} that it does not define"
			)
