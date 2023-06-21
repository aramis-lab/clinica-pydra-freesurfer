"""
Convert
=======

General purpose utility for converting between different file formats.

Examples
--------

Convert volume data to float:

>>> task = Convert(input_volume="orig.nii.gz", output_volume="float.nii.gz", output_datatype="float")
>>> task.cmdline
'mri_convert -odt float orig.nii.gz float.nii.gz'
"""

__all__ = ["Convert"]

from os import PathLike

from attrs import define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


@define(kw_only=True)
class ConvertSpec(ShellSpec):
    """Specifications for mri_convert."""

    input_volume: PathLike = field(
        metadata={
            "help_string": "input volume",
            "mandatory": True,
            "argstr": "",
            "position": -2,
        }
    )

    output_volume: str = field(
        metadata={
            "help_string": "output volume",
            "argstr": "",
            "position": -1,
            "output_file_template": "{input_volume}_convert.nii.gz",
        }
    )

    output_datatype: str = field(
        metadata={
            "help_string": "output datatype",
            "argstr": "-odt",
            "allowed_values": {"uchar", "short", "int", "float", "rgb"},
        }
    )


class Convert(ShellCommandTask):
    """Task definition for mri_convert."""

    input_spec = SpecInfo(name="ConvertInput", bases=(ConvertSpec,))

    executable = "mri_convert"
