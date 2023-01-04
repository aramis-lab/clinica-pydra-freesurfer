"""
MRISExpand
==========

Expand a surface outwards by a specified amount
while maintaining smoothness and self-intersection constraints.

Examples
--------

1. Expand by cortical thickness:

>>> task = MRISExpand(
...     input_surface_file="lh.white",
...     fraction_of_cortical_thickness=0.5,
... )
>>> task.cmdline    # doctest: +ELLIPSIS
'mris_expand -thickness lh.white 0.5 ...lh_expanded.white'

2. Expand by distance from label:

>>> task = MRISExpand(
...     input_surface_file="lh.white",
...     distance=0.5,
...     output_surface_file="lh.graymid",
...     label="labelfile",
... )
>>> task.cmdline
'mris_expand -label labelfile lh.white 0.5 lh.graymid'
"""

import attrs

import pydra

__all__ = ["MRISExpand"]


@attrs.define(slots=False, kw_only=True)
class MIRSExpandSpec(pydra.specs.ShellSpec):
    """Specifications for mris_expand."""

    input_surface_file: str = attrs.field(
        metadata={
            "help_string": "input surface",
            "mandatory": True,
            "argstr": "",
            "position": -3,
        }
    )

    distance: float = attrs.field(
        metadata={
            "help_string": "distance in millimeters",
            "mandatory": True,
            "argstr": "",
            "position": -2,
            "xor": {"fraction_of_cortical_thickness"},
        }
    )

    fraction_of_cortical_thickness: float = attrs.field(
        metadata={
            "help_string": "fraction of cortical thickness",
            "mandatory": True,
            "argstr": "",
            "position": -2,
            "xor": {"distance"},
        }
    )

    output_surface_file: str = attrs.field(
        metadata={
            "help_string": "output surface",
            "argstr": "",
            "position": -1,
            "output_file_template": "{input_surface_file}_expanded",
        }
    )

    distance_is_fraction_of_cortical_thickness: bool = attrs.field(
        metadata={
            "help_string": "treat distance as fraction of cortical thickness",
            "formatter": (
                lambda fraction_of_cortical_thickness, distance_is_fraction_of_cortical_thickness: "-thickness"
                if fraction_of_cortical_thickness
                or distance_is_fraction_of_cortical_thickness
                else ""
            ),
        }
    )

    label: str = attrs.field(
        metadata={
            "help_string": "input labels",
            "argstr": "-label",
        }
    )


class MRISExpand(pydra.ShellCommandTask):
    """Task for mris_expand."""

    input_spec = pydra.specs.SpecInfo(
        name="MRISExpandInput",
        bases=(MIRSExpandSpec, pydra.specs.ShellSpec),
    )

    executable = "mris_expand"
