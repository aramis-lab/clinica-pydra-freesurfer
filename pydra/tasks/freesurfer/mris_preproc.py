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

    >>> source_subject_ids = [f"abc{s:02d}-anat" for s in range(1, 5)]

    1. Resample abcXX-anat/surf/lh.thickness onto fsaverage:

    >>> task = MRISPreproc(
    ...     source_subject_ids=source_subject_ids,
    ...     target_subject_id="fsaverage",
    ...     hemifield="lh",
    ...     measure="thickness",
    ...     output_file="abc-lh-thickness.mgh",
    ... )
    >>> task.cmdline
    'mris_preproc --out abc-lh-thickness.mgh --target fsaverage --hemi lh --meas thickness \
--s abc01-anat --s abc02-anat --s abc03-anat --s abc04-anat'

    2. Same as above but using a fsgd file (which would have the abcXXs as Inputs):

    >>> task = MRISPreproc(
    ...     fsgd_file="abc.fsgd",
    ...     target_subject_id="fsaverage",
    ...     hemifield="lh",
    ...     measure="thickness",
    ...     output_file="abc-lh-thickness.mgh",
    ... )
    >>> task.cmdline
    'mris_preproc --out abc-lh-thickness.mgh --target fsaverage --hemi lh --meas thickness --fsgd abc.fsgd'

    3. Same as #1 with additional smoothing by 5mm:

    >>> task = MRISPreproc(
    ...     source_subject_ids=source_subject_ids,
    ...     target_subject_id="fsaverage",
    ...     hemifield="lh",
    ...     measure="thickness",
    ...     output_file="abc-lh-thickness.sm5.mgh",
    ...     target_fwhm=5,
    ... )
    >>> task.cmdline
    'mris_preproc --out abc-lh-thickness.sm5.mgh --target fsaverage --hemi lh --meas thickness \
--s abc01-anat --s abc02-anat --s abc03-anat --s abc04-anat --fwhm 5'

    4. Same as #1 but using full paths.

    >>> task = MRISPreproc(
    ...     target_subject_id="fsaverage",
    ...     hemifield="lh",
    ...     output_file="abc-lh-thickness.mgh",
    ...     fsgd_file="abc.fsgd",
    ...     source_format="curv",
    ...     input_surface_paths=[f"abc{s:02d}-anat/surf/lh.thickness" for s in range(1, 5)],
    ... )
    >>> task.cmdline
    'mris_preproc --out abc-lh-thickness.mgh --target fsaverage --hemi lh --fsgd abc.fsgd \
--isp abc01-anat/surf/lh.thickness --isp abc02-anat/surf/lh.thickness --isp abc03-anat/surf/lh.thickness \
--isp abc04-anat/surf/lh.thickness --srcfmt curv'

    5. Same as #2 but computes paired differences.

    >>> task = MRISPreproc(
    ...     fsgd_file="abc.fsgd",
    ...     target_subject_id="fsaverage",
    ...     hemifield="lh",
    ...     measure="thickness",
    ...     output_file="abc-lh-thickness-pdiff.mgh",
    ...     paired_differences=True,
    ... )
    >>> task.cmdline
    'mris_preproc --out abc-lh-thickness-pdiff.mgh --target fsaverage --hemi lh --meas thickness --fsgd abc.fsgd \
--paired-diff'
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
                    "xor": {"fsgd_file"},
                },
            ),
            (
                "fsgd_file",
                str,
                {
                    "help_string": "fsgd file containing the list of input subjects",
                    "argstr": "--fsgd {fsgd_file}",
                    "xor": {"source_sibject_ids"},
                },
            ),
            (
                "input_surface_paths",
                ty.Iterable[str],
                {
                    "help_string": "full paths to input surface measure files",
                    "argstr": "--isp...",
                    "requires": {"fsgd_file"},
                },
            ),
            (
                "source_format",
                str,
                {
                    "help_string": "source format of input surface measure files",
                    "argstr": "--srcfmt {source_format}",
                    "requires": {"input_surface_paths"},
                },
            ),
            (
                "target_fwhm",
                float,
                {
                    "help_string": "smooth target surface data by fwhm mm",
                    "argstr": "--fwhm {target_fwhm}",
                },
            ),
            (
                "source_fwhm",
                float,
                {
                    "help_string": "smooth source surface data by fwhm mm",
                    "argstr": "--fwhm-src {source_fwhm}",
                },
            ),
            (
                "paired_differences",
                bool,
                {
                    "help_string": "compute paired differences",
                    "argstr": "--paired-diff",
                },
            ),
            (
                "subjects_dir",
                str,
                {
                    "help_string": "user defined subjects directory",
                    "argstr": "--SUBJECTS_DIR {subjects_dir}",
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
