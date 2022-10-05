from pydra.engine.specs import ShellOutSpec, ShellSpec, SpecInfo

from pydra import ShellCommandTask

__all__ = ["GTMSeg"]


class GTMSeg(ShellCommandTask):
    """Task for PETSurfer's gtmseg.

    Examples
    --------
    >>> task = GTMSeg(subject_id="subject")
    >>> task.cmdline
    'gtmseg --s subject'
    >>> task = GTMSeg(
    ...     subject_id="subject",
    ...     keep_hypointensities=True,
    ...     subsegment_white_matter=True,
    ...     output_volume="gtmseg.wmseg.hypo.mgz",
    ...     upsampling_factor=1,
    ... )
    >>> task.cmdline
    'gtmseg --s subject --o gtmseg.wmseg.hypo.mgz --usf 1 --keep-hypo --subsegwm'
    >>> task = GTMSeg(
    ...     subject_id="subject",
    ...     output_volume="gtmseg+myseg.mgz",
    ...     headseg="apas+head+myseg.mgz",
    ...     colortable="myseg.colortable.txt",
    ... )
    >>> task.cmdline
    'gtmseg --s subject --o gtmseg+myseg.mgz --head apas+head+myseg.mgz --ctab myseg.colortable.txt'
    """

    input_spec = SpecInfo(
        name="GTMSegInput",
        fields=[
            (
                "subjects_dir",
                str,
                {
                    "help_string": "user defined SUBJECTS_DIR",
                    "argstr": "--sd {subjects_dir}",
                },
            ),
            (
                "subject_id",
                str,
                {
                    "help_string": "subject to analyze",
                    "mandatory": True,
                    "argstr": "--s {subject_id}",
                },
            ),
            (
                "output_volume",
                str,
                {
                    "help_string": "output volume relative to subject's mri directory",
                    "argstr": "--o {output_volume}",
                },
            ),
            (
                "xcerseg",
                bool,
                {
                    "help_string": "generate headseg with xcerebralseg",
                    "argstr": "--xcerseg",
                    "xor": ["headseg"],
                },
            ),
            (
                "headseg",
                str,
                {
                    "help_string": "custom headseg",
                    "argstr": "--head {headseg}",
                    "xor": ["xcerseg"],
                },
            ),
            (
                "no_pons",
                bool,
                {
                    "help_string": "no pons segmentation with xcerebralseg",
                    "argstr": "--no-pons",
                    "requires": ["xcerseg"],
                },
            ),
            (
                "no_vermis",
                bool,
                {
                    "help_string": "no vermis segmentation with xcerebralseg",
                    "argstr": "--no-vermis",
                    "requires": ["xcerseg"],
                },
            ),
            (
                "colortable",
                str,
                {
                    "help_string": "custom colortable",
                    "argstr": "--ctab {colortable}",
                },
            ),
            (
                "upsampling_factor",
                float,
                {
                    "help_string": "upsampling factor",
                    "argstr": "--usf {upsampling_factor}",
                },
            ),
            (
                "output_upsampling_factor",
                float,
                {
                    "help_string": "output upsampling factor (if different from upsampling factor)",
                    "argstr": "--output-usf {output_upsampling_factor}",
                },
            ),
            (
                "keep_hypointensities",
                bool,
                {
                    "help_string": "do not relabel hypointensities as white matter",
                    "argstr": "--keep-hypo",
                },
            ),
            (
                "keep_corpus_callosum",
                bool,
                {
                    "help_string": "do not relabel corpus callosum as white matter",
                    "argstr": "--keep-cc",
                },
            ),
            (
                "subsegment_white_matter",
                bool,
                {
                    "help_string": "subsegment white matter into lobes",
                    "argstr": "--subsegwm",
                },
            ),
        ],
        bases=(ShellSpec,),
    )

    output_spec = SpecInfo(
        name="GTMSegOutput",
        fields=[],
        bases=(ShellOutSpec,),
    )

    executable = "gtmseg"
