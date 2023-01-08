"""
MRIAnatomicalStats
==================

Computes a number of anatomical properties.

Examples
--------

>>> task = MRIAnatomicalStats(
...     subject_id="subjid",
...     hemisphere="lh",
...     annotation_file="subjid/label/lh.aparc.annot",
...     format_stdout_as_table=True,
... )
>>> task.cmdline
'mris_anatomical_stats -a subjid/label/lh.aparc.annot -b subjid lh'

>>> task = MRIAnatomicalStats(
...     subject_id="subjid",
...     hemisphere="lh",
...     label_file="lh.cortex.label",
...     format_stdout_as_table=True,
... )
>>> task.cmdline
'mris_anatomical_stats -l lh.cortex.label -b subjid lh'
"""

import attrs

import pydra

from . import specs

__all__ = ["MRIAnatomicalStats"]


@attrs.define(slots=False, kw_only=True)
class MRIAnatomicalStatsSpec(pydra.specs.ShellSpec):
    """Specifications for mri_anatomical_stats."""

    subject_id: str = attrs.field(
        metadata={
            "help_string": "subject to process",
            "mandatory": True,
            "argstr": "",
            "position": -2,
        }
    )

    hemisphere: str = attrs.field(
        metadata={
            "help_string": "left or right hemisphere",
            "mandatory": True,
            "argstr": "",
            "position": -1,
            "allowed_values": {"lh", "rh"},
        }
    )

    label_file: str = attrs.field(
        metadata={
            "help_string": "restrict computation to the specified label",
            "argstr": "-l",
        }
    )

    annotation_file: str = attrs.field(
        metadata={
            "help_string": "compute statistics for each annotation in this file",
            "argstr": "-a",
        }
    )

    format_stdout_as_table: bool = attrs.field(
        metadata={
            "help_string": "write to stdout in table format",
            "argstr": "-b",
        }
    )

    output_table_file = attrs.field(
        metadata={
            "help_string": "write table output to this file",
            "argstr": "-f",
        }
    )

    output_stats_file = attrs.field(
        metadata={
            "help_string": "write stats output to this file",
            "argstr": "-log",
        }
    )

    subjects_dir: str = attrs.field(
        metadata={
            "help_string": "subjects directory",
            "argstr": "-sdir",
        }
    )


class MRIAnatomicalStats(pydra.engine.ShellCommandTask):
    """Task for mri_annatomical_stats."""

    input_spec = pydra.specs.SpecInfo(
        name="MRIAnnatomicalStatsInput",
        bases=(MRIAnatomicalStatsSpec,),
    )

    output_spec = pydra.specs.SpecInfo(
        name="MRIAnnatomicalStatsOutput",
        bases=(specs.SubjectsDirOutSpec,),
    )

    executable = "mris_anatomical_stats"
