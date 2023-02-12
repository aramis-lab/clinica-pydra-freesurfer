"""
MRIBinarize
===========

Binarize a volume (or volume-encoded surface file) based on thresholds or match values.
Can also be used to merge other results of binarization.

Examples
--------

>>> task = MRIBinarize(
...     input_volume_file="aseg.nii.gz",
...     output_volume_file="mask.nii.gz",
...     min_value=1000,
...     max_value=1999,
...     bin_value=1,
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'mri_binarize --i aseg.nii.gz --min 1000 --max 1999 --o mask.nii.gz --count ...aseg_count.txt --binval 1'
"""
import os
import typing as ty

import attrs

import pydra

__all__ = ["MRIBinarize"]


@attrs.define(slots=False, kw_only=True)
class MRIBinarizeSpec(pydra.specs.ShellSpec):
    """Specifications for mri_binarize."""

    input_volume_file: os.PathLike = attrs.field(
        metadata={"help_string": "input volume", "mandatory": True, "argstr": "--i"}
    )

    min_value: float = attrs.field(
        metadata={
            "help_string": "minimum absolute threshold value",
            "argstr": "--min",
            "xor": {"relative_min", "relative_max", "match_values"},
        }
    )

    max_value: float = attrs.field(
        metadata={
            "help_string": "maximum absolute threshold value",
            "argstr": "--max",
            "xor": {"relative_min", "relative_max", "match_values"},
        }
    )

    relative_min: float = attrs.field(
        metadata={
            "help_string": "minimum threshold value relative to the global mean",
            "argstr": "--rmin",
            "xor": {"min_value", "max_value", "match_values"},
        }
    )

    relative_max: float = attrs.field(
        metadata={
            "help_string": "maximum threshold value relative to the global mean",
            "argstr": "--rmax",
            "xor": {"min_value", "max_value", "match_values"},
        }
    )

    percentage: float = attrs.field(
        metadata={
            "help_string": "set the minimum threshold to capture a given percentage of top voxel values",
            "argstr": "--pct",
            "xor": {"min_value", "relative_min", "match_values"},
        }
    )

    false_discovery_rate: float = attrs.field(
        metadata={
            "help_string": "set the minimum threshold to achieve a given false discovery rate",
            "argstr": "--fdr",
            "xor": {"min_value", "relative_min", "match_values"},
        }
    )

    match_values: ty.Iterable[float] = attrs.field(
        metadata={
            "help_string": "binarize based on match values",
            "argstr": "--match",
            "xor": {"min_value", "max_value", "relative_min", "relative_max"},
        }
    )

    output_volume_file: str = attrs.field(
        metadata={
            "help_string": "output volume",
            "argstr": "--o",
            "output_file_template": "{input_volume_file}_mask",
        }
    )

    output_count_file: str = attrs.field(
        metadata={
            "help_string": "save hit counts",
            "argstr": "--count",
            "output_file_template": "{input_volume_file}_count.txt",
            "keep_extension": False,
        }
    )

    bin_value: int = attrs.field(
        metadata={"help_string": "substitute value for voxels in range of binarization", "argstr": "--binval"}
    )

    not_bin_value: int = attrs.field(
        metadata={
            "help_string": "substitute value for voxels not in range for binarization",
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

    mask_file: os.PathLike = attrs.field(
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
