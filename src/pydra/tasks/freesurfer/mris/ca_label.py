"""
CALabel
=======

Assign an anatomical label to each cortical surface vertex.

Examples
--------

>>> task = CALabel(
...     subject_id="my_subject",
...     hemisphere="lh",
...     canonical_surface="sphere.reg",
...     surface_atlas="lh.rahul.gcs",
...     original_surface="white",
...     no_covariance=True,
...     parcellation_table="colortable.txt",
...     atlas_name="rahul",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'mris_ca_label -orig white -novar -t colortable.txt \
my_subject lh sphere.reg lh.rahul.gcs ...lh.rahul.annot'
"""

__all__ = ["CALabel"]

from os import PathLike

from attrs import define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask

from .. import specs


@define(slots=False, kw_only=True)
class CALabelSpec(ShellSpec):
    """Specifications for mris_ca_label."""

    subject_id: str = field(
        metadata={
            "help_string": "subject to process",
            "mandatory": True,
            "argstr": "",
            "position": -5,
        }
    )

    hemisphere: str = field(
        metadata={
            "help_string": "process left or right hemisphere",
            "mandatory": True,
            "argstr": "",
            "position": -4,
            "allowed_values": {"lh", "rh"},
        }
    )

    canonical_surface: PathLike = field(
        metadata={
            "help_string": "canonical surface file",
            "mandatory": True,
            "argstr": "",
            "position": -3,
        }
    )

    surface_atlas: PathLike = field(
        metadata={
            "help_string": "surface atlas file",
            "mandatory": True,
            "argstr": "",
            "position": -2,
        }
    )

    atlas_name: str = field(default="atlas", metadata={"help_string": "atlas name"})

    output_annotation_file: str = field(
        metadata={
            "help_string": "output surface annotation file",
            "argstr": "",
            "position": -1,
            "output_file_template": "{hemisphere}.{atlas_name}.annot",
        }
    )

    subjects_dir: str = field(metadata={"help_string": "subjects directory", "argstr": "-sdir"})

    aseg_volume: PathLike = field(metadata={"help_string": "use aseg volume to correct midline", "argstr": "-aseg"})

    original_surface: str = field(default="smoothwm", metadata={"help_string": "original surface", "argstr": "-orig"})

    no_covariance: bool = field(metadata={"help_string": "set covariance matrices to identity", "argstr": "-novar"})

    parcellation_table: PathLike = field(metadata={"help_string": "parcellation table", "argstr": "-t"})

    cortex_label_file: PathLike = field(metadata={"help_string": "cortex label file", "argstr": "-l"})


class CALabel(ShellCommandTask):
    """Task definition for mris_ca_label."""

    executable = "mris_ca_label"

    input_spec = SpecInfo(name="Input", bases=(CALabelSpec,))

    output_spec = SpecInfo(name="Output", bases=(specs.SubjectsDirOutSpec,))
