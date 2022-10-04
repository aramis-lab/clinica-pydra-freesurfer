from pydra.engine.specs import ShellOutSpec, ShellSpec, SpecInfo

from pydra import ShellCommandTask

__all__ = ["MRISExpand"]


class MRISExpand(ShellCommandTask):
    """Task for mris_expand.

    Expand a surface outwards by a specified amount while maintaining smoothness and self-intersection constraints.

    Examples
    --------

    1. Expand by cortical thickness:

    >>> task = MRISExpand(
    ...     input_surface="lh.white",
    ...     distance=0.5,
    ...     thickness=True
    ... )
    >>> task.cmdline    # doctest: +ELLIPSIS
    'mris_expand -thickness lh.white 0.5 ...lh_expanded.white'

    2. Expand by distance from label:

    >>> task = MRISExpand(
    ...     input_surface="lh.white",
    ...     distance=0.5,
    ...     output_surface="lh.graymid",
    ...     label="labelfile",
    ... )
    >>> task.cmdline
    'mris_expand -label labelfile lh.white 0.5 lh.graymid'
    """

    input_spec = SpecInfo(
        name="MRISExpandInput",
        fields=[
            (
                "input_surface",
                str,
                {
                    "help_string": "input surface file",
                    "mandatory": True,
                    "argstr": "{input_surface}",
                    "position": -3,
                },
            ),
            (
                "distance",
                float,
                {
                    "help_string": "distance in mm or fraction of cortical thickness",
                    "mandatory": True,
                    "argstr": "{distance}",
                    "position": -2,
                },
            ),
            (
                "output_surface",
                str,
                {
                    "help_string": "output surface file",
                    "argstr": "{output_surface}",
                    "position": -1,
                    "output_file_template": "{input_surface}_expanded",
                },
            ),
            (
                "thickness",
                bool,
                {
                    "help_string": "expand by fraction of cortical thickness",
                    "argstr": "-thickness",
                },
            ),
            (
                "label",
                str,
                {
                    "help_string": "label file",
                    "argstr": "-label {label}",
                },
            ),
        ],
        bases=(ShellSpec,),
    )

    output_spec = SpecInfo(
        name="MRISExpandOutput",
        fields=[],
        bases=(ShellOutSpec,),
    )

    executable = "mris_expand"
