"""
TkRegister2
===========

Linear registration between two volumes,
mainly for the purpose of interacting with the FreeSurfer anatomical stream.

Examples
--------

Create a registration matrix between the conformed space (orig.mgz) and the native anatomical (rawavg.mgz):

>>> task = TkRegister2(moving_volume="rawavg.mgz", target_volume="orig.mgz", register_from_headers=True)
>>> task.cmdline    # doctest: +ELLIPSIS
'tkregister2 --noedit --mov rawavg.mgz --targ orig.mgz --reg ...rawavg_tkregister2.dat --regheader'
"""

__all__ = ["TkRegister2"]

from os import PathLike

from attrs import define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


@define(kw_only=True)
class TkRegister2Spec(ShellSpec):
    """Specifications for tkregister2."""

    moving_volume: PathLike = field(metadata={"help_string": "moving volume", "mandatory": True, "argstr": "--mov"})

    target_volume: PathLike = field(metadata={"help_string": "target volume", "mandatory": True, "argstr": "--targ"})

    output_registration_file: str = field(
        metadata={
            "help_string": "output registration file",
            "argstr": "--reg",
            "output_file_template": "{moving_volume}_tkregister2.dat",
            "keep_extension": False,
        }
    )

    register_from_headers: bool = field(
        metadata={"help_string": "compute registration from headers", "argstr": "--regheader"}
    )

    align_volume_centers: bool = field(
        metadata={"help_string": "register from headers and align volume centers", "argstr": "--regheader-center"}
    )


class TkRegister2(ShellCommandTask):
    """Task for tkregister2."""

    executable = "tkregister2 --noedit"

    input_spec = SpecInfo(name="Input", bases=(TkRegister2Spec,))
