import typing as ty

from pydra.engine.specs import ShellOutSpec, ShellSpec, SpecInfo

from pydra import ShellCommandTask

__all__ = ["MRIVol2Vol"]


class MRIVol2Vol(ShellCommandTask):
    """Task for mri_vol2vol.

    Resamples a volume into another field-of-view using various types of matrices (FreeSurfer, FSL, SPM, and MNI). This
    is meant to be used in conjunction with tkregister2.

    Examples
    --------

    1. Resample functional data into anatomical space:

    >>> task = MRIVol2Vol(
    ...     regfile="register.dat",
    ...     movvol="func.nii.gz",
    ...     fstarg=True,
    ...     outvol="func-in-anat.mgh",
    ... )
    >>> task.cmdline
    'mri_vol2vol --mov func.nii.gz --o func-in-anat.mgh --reg register.dat --fstarg'
    """

    input_spec = SpecInfo(
        name="MRIVol2VolInput",
        fields=[
            (
                "movvol",
                str,
                {
                    "help_string": "input volume (or output template with --inv)",
                    "argstr": "--mov {movvol}",
                },
            ),
            (
                "outvol",
                str,
                {
                    "help_string": "output volume",
                    "argstr": "--o {outvol}",
                    "output_file_template": "{outvol}",
                },
            ),
            (
                "regfile",
                str,
                {
                    "help_string": "tkRAS-to-tkRAS matrix",
                    "argstr": "--reg {regfile}",
                },
            ),
            (
                "fstarg",
                bool,
                {
                    "help_string": "use vol from subject in --reg as target",
                    "argstr": "--fstarg",
                    "requires": ["regfile"],
                },
            ),
        ],
        bases=(ShellSpec,),
    )

    output_spec = SpecInfo(
        name="MRIVol2VolOutput",
        fields=[],
        bases=(ShellOutSpec,),
    )

    executable = "mri_vol2vol"
