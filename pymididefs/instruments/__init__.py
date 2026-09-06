"""What a particular model of instrument does, as opposed to what MIDI does.

The rest of this package holds **specification** facts — CC 7 is Volume, note 60
is C4.  They are true for everybody, permanently, and they cannot be wrong.

This module holds **model** facts — a Minitaur ignores notes above 72, a
Matriarch's CC 94 switches it between one, two and four voices.  They are true
for everybody who owns that model, and they change when the manufacturer ships
firmware.  A model fact is a *report*, so a definition carries provenance saying
which manual and which page it came from, and an imported one stays marked
unverified until a person has checked it.

**Rig** facts — which channel *your* Minitaur is on, which port it is plugged
into — are never here.  They belong to your composition.

Reading a definition needs a YAML parser, which the base install deliberately
does not pull in::

	pip install pymididefs[instruments]

Importing this module does not need one; only reading a file does, and the
error says what to install.

::

	import pymididefs.instruments

	matriarch = pymididefs.instruments.load("moog_matriarch")

	matriarch.voice.polyphony                      # None — switchable, see voicing_modes
	matriarch.controls["glide_type"].kind          # 'choice'
	matriarch.controls["glide_type"].value_for("exp")   # what to send for EXP

Definitions are looked for beside your composition first, then in your own
library, then in the set bundled here — so a file you drop always beats one we
shipped.  That is the whole answer to adding your own synth.

To start one from a MIDNAM file — Ardour bundles several hundred — see
``pymididefs.instruments.midnam``.  What it lands is a draft: MIDNAM carries a
control map and nothing else, and the numbers in it are worth checking.
"""

# This file is a re-export shim, and it is the one place in the package that
# imports names rather than modules. A subpackage cannot reach itself by its own
# full path while it is still being imported -- `pymididefs.instruments` is not
# an attribute of `pymididefs` until this file finishes -- so the usual
# fully-qualified style is not available here. Everywhere else it holds.

from pymididefs.instruments.definition import (
	CHOICE,
	CONTINUOUS,
	SWITCH,
	Control,
	Definition,
	Midi,
	Model,
	Voice,
)
from pymididefs.instruments.loading import (
	DefinitionNotFound,
	available,
	load,
	load_file,
	locate,
	parse,
	search_path,
)
from pymididefs.instruments.validation import DefinitionError


# The public surface, declared rather than implied. Nothing else in this package
# does this yet; a shim module is the one place it is unambiguously right, and it
# is what makes these re-exports explicit to a type checker as well as a reader.
__all__ = [
	"CHOICE",
	"CONTINUOUS",
	"SWITCH",
	"Control",
	"Definition",
	"DefinitionError",
	"DefinitionNotFound",
	"Midi",
	"Model",
	"Voice",
	"available",
	"load",
	"load_file",
	"locate",
	"parse",
	"search_path",
]
