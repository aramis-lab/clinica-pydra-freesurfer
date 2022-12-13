import typing as ty

from pydra.engine.specs import ShellOutSpec, ShellSpec, SpecInfo

from pydra import ShellCommandTask

__all__ = ["ReconAll"]


class ReconAll(ShellCommandTask):
    """Task for FreeSurfer's recon-all.

    Fully automatic structural imaging stream for processing cross-sectional and longitudinal data.

    Examples
    --------
    >>> task = ReconAll(directive="all", subject_id="tpnid", t1_volume="/path/to/tpn.dcm")
    >>> task.cmdline
    'recon-all -all -subjid tpnid -i /path/to/tpn.dcm'
    >>> task = ReconAll(
    ...     directive="all",
    ...     base_subject_id="templateid",
    ...     base_timepoint_ids=["tp1id", "tp2id"],
    ... )
    >>> task.cmdline
    'recon-all -all -base templateid -tp tp1id -tp tp2id'
    >>> task = ReconAll(
    ...    directive="all",
    ...    longitudinal_timepoint_id="tpnid",
    ...    longitudinal_template_id="templateid",
    ... )
    >>> task.cmdline
    'recon-all -all -long tpnid templateid'
    """

    input_spec = SpecInfo(
        name="ReconAllInput",
        fields=[
            # Required arguments.
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
                    "argstr": "-sd {subject_dir}",
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
                "base_timepoint_id",
                str,
                {
                    "help_string": "base time-point identifier",
                    "argstr": "-tp {base_timepoint_id}",
                    "xor": ["base_timepoint_ids"],
                },
            ),
            (
                "base_timepoint_ids",
                ty.Iterable[str],
                {
                    "help_string": "base time-point identifiers",
                    "argstr": "-tp...",
                    "xor": ["base_timepoint_id"],
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
        ],
        bases=(ShellSpec,),
    )

    output_spec = SpecInfo(
        name="ReconAllOutput",
        fields=[],
        bases=(ShellOutSpec,),
    )

    executable = "recon-all"
