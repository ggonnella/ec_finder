# EcFinder

EcFinder tries to find an EC number for an enzyme name
using exact and fuzzy search.

It automatically downloads the EC data file from Expasy.

## Installation

It can be installed using ``pip install ec_finder``.

## CLI

The CLI tool ``ec-find`` is provided by the package.
The first time the tool is called from the command line, the enzyme
data are downloaded from Expasy.

## API

The first time that ``ec_finder`` is imported, the package
data is downloaded from Expasy.

The ``ec_finder.update()`` function can be used to check if new
enzyme data is avalaible at Expasy and, if so, download it and update
the data.

The ``ec_finder.search()`` function is used for searching
for an enzyme name.
