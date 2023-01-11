"""
MRIConvert
==========

General purpose utility for converting between different file formats.

Examples
--------

Convert volume data to float:

>>> task = MRIConvert(
...     input_volume_file="orig.nii.gz",
...     output_volume_file="float.nii.gz",
...     output_data_type="float",
... )
>>> task.cmdline
'mri_convert -odt float orig.nii.gz float.nii.gz'
"""

import attrs

import pydra

__all__ = ["MRIConvert"]


@attrs.define(slots=False, kw_only=True)
class MRIConvertSpec(pydra.specs.ShellSpec):
    """Specifications for mri_convert."""

    input_volume_file: str = attrs.field(
        metadata={
            "help_string": "input volume",
            "mandatory": True,
            "argstr": "",
            "position": -2,
        }
    )

    output_volume_file: str = attrs.field(
        metadata={
            "help_string": "output volume",
            "argstr": "",
            "position": -1,
            "output_file_template": "{input_volume}_converted.nii.gz",
        }
    )

    output_data_type: str = attrs.field(
        metadata={
            "help_string": "output data type",
            "argstr": "-odt",
        }
    )


class MRIConvert(pydra.ShellCommandTask):
    """Task for mri_convert."""

    input_spec = pydra.specs.SpecInfo(
        name="MRIConvertInput",
        bases=(MRIConvertSpec, pydra.specs.ShellSpec),
    )

    executable = "mri_convert"
