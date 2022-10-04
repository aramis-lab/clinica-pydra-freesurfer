from pydra.engine.specs import ShellOutSpec, ShellSpec, SpecInfo

from pydra import ShellCommandTask

__all__ = ["MRISExpand"]


class MRISExpand(ShellCommandTask):
    """Task for mris_expand.

    Examples
    --------
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
                    "mandatory": True,
                    "argstr": "{output_surface}",
                    "position": -1,
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
