"""
Expand
======

Expand a surface outwards by a specified amount
while maintaining smoothness and self-intersection constraints.

Examples
--------

1. Expand by cortical thickness:

>>> task = Expand(input_surface="lh.white", distance=0.5, use_thickness=True)
>>> task.cmdline    # doctest: +ELLIPSIS
'mris_expand -thickness lh.white 0.5 ...lh_expand.white'

2. Expand by distance from label:

>>> task = Expand(input_surface="lh.white", distance=0.5, output_surface="lh.graymid", label_file="labelfile")
>>> task.cmdline
'mris_expand -label labelfile lh.white 0.5 lh.graymid'
"""

__all__ = ["Expand"]

from os import PathLike

from attrs import define, field

from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


@define(kw_only=True)
class MIRSExpandSpec(ShellSpec):
    """Specifications for mris_expand."""

    input_surface: PathLike = field(
        metadata={"help_string": "input surface", "mandatory": True, "argstr": "", "position": -3}
    )

    distance: float = field(
        metadata={
            "help_string": "distance in millimeters",
            "mandatory": True,
            "argstr": "",
            "position": -2,
        }
    )

    output_surface: str = field(
        metadata={
            "help_string": "output surface",
            "argstr": "",
            "position": -1,
            "output_file_template": "{input_surface}_expand",
        }
    )

    use_thickness: bool = field(
        metadata={"help_string": "treat distance as fraction of cortical thickness", "argstr": "-thickness"}
    )

    label_file: PathLike = field(metadata={"help_string": "input labels", "argstr": "-label"})


class Expand(ShellCommandTask):
    """Task definition for mris_expand."""

    input_spec = SpecInfo(name="Input", bases=(MIRSExpandSpec,))

    executable = "mris_expand"
