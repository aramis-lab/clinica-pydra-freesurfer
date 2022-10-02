from pydra.engine.specs import ShellOutSpec, ShellSpec, SpecInfo

from pydra import ShellCommandTask

__all__ = ["TkRegister2"]


class TkRegister2(ShellCommandTask):
    """Task for tkregister2.

    tkregister2 is a tool to assist in the manual tuning of the linear registration between two volumes, mainly for the
    purpose of interacting with the FreeSurfer anatomical stream.
    """

    input_spec = SpecInfo(
        name="TkRegister2Input",
        fields=[],
        bases=(ShellSpec,),
    )

    output_spec = SpecInfo(
        name="TkRegisterOutput",
        fields=[],
        bases=(ShellOutSpec,),
    )

    executable = "tkregister2"
