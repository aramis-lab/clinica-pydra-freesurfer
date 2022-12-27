import os
import typing as ty

from pydra.engine.specs import ShellOutSpec, ShellSpec, SpecInfo

from pydra import ShellCommandTask

__all__ = ["ReconAll"]


class ReconAll(ShellCommandTask):
    """Task for FreeSurfer's recon-all.

    Fully automatic structural imaging stream for processing cross-sectional and longitudinal data.

    Examples
    --------
    Cross-sectional processing:

    By default, FreeSurfer writes its output to a directory defined through the `$SUBJECTS_DIR` environment variable.
    It can be overridden using the `subjects_dir` argument:

    >>> task = ReconAll(
    ...     directive="all",
    ...     subject_id="sub-P01",
    ...     subjects_dir="/path/to/subjects/dir",
    ... )
    >>> task.cmdline  # doctest: +ELLIPSIS
    'recon-all ... -sd /path/to/subjects/dir'

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
    ...     base_template_id="longbase",
    ...     base_timepoint_ids=["tp1", "tp2"],
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

    @staticmethod
    def get_output_subject_id(inputs) -> str:
        # Returns the output subject identifier depending on the workflow.
        return (
            # Cross-sectional case
            inputs.subject_id
            # Longitudinal template case
            or inputs.base_template_id
            # Longitudinal timepoint case
            or f"{inputs.longitudinal_timepoint_id}.long.{inputs.longitudinal_template_id}"
        )

    @staticmethod
    def get_output_subjects_dir(inputs) -> str:
        # Returns the default FreeSurfer's subjects directory unless overridden.
        return os.fspath(inputs.subjects_dir or os.getenv("SUBJECTS_DIR"))

    DIRECTIVES = {
        # All steps.
        "all",
        # Steps 1 to 5.
        "autorecon1",
        # Steps 6 to 23.
        "autorecon2",
        # Steps 12 to 23.
        "autorecon2-cp",
        # Steps 15 to 23.
        "autorecon2-wm",
        # Steps 21 to 23.
        "autorecon2-pial",
        # Steps 24 to 31.
        "autorecon3",
    }

    input_spec = SpecInfo(
        name="ReconAllInput",
        fields=[
            (
                "directive",
                str,
                {
                    "help_string": "process directive",
                    "mandatory": True,
                    "argstr": "-{directive}",
                    "allowed_values": DIRECTIVES,
                    "position": 0,
                },
            ),
            (
                "subject_id",
                str,
                {
                    "help_string": "subject identifier",
                    "mandatory": True,
                    "argstr": "-subjid {subject_id}",
                    "xor": ["base_template_id", "longitudinal_timepoint_id"],
                },
            ),
            (
                "t1_volume",
                os.PathLike,
                {
                    "help_string": "input T1 volume",
                    "argstr": "-i {t1_volume}",
                    "xor": ["t1_volumes"],
                },
            ),
            (
                "t1_volumes",
                ty.Iterable[os.PathLike],
                {
                    "help_string": "input T1 volumes",
                    "argstr": "-i...",
                    "xor": ["t1_volume"],
                },
            ),
            (
                "t2_volume",
                os.PathLike,
                {
                    "help_string": "input T2 volume",
                    "argstr": "-t2 {t2_volume}",
                },
            ),
            (
                "flair_volume",
                os.PathLike,
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
                    "mandatory": True,
                    "argstr": "-long {longitudinal_timepoint_id} {longitudinal_template_id}",
                    "requires": ["longitudinal_template_id"],
                    "xor": ["subject_id", "base_template_id"],
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
                "base_template_id",
                str,
                {
                    "help_string": "base template identifier",
                    "mandatory": True,
                    "argstr": "-base {base_template_id}",
                    "xor": ["subject_id", "longitudinal_timepoint_id"],
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
                os.PathLike,
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
            (
                "subjects_dir",
                os.PathLike,
                {
                    "help_string": "subjects directory processed by FreeSurfer",
                    "argstr": "-sd {subjects_dir}",
                },
            ),
        ],
        bases=(ShellSpec,),
    )

    output_spec = SpecInfo(
        name="ReconAllOutput",
        fields=[
            (
                "subject_id",
                str,
                {
                    "help_string": "subject identifier where outputs are written",
                    "callable": get_output_subject_id,
                },
            ),
            (
                "subjects_dir",
                str,
                {
                    "help_string": "subjects directory processed by FreeSurfer",
                    "callable": get_output_subjects_dir,
                },
            ),
        ],
        bases=(ShellOutSpec,),
    )

    executable = "recon-all"
