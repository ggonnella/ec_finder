# EcFinder

EcFinder tries to find an EC number for an enzyme name
using exact and fuzzy search.

It automatically downloads the EC data file from Expasy.

## Installation

It can be installed using ``pip install ec_finder``.

## CLI

The CLI tool ``ec-find`` is provided by the package.

### Setup

The first time the tool is called from the command line, the enzyme
data file is downloaded from Expasy. To update the file if a new file
is available, use ``ec-find update``.
To remove the file (e.g. to force an update), use ``ec-find cleanup``.

### Search

Use ``ec-find "enzyme name"`` to find the EC number for an enzyme name.
Note the quotes, necessary if there are spaces.

Use ``ec-find filename 1`` to find the EC number for all enzyme names
in a file, where each line contains only an enzyme name each.

Use ``ec-find filename colnum`` to find the EC number for all enzyme names
in a Tab-separated file, where enzyme names are in the column with the
specified 1-based column number.

Use ``ec-find filename colnum --separator S`` to find the EC number for all
enzyme names in a file separated by separator ``S``.

## API

The first time that ``ec_finder`` is imported, the package
data is downloaded from Expasy.

The ``ec_finder.update()`` function can be used to check if new
enzyme data is avalaible at Expasy and, if so, download it and update
the data. The ``ec.finder.cleanup()`` function deletes the data.

The ``ec_finder.search(enzyme_name)`` function is used for searching
for an enzyme name.

## Output format

The output format consists of three fields, separated by the separator
indicated in the ``--separator`` option (CLI), or by the ``separator`` argument
of ``search()`` (API). By default the Tab is used.

The three fields are:
- result comment
- result EC
- enzyme name (input)

The result comment may be:
- MAIN, the enzyme name was found as one of the main enzye names.
- ALT, the enzyme name was found as one of the alternative enzyme names.
- FUZZY:foobar, the enzyme name was not found, but a similar one (foobar)
  was found
- NOT\_FOUND, the enzyme name was not found (in this case EC is empty)

If the input of the CLI tool ``ec-find`` is a file, then each file line
is output after the three fields reported above, separated from it by the
separator (default: tab).

## Settings

The minimum score for the fuzzy search is by default "90" and can be set
to a value between 0 and 100 by the option ``--min-score`` of the CLI
or by the argument ``min_score`` of the API function ``search()``.

The separator in the output is by default TAB and can be set by
the CLI option ``--separator`` (which also changes the input separator,
if the input is a file) or by the API function ``search()`` argument
``separator``.
