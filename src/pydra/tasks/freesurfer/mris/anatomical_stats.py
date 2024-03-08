"""
AnatomicalStats
===============

Computes a number of anatomical properties.

Examples
--------

>>> task = AnatomicalStats(subject_id="subjid", hemisphere="lh", annotation_file="lh.aparc.annot")
>>> task.cmdline    # doctest: +ELLIPSIS
'mris_anatomical_stats -a lh.aparc.annot -f ...lh.white.stats -log ...lh.white.log subjid lh white'

>>> task = AnatomicalStats(subject_id="subjid", hemisphere="lh", label_file="lh.cortex.label")
>>> task.cmdline    # doctest: +ELLIPSIS
'mris_anatomical_stats -l lh.cortex.label -f ...lh.white.stats -log ...lh.white.log subjid lh white'
"""

__all__ = ["AnatomicalStats"]

from os import PathLike

from attrs import define, field

from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask
from pydra.tasks.freesurfer import specs


@define(slots=False, kw_only=True)
class AnatomicalStatsSpec(ShellSpec):
    """Specifications for mris_anatomical_stats."""

    subject_id: str = field(
        metadata={"help_string": "subject identifier", "mandatory": True, "argstr": "", "position": -3}
    )

    hemisphere: str = field(
        metadata={
            "help_string": "process left or right hemisphere",
            "mandatory": True,
            "argstr": "",
            "position": -2,
            "allowed_values": {"lh", "rh"},
        }
    )

    surface_name: str = field(default="white", metadata={"help_string": "surface name", "argstr": "", "position": -1})

    label_file: PathLike = field(
        metadata={"help_string": "restrict computation to each label in this file", "argstr": "-l"}
    )

    annotation_file: PathLike = field(
        metadata={"help_string": "compute statistics for each annotation in this file", "argstr": "-a"}
    )

    output_stats_file: str = field(
        metadata={
            "help_string": "output stats file in table format",
            "argstr": "-f",
            "output_file_template": "{hemisphere}.{surface_name}.stats",
        }
    )

    output_log_file: str = field(
        metadata={
            "help_string": "output stats file in log format",
            "argstr": "-log",
            "output_file_template": "{hemisphere}.{surface_name}.log",
        }
    )

    output_colortable_file: PathLike = field(
        metadata={
            "help_string": "write colortable for annotations",
            "argstr": "-c",
            "requires": {"annotation_file"},
        }
    )

    no_global_stats: bool = field(
        metadata={"help_string": "do not write global stats", "argstr": "-noglobal", "requires": {"output_stats_file"}}
    )

    no_header: bool = field(
        metadata={"help_string": "do not write a header", "argstr": "-noheader", "requires": {"output_log_file"}}
    )

    subjects_dir: str = field(metadata={"help_string": "subjects directory", "argstr": "-sdir"})


class AnatomicalStats(ShellCommandTask):
    """Task definition for mris_anatomical_stats."""

    executable = "mris_anatomical_stats"

    input_spec = SpecInfo(name="Input", bases=(AnatomicalStatsSpec,))

    output_spec = SpecInfo(name="Output", bases=(specs.SubjectsDirOutSpec,))
