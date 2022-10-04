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
        fields=[],
        bases=(ShellSpec,),
    )

    output_spec = SpecInfo(
        name="MRISExpandOutput",
        fields=[],
        bases=(ShellOutSpec,),
    )

    executable = "mris_expand"
