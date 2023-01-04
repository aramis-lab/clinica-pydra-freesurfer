# pydra-freesurfer

[![PyPI - Version](https://img.shields.io/pypi/v/pydra-freesurfer.svg)](https://pypi.org/project/pydra-freesurfer)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydra-freesurfer.svg)](https://pypi.org/project/pydra-freesurfer)

---

Pydra tasks for FreeSurfer.

[Pydra][pydra] is a dataflow engine
which provides a set of lightweight abstractions
for DAG construction, manipulation, and distributed execution.

[FreeSurfer][freesurfer] is a neuroimaging toolkit
for processing, analyzing, and visualizing human brain MR images.

This project exposes some of FreeSurfer's utilities as Pydra tasks
to facilitate their incorporation into more advanced processing workflows.

**Table of contents**

- [Installation](#installation)
- [Available interfaces](#available-interfaces)
- [Development](#development)
- [Licensing](#licensing)

## Installation

```console
pip install pydra-freesurfer
```

## Available interfaces

- gtmseg
- mri_convert
- mri_surf2surf
- mri_vol2vol
- mris_expand
- mris_preproc
- recon-all
- tkregister2

## Development

This project is managed using [Poetry].

To install, check and test the code:

```console
make
```

To run the test suite when hacking:

```console
make test
```

To format the code before review:

```console
make format
```

To build the project's documentation:

```console
make docs
```

## Licensing

This project is released under the terms of the [Apache License, Version 2.0][license].

[pydra]: https://nipype.github.io/pydra
[freesurfer]: https://surfer.nmr.mgh.harvard.edu
[poetry]: https://python-poetry.org
[license]: https://opensource.org/licenses/Apache-2.0
