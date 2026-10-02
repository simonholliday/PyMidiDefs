"""Every worked example in the package and the README is run, not just written.

A reference library's examples are read as authority, so one that was never
executed is the same hazard as cc.py's omission list, which looked precise and
was wrong (#1489). There are two kinds here and both are checked:

- ``>>>`` examples, which :mod:`doctest` runs;
- ``expression  # value`` lines, in the README's Python blocks and in the ``::``
  literal blocks of the module docstrings. These are not doctests and nothing
  ran them, so a printed value could go stale with the suite green.

They run from a test rather than from ``--doctest-modules`` in the pytest
configuration. Collecting the package directory as well as the tests breaks how
a packager invokes pytest: ``--import-mode=append`` against an installed wheel
stops on import-file-mismatch errors, ``--import-mode=importlib`` quietly tests
the installed copy rather than the checkout, ``-p no:doctest`` becomes a usage
error, and pytest before 7.2 aborts outright if the source directory is not
beside the tests. A test runs the same examples however pytest is called.
"""

import doctest
import importlib
import pathlib
import pkgutil
import re
import types

import pytest

import pymididefs


# `pymididefs.cc.SUSTAIN_PEDAL    # 64`, where the comment may carry a note
# after the value: `# 0x9   (a UMP opcode, not the 0x90 status byte)`.
EXAMPLE = re.compile(
	r"^(pymididefs\.[A-Za-z_0-9.\[\]\"'(), -]+?)"
	r"\s+#\s*(0x[0-9A-Fa-f]+|\d+|True|False|\"[^\"]*\"|\([0-9, ]+\))"
)


def _modules () -> list[types.ModuleType]:

	"""Every module in the package, derived rather than listed."""

	found = [
		importlib.import_module(info.name)
		for info in pkgutil.walk_packages(pymididefs.__path__, prefix = "pymididefs.")
	]

	return [pymididefs, *found]


def _examples_in (text: str, python_only: bool = False) -> list[tuple[str, str]]:

	"""Return every ``expression  # value`` pair in text.

	With python_only, only lines inside a ```python fence are read, which is
	what the README needs; a docstring has no fences and is read whole.
	"""

	inside = not python_only
	found: list[tuple[str, str]] = []

	for line in text.splitlines():
		if python_only and line.startswith("```"):
			inside = line.startswith("```python")
			continue

		if inside:
			match = EXAMPLE.match(line.strip())

			if match:
				found.append((match.group(1).strip(), match.group(2)))

	return found


def _namespace () -> dict[str, object]:

	"""A namespace with the whole package imported, to evaluate examples in."""

	namespace: dict[str, object] = {}

	for module in _modules():
		exec(f"import {module.__name__}", namespace)   # noqa: S102

	return namespace


def _check (examples: list[tuple[str, str]], where: str) -> None:

	"""Evaluate each example and assert it is what it claims to be."""

	namespace = _namespace()
	wrong: list[str] = []

	for expression, expected in examples:
		got = eval(expression, namespace)      # noqa: S307
		want = eval(expected, namespace)       # noqa: S307

		if got != want:
			wrong.append(f"{expression} is {got!r}, {where} says {expected}")

	assert wrong == [], f"{where} examples that do not hold: " + "; ".join(wrong)


def _readme () -> pathlib.Path:

	"""The README beside the package, or skip if this is an installed copy."""

	readme = pathlib.Path(__file__).resolve().parent.parent / "README.md"

	if not readme.is_file():
		pytest.skip("README.md is not beside the tests")

	return readme


class TestDoctestExamples:

	def test_every_doctest_example_runs (self) -> None:
		"""Each ``>>>`` example in the package produces what it claims."""
		failed: list[str] = []

		for module in _modules():
			results = doctest.testmod(module, verbose = False, report = False)

			if results.failed:
				failed.append(f"{module.__name__}: {results.failed} of {results.attempted}")

		assert failed == [], f"docstring examples that did not match: {failed}"

	def test_the_examples_are_actually_being_found (self) -> None:
		"""A test that runs nothing passes, and would hide every example.

		A floor rather than an exact count, so that adding an example does not
		fail this but losing the collection does.
		"""
		attempted = sum(
			doctest.testmod(module, verbose = False, report = False).attempted
			for module in _modules()
		)

		assert attempted >= 30, f"only {attempted} doctest examples ran"

	def test_the_modules_with_doctests_are_the_ones_expected (self) -> None:
		"""Says out loud which modules carry ``>>>`` examples, so losing one shows."""
		with_examples = {
			module.__name__
			for module in _modules()
			if doctest.testmod(module, verbose = False, report = False).attempted
		}

		assert with_examples == {
			"pymididefs.cc", "pymididefs.drums", "pymididefs.notes", "pymididefs.scaling",
		}


class TestLiteralBlockExamples:

	"""The ``expression  # value`` lines in the module docstrings' ``::`` blocks.

	These read exactly like doctests to somebody skimming, and are not: without
	a ``>>>`` prompt nothing runs them.
	"""

	def test_the_examples_are_being_found (self) -> None:
		"""If a docstring's format changes, this fails rather than passing empty."""
		found = {
			module.__name__: _examples_in(module.__doc__ or "")
			for module in _modules()
		}
		total = sum(len(examples) for examples in found.values())

		assert total >= 10, found

	def test_every_example_evaluates_to_what_it_claims (self) -> None:
		for module in _modules():
			_check(_examples_in(module.__doc__ or ""), f"{module.__name__}'s docstring")


class TestReadmeExamples:

	"""Every ``expression  # value`` line in the README's Python blocks.

	The README is the first thing a reader of this package sees, and its printed
	values are exactly the kind of claim this project keeps finding stale.
	"""

	def test_the_examples_are_being_found (self) -> None:
		"""If the README's format changes, this fails rather than passing empty."""
		examples = _examples_in(_readme().read_text(encoding = "utf-8"), python_only = True)

		assert len(examples) >= 30, examples

	def test_every_example_evaluates_to_what_it_claims (self) -> None:
		_check(
			_examples_in(_readme().read_text(encoding = "utf-8"), python_only = True),
			"README.md",
		)
