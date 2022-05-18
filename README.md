# pydra-freesurfer

Pydra tasks for FreeSurfer.

[Pydra] is a dataflow engine which provides a set of lightweight abstractions for DAG construction, manipulation, and
distributed execution.

[FreeSurfer] is a neuroimaging toolkit for processing, analyzing, and visualizing human brain MR images.

This project exposes some of FreeSurfer's utilities as Pydra tasks to facilitate their incorporation into more advanced
processing workflows.

## Development

Setup for development requires [Poetry](https://python-poetry.org/).

Install the project and its dependencies with:

```console
make install
```

Run the tests with:

```console
make test
```

Build the project's documentation with:

```console
make docs
```

Format the code before review with:

```console
make format
```

## Licensing

This project is released under the terms of the Apache License 2.0.

[Pydra]: https://nipype.github.io/pydra/
[Freesurfer]: https://surfer.nmr.mgh.harvard.edu/
