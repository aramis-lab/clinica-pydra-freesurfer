"""
CATrain
=======

Examples
--------

>>> task = CATrain(
...     hemisphere="lh",
...     canonical_surface="sphere.reg",
...     annotation_file="my_manual_labeling",
...     subject_ids=["subj1", "subj2"],
...     parcellation_table="colortable.txt",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'mris_ca_train -orig smoothwm -t colortable.txt -n 2 \
lh sphere.reg my_manual_labeling subj1 subj2 ...lh.my_atlas.gcs'
"""

__all__ = ["CATrain"]

from os import PathLike
from typing import Sequence

from attrs import define, field

from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask
from pydra.tasks.freesurfer import specs


@define(slots=False, kw_only=True)
class CATrainSpec(ShellSpec):
    """Specifications for mris_ca_train."""

    hemisphere: str = field(
        metadata={
            "help_string": "process left or right hemisphere",
            "mandatory": True,
            "argstr": "",
            "position": -5,
            "allowed_values": {"lh", "rh"},
        }
    )

    canonical_surface: PathLike = field(
        metadata={"help_string": "canonical surface", "mandatory": True, "argstr": "", "position": -4}
    )

    annotation_file: PathLike = field(
        metadata={"help_string": "annotation file", "mandatory": True, "argstr": "", "position": -3}
    )

    subject_ids: Sequence[str] = field(
        metadata={"help_string": "subject identifiers", "mandatory": True, "argstr": "...", "position": -2}
    )

    output_surface_atlas: str = field(
        metadata={
            "help_string": "output surface atlas file",
            "argstr": "",
            "position": -1,
            "output_file_template": "{hemisphere}.my_atlas.gcs",
        }
    )

    subjects_dir: str = field(metadata={"help_string": "subjects directory", "argstr": "-sdir"})

    original_surface: str = field(
        default="smoothwm",
        metadata={"help_string": "original surface", "argstr": "-orig"},
    )

    parcellation_table: str = field(metadata={"help_string": "parcellation table", "argstr": "-t"})

    num_subjects: int = field(
        metadata={
            "help_string": "number of input subjects to process",
            "formatter": lambda subject_ids: f"-n {len(subject_ids)}",
            "readonly": True,
        }
    )


class CATrain(ShellCommandTask):
    """Task definition for mris_ca_train."""

    executable = "mris_ca_train"

    input_spec = SpecInfo(name="Input", bases=(CATrainSpec,))

    output_spec = SpecInfo(name="Output", bases=(specs.SubjectsDirOutSpec,))
