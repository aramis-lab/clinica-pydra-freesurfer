from typing import List, Tuple

from pydra.engine.specs import ShellOutSpec, ShellSpec, SpecInfo

from pydra import ShellCommandTask

__all__ = ("ReconAll",)


input_fields = [
    (
        "subject",
        str,
        {
            "help_string": "subject identifier",
            "argstr": "-s {subject}",
        },
    ),
    (
        "base_subject",
        str,
        {
            "help_string": "base subject template",
            "argstr": "-base {base_subject}",
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
        "timepoints",
        List[str],
        {
            "help_string": "timepoints",
            "argstr": "-tp...",
        },
    ),
    (
        "subject_dir",
        str,
        {
            "help_string": "subject directory",
            "argstr": "-sd {subject_dir}",
        },
    ),
    (
        "t1_volume",
        str,
        {
            "help_string": "input T1 volume",
            "argstr": "-i {t1_input}",
        },
    ),
    (
        "t2_volume",
        str,
        {
            "help_string": "input T2 volume",
            "argstr": "-t2 {t2_input}",
        },
    ),
    (
        "flair_volume",
        str,
        {
            "help_string": "input FLAIR volume",
            "argstr": "-flair {flair_input}",
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
        "directive",
        str,
        {
            "help_string": "workflow directive",
            "argstr": "-{directive}",
            "allowed_values": ["all"],
            "position": -1,
        },
    ),
]

recon_all_input_spec = SpecInfo(name="Input", fields=input_fields, bases=(ShellSpec,))

output_fields = []

recon_all_output_spec = SpecInfo(
    name="Output", fields=output_fields, bases=(ShellOutSpec,)
)


class ReconAll(ShellCommandTask):
    """Task for FreeSurfer's recon-all pipeline.

    Fully automatic structural imaging stream for processing cross-sectional and longitudinal data.

    Examples
    --------
    >>> task = ReconAll(directive="all", subject="tpNid", t1_volume="path_to_tpN_dcm")
    >>> task.cmdline
    'recon-all -s tpNid -i path_to_tpN_dcm -all'
    >>> task = ReconAll(directive="all", base_subject="templateid", timepoints=["tp1id", "tp2id"])
    >>> task.cmdline
    'recon-all -base templateid -tp tp1id -tp tp2id -all'
    >>> task = ReconAll(
    ...    directive="all",
    ...    longitudinal_timepoint_id="tpNid",
    ...    longitudinal_template_id="templateid",
    ... )
    >>> task.cmdline
    'recon-all -long tpNid templateid -all'
    """

    input_spec = recon_all_input_spec
    output_spec = recon_all_output_spec
    executable = "recon-all"
