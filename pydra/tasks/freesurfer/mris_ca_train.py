"""
MRISCATrain
===========

Examples
--------

>>> task = MRISCATrain(
...     hemisphere="lh",
...     canonical_surface_file="sphere.reg",
...     annotation_file="my_manual_labeling",
...     subject_ids=["subj1", "subj2"],
...     parcellation_table_file="colortable.txt",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'mris_ca_train -orig smoothwm -t colortable.txt -n 2 \
lh sphere.reg my_manual_labeling subj1 subj2 ...lh.my_atlas.gcs'
"""

import typing as ty

import attrs

import pydra

from . import specs

__all__ = ["MRISCATrain"]


@attrs.define(slots=False, kw_only=True)
class MRISCATrainSpec(pydra.specs.ShellSpec):
    """Specifications for mris_ca_train."""

    hemisphere: str = attrs.field(
        metadata={
            "help_string": "left or right hemisphere",
            "mandatory": True,
            "argstr": "",
            "position": -5,
            "allowed_values": {"lh", "rh"},
        }
    )

    canonical_surface_file: str = attrs.field(
        metadata={
            "help_string": "canonical surface file",
            "mandatory": True,
            "argstr": "",
            "position": -4,
        }
    )

    annotation_file: str = attrs.field(
        metadata={
            "help_string": "per-subject annotation file",
            "mandatory": True,
            "argstr": "",
            "position": -3,
        }
    )

    subject_ids: ty.Iterable[str] = attrs.field(
        metadata={
            "help_string": "subject to process",
            "mandatory": True,
            "argstr": "...",
            "position": -2,
        }
    )

    output_surface_atlas_file: str = attrs.field(
        metadata={
            "help_string": "output surface atlas file",
            "argstr": "",
            "position": -1,
            "output_file_template": "{hemisphere}.my_atlas.gcs",
        }
    )

    subjects_dir: str = attrs.field(
        metadata={
            "help_string": "subjects directory",
            "argstr": "-sdir",
        }
    )

    original_surface_file: str = attrs.field(
        default="smoothwm",
        metadata={
            "help_string": "original surface file",
            "argstr": "-orig",
        },
    )

    parcellation_table_file: str = attrs.field(
        metadata={
            "help_string": "parcellation table file",
            "argstr": "-t",
        }
    )

    number_of_subjects: int = attrs.field(
        metadata={
            "help_string": "number of input subjects to process",
            "formatter": lambda subject_ids: f"-n {len(subject_ids)}",
        }
    )


class MRISCATrain(pydra.ShellCommandTask):
    """Task for mris_ca_train."""

    input_spec = pydra.specs.SpecInfo(
        name="MRISCATrainInput",
        bases=(MRISCATrainSpec,),
    )

    output_spec = pydra.specs.SpecInfo(
        name="MRISCATrainOuput",
        bases=(specs.SubjectsDirOutSpec,),
    )

    executable = "mris_ca_train"
