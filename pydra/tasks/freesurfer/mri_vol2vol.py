from pydra.engine.specs import ShellOutSpec, ShellSpec, SpecInfo

from pydra import ShellCommandTask

__all__ = ["MRIVol2Vol"]


class MRIVol2Vol(ShellCommandTask):
    """Task for mri_vol2vol.

    Resamples a volume into another field-of-view using various types of matrices (FreeSurfer, FSL, SPM, and MNI). This
    is meant to be used in conjunction with tkregister2.

    Examples
    --------
    """

    input_spec = SpecInfo(
        name="MRIVol2VolInput",
        fields=[],
        bases=(ShellSpec,),
    )

    output_spec = SpecInfo(
        name="MRIVol2VolOutput",
        fields=[],
        bases=(ShellOutSpec,),
    )

    cmdline = "mri_vol2vol"
