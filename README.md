# pydra-freesurfer

Pydra tasks for FreeSurfer.

[Pydra] is a dataflow engine which provides a set of lightweight abstractions
for DAG construction, manipulation, and distributed execution.

[FreeSurfer] is a neuroimaging toolkit for processing, analyzing, and
visualizing human brain MR images.

This project exposes some of FreeSurfer's utilities as Pydra tasks to
facilitate their incorporation into more advanced processing workflows.

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

This project is released under the terms of the Apache License 2.0.


[Pydra]: https://nipype.github.io/pydra
[Freesurfer]: https://surfer.nmr.mgh.harvard.edu
[Poetry]: https://python-poetry.org
