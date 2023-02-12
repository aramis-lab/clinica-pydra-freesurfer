"""
MRIBinarize
===========

Binarize a volume (or volume-encoded surface file) based on thresholds or match values.
Can also be used to merge other results of binarization.

Examples
--------

>>> task = MRIBinarize(
...     input_volume="aseg.nii.gz",
...     output_volume="mask.nii.gz",
...     min=1000,
...     max=1999,
...     bin_value=1,
... )
>>> task.cmdline
'mri_binarize --i aseg.nii.gz --min 1000 --max 1999 --o mask.nii.gz --binval 1'
"""
import os
import typing as ty

import attrs

import pydra

__all__ = ["MRIBinarize"]


@attrs.define(slots=False, kw_only=True)
class MRIBinarizeSpec(pydra.specs.ShellSpec):
    """Specifications for mri_binarize."""

    input_volume: os.PathLike = attrs.field(
        metadata={"help_string": "input volume", "mandatory": True, "argstr": "--i"}
    )

    min: float = attrs.field(
        metadata={
            "help_string": "minimum threshold",
            "argstr": "--min",
            "xor": {"rmin", "rmax", "match"},
        }
    )

    max: float = attrs.field(
        metadata={
            "help_string": "maximum threshold",
            "argstr": "--max",
            "xor": {"rmin", "rmax", "match"},
        }
    )

    rmin: float = attrs.field(
        metadata={
            "help_string": "minimum relative threshold",
            "argstr": "--rmin",
            "xor": {"min", "max", "match"},
        }
    )

    rmax: float = attrs.field(
        metadata={
            "help_string": "maximum relative threshold",
            "argstr": "--rmax",
            "xor": {"min", "max", "match"},
        }
    )

    pct: float = attrs.field(
        metadata={
            "help_string": (
                "Set min threshold so that the top P percent of the voxels"
                " are captured in the output mask."
            ),
            "argstr": "--pct",
            "xor": {"min", "rmin"},
        }
    )

    fdr: float = attrs.field(
        metadata={
            "help_string": "set min threshold to achieve a given FDR.",
            "argstr": "--fdr",
            "xor": {"min", "rmin"},
        }
    )

    match: ty.Iterable[float] = attrs.field(
        metadata={
            "help_string": "binarize based on match values",
            "argstr": "--match",
            "xor": {"min", "max", "rmin", "rmax"},
        }
    )

    output_volume: str = attrs.field(
        metadata={
            "help_string": "output volume",
            "mandatory": True,
            "argstr": "--o",
            "output_file_template": "{input_volume}_binarized",
        }
    )

    bin_value: int = attrs.field(
        metadata={"help_string": "value to use for voxels in range for binarization", "argstr": "--binval"}
    )

    not_bin_value: int = attrs.field(
        metadata={
            "help_string": "value to use for voxels not in range for binarization",
            "argstr": "--binvalnot",
            "xor": {"merge_volume_file"},
        }
    )

    copy_volume_file: os.PathLike = attrs.field(
        metadata={"help_string": "copy values from this volume to the output", "argstr": "--copy"}
    )

    merge_volume_file: os.PathLike = attrs.field(
        metadata={"help_string": "merge binarization with this volume", "argstr": "--merge", "xor": {"not_bin_value"}}
    )

    mask_volume_file: os.PathLike = attrs.field(
        metadata={"help_string": "input mask applied to volume", "argstr": "--mask"}
    )

    mask_threshold: float = attrs.field(
        metadata={
            "help_string": "threshold applied to input mask (default is 0.5)",
            "argstr": "--mask-thresh",
            "requires": {"mask_file"},
        }
    )

    save_as_uchar: bool = attrs.field(
        metadata={"help_string": "save output volume as unsigned char", "argstr": "--uchar"}
    )


class MRIBinarize(pydra.engine.ShellCommandTask):
    """Task definition for mri_binarize."""

    input_spec = pydra.specs.SpecInfo(
        name="MRIBinarizeInput",
        bases=(MRIBinarizeSpec,),
    )

    executable = "mri_binarize"
