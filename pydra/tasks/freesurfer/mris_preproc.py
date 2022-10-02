from pydra.engine.specs import ShellOutSpec, ShellSpec, SpecInfo

from pydra import ShellCommandTask

__all__ = ["MRISPreproc"]


class MRISPreproc(ShellCommandTask):
    """Task for mris_preproc.

    Script to prepare surface-based data for high-level analysis by resampling surface or volume source data to a
    common subject (usually an average subject) and then concatenating them into one file which can then be used by a
    number of programs (eg, mri_glmfit).

    Examples
    --------
    """

    input_spec = SpecInfo(
        name="MRISPreprocInput",
        fields=[],
        bases=(ShellSpec,),
    )

    output_spec = SpecInfo(
        name="MRISPreprocOutput",
        fields=[],
        bases=(ShellOutSpec,),
    )

    executable = "mris_preproc"
