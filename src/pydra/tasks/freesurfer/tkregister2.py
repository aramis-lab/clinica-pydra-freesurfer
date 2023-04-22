"""
TkRegister2
===========

Linear registration between two volumes,
mainly for the purpose of interacting with the FreeSurfer anatomical stream.

Examples
--------

Create a registration matrix between the conformed space (orig.mgz) and the native anatomical (rawavg.mgz):

>>> task = TkRegister2(
...     moving_volume_file="rawavg.mgz",
...     target_volume_file="orig.mgz",
...     registration_file="register.native.dat",
...     compute_registration_from_headers=True,
... )
>>> task.cmdline
'tkregister2 --noedit --mov rawavg.mgz --targ orig.mgz --reg register.native.dat --regheader'


"""

import attrs

import pydra

__all__ = ["TkRegister2"]


@attrs.define(slots=False, kw_only=True)
class TkRegister2Spec(pydra.specs.ShellSpec):
    """Specifications for tkregister2."""

    moving_volume_file: str = attrs.field(
        metadata={
            "help_string": "moving volume",
            "mandatory": True,
            "argstr": "--mov",
        }
    )

    target_volume_file: str = attrs.field(
        metadata={
            "help_string": "target volume",
            "mandatory": True,
            "argstr": "--targ",
        }
    )

    registration_file: str = attrs.field(
        metadata={
            "help_string": "registration file in FreeSurfer's format",
            "argstr": "--reg",
            "output_file_template": "{registration_file}",
        }
    )

    compute_registration_from_headers: bool = attrs.field(
        metadata={
            "help_string": "compute registration from the headers of the input volumes",
            "argstr": "--regheader",
        }
    )


class TkRegister2(pydra.ShellCommandTask):
    """Task for tkregister2."""

    input_spec = pydra.specs.SpecInfo(
        name="TkRegister2Input",
        bases=(TkRegister2Spec, pydra.specs.ShellSpec),
    )

    executable = "tkregister2 --noedit"
