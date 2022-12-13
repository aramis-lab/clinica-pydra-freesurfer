import typing as ty

from pydra.engine.specs import ShellOutSpec, ShellSpec, SpecInfo

from pydra import ShellCommandTask

__all__ = ["ReconAll"]


class ReconAll(ShellCommandTask):
    """Task for FreeSurfer's recon-all.

    Fully automatic structural imaging stream for processing cross-sectional and longitudinal data.

    Examples
    --------
    Longitudinal processing:

    1. Cross-sectionally process tpN subjects (the default workflow):

    >>> task = ReconAll(
    ...     directive="all",
    ...     subject_id="tp1",
    ...     t1_volume="/path/to/tp1.dcm"
    ... )
    >>> task.cmdline
    'recon-all -all -subjid tp1 -i /path/to/tp1.dcm'

    2. Create and process the unbiased base (subject template):

    >>> task = ReconAll(
    ...     directive="all",
    ...     base_subject_id="longbase",
    ...     base_timepoint_ids=["tp1", "tp2"]
    ... )
    >>> task.cmdline
    'recon-all -all -base longbase -base-tp tp1 -base-tp tp2'

    3. Longitudinally process tpN subjects:

    >>> task = ReconAll(
    ...    directive="all",
    ...    longitudinal_timepoint_id="tp1",
    ...    longitudinal_template_id="longbase",
    ... )
    >>> task.cmdline
    'recon-all -all -long tp1 longbase'
    """

    input_spec = SpecInfo(
        name="ReconAllInput",
        fields=[
            (
                "directive",
                str,
                {
                    "help_string": "process directive",
                    "argstr": "-{directive}",
                    "allowed_values": ["all"],
                    "position": 0,
                },
            ),
            (
                "subject_id",
                str,
                {
                    "help_string": "subject identifier",
                    "argstr": "-subjid {subject_id}",
                },
            ),
            (
                "subjects_dir",
                str,
                {
                    "help_string": "user defined SUBJECTS_DIR",
                    "argstr": "-sd {subjects_dir}",
                },
            ),
            (
                "t1_volume",
                str,
                {
                    "help_string": "input T1 volume",
                    "argstr": "-i {t1_volume}",
                    "xor": ["t1_volumes"],
                },
            ),
            (
                "t1_volumes",
                ty.Iterable[str],
                {
                    "help_string": "input T1 volumes",
                    "argstr": "-i...",
                    "xor": ["t1_volume"],
                },
            ),
            (
                "t2_volume",
                str,
                {
                    "help_string": "input T2 volume",
                    "argstr": "-t2 {t2_volume}",
                },
            ),
            (
                "flair_volume",
                str,
                {
                    "help_string": "input FLAIR volume",
                    "argstr": "-flair {flair_volume}",
                },
            ),
            (
                "longitudinal_timepoint_id",
                str,
                {
                    "help_string": "longitudinal timepoint identifier",
                    "argstr": "-long {longitudinal_timepoint_id} {longitudinal_template_id}",
                    "requires": ["longitudinal_template_id"],
                },
            ),
            (
                "longitudinal_template_id",
                str,
                {
                    "help_string": "longitudinal template identifier",
                    "argstr": None,
                    "requires": ["longitudinal_timepoint_id"],
                },
            ),
            (
                "base_subject_id",
                str,
                {
                    "help_string": "base subject template",
                    "argstr": "-base {base_subject_id}",
                },
            ),
            (
                "base_timepoint_ids",
                ty.Iterable[str],
                {
                    "help_string": "base timepoint identifiers",
                    "argstr": "-base-tp...",
                },
            ),
            (
                "custom_mask_input",
                str,
                {
                    "help_string": "input custom brain mask",
                    "argstr": "-xmask {custom_mask_input}",
                },
            ),
            (
                "hemisphere",
                str,
                {
                    "help_string": "restrict processing to this hemisphere",
                    "argstr": "-hemi {hemisphere}",
                    "allowed_values": ["lh", "rh"],
                },
            ),
            (
                "parallel",
                bool,
                {
                    "help_string": "process both hemispheres in parallel",
                    "argstr": "-parallel",
                    "xor": ["hemisphere"],
                },
            ),
            (
                "threads",
                int,
                {
                    "help_string": "set number of threads to use",
                    "argstr": "-threads {threads}",
                },
            ),
        ],
        bases=(ShellSpec,),
    )

    output_spec = SpecInfo(
        name="ReconAllOutput",
        fields=[],
        bases=(ShellOutSpec,),
    )

    executable = "recon-all"
