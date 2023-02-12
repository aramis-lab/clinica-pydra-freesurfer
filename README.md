# pydra-freesurfer

[![PyPI - Version](https://img.shields.io/pypi/v/pydra-freesurfer.svg)](https://pypi.org/project/pydra-freesurfer)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydra-freesurfer.svg)](https://pypi.org/project/pydra-freesurfer)
[![PyPI - Downloads](https://static.pepy.tech/badge/pydra-freesurfer)](https://pypi.org/project/pydra-freesurfer)

---

Pydra tasks for FreeSurfer.

[Pydra][pydra] is a dataflow engine
which provides a set of lightweight abstractions
for DAG construction, manipulation, and distributed execution.

[FreeSurfer][freesurfer] is a neuroimaging toolkit
for processing, analyzing, and visualizing human brain MR images.

This project exposes some of FreeSurfer's utilities as Pydra tasks
to facilitate their integration into more advanced processing workflows.

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
- mri_aparc2aseg
- mri_binarize
- mri_convert
- mri_label2vol
- mri_surf2surf
- mri_vol2vol
- mris_anatomical_stats
- mris_ca_label
- mris_ca_train
- mris_expand
- mris_preproc
- recon-all
- tkregister2

## Development

This project is managed with [Hatch][hatch]:

```console
pipx install hatch
```

To run the test suite:

```console
hatch run test:no-cov
```

To fix linting issues:

```console
hatch run lint:fix
```

To check the documentation:

```console
hatch run docs:serve --open-browser
```

## Licensing

This project is released under the terms of the [Apache License, Version 2.0][license].

[pydra]: https://nipype.github.io/pydra
[freesurfer]: https://surfer.nmr.mgh.harvard.edu
[hatch]: https://hatch.pypa.io
[license]: https://opensource.org/licenses/Apache-2.0
