from enum import Enum

from pydra.engine.specs import ShellSpec, SpecInfo

from pydra import ShellCommandTask

__all__ = ("ReconAll",)


ReconAllInputSpec = SpecInfo(
    name="ReconAllInputs",
    fields=[
        ("subject", str, dict(argstr="-s {subject}", help_string="Subject identifier")),
        ("directive", str, dict(argstr="-{directive}", help_string="Workflow directive", position=-1)),
    ],
    bases=(ShellSpec,),
)


class ReconAll(ShellCommandTask):
    """Task for FreeSurfer's recon-all pipeline.

    Fully automatic structural imaging stream for processing cross-sectional and longitudinal data.

    Examples
    --------
    >>> task = ReconAll()
    >>> task.inputs.subject = "sub-01"
    >>> task.inputs.directive = "all"
    >>> task.cmdline
    'recon-all -s sub-01 -all'
    """

    input_spec = ReconAllInputSpec
    output_spec = None
    executable = "recon-all"
