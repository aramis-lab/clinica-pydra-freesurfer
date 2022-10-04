import typing as ty

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

    1. Resample abcXX-anat/surf/lh.thickness onto fsaverage:

    >>> task = MRISPreproc(
    ...     source_subject_ids=[f"abc{s:02d}-anat" for s in range(1, 5)],
    ...     target_subject_id="fsaverage",
    ...     hemifield="lh",
    ...     measure="thickness",
    ...     output_file="abc-lh-thickness.mgh",
    ... )
    >>> task.cmdline
    'mris_preproc --out abc-lh-thickness.mgh --target fsaverage --hemi lh --meas thickness \
--s abc01-anat --s abc02-anat --s abc03-anat --s abc04-anat'
    """

    input_spec = SpecInfo(
        name="MRISPreprocInput",
        fields=[
            (
                "output_file",
                str,
                {
                    "help_string": "path where to save output",
                    "argstr": "--out {output_file}",
                    "output_file_template": "concat_{hemifield}_{target_subject_id}.mgz",
                },
            ),
            (
                "target_subject_id",
                str,
                {
                    "help_string": "subject to use as the common space",
                    "mandatory": True,
                    "argstr": "--target {target_subject_id}",
                },
            ),
            (
                "hemifield",
                str,
                {
                    "help_string": "hemifield",
                    "mandatory": True,
                    "argstr": "--hemi",
                    "allowed_values": {"lh", "rh"},
                },
            ),
            (
                "measure",
                str,
                {
                    "help_string": "use source subject's measure as input",
                    "argstr": "--meas {measure}",
                },
            ),
            (
                "source_subject_ids",
                ty.Iterable[str],
                {
                    "help_string": "source subjects used as input",
                    "argstr": "--s...",
                    "requires": {"measure"},
                },
            ),
        ],
        bases=(ShellSpec,),
    )

    output_spec = SpecInfo(
        name="MRISPreprocOutput",
        fields=[],
        bases=(ShellOutSpec,),
    )

    executable = "mris_preproc"
