"""
MRISCALabel
===========

Assign an anatomical label to each cortical surface vertex.

Examples
--------

>>> task = MRISCALabel(
...     subject_id="my_subject",
...     hemisphere="lh",
...     canonical_surface_file="sphere.reg",
...     surface_atlas_file="lh.rahul.gcs",
...     original_surface_file="white",
...     no_covariance=True,
...     parcellation_table_file="colortable.txt",
...     atlas_name="rahul",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'mris_ca_label -orig white -novar -t colortable.txt \
my_subject lh sphere.reg lh.rahul.gcs ...lh.rahul.annot'
"""

import attrs

import pydra

from . import specs

__all__ = ["MRISCALabel"]


@attrs.define(slots=False, kw_only=True)
class MRISCALabelSpec(pydra.specs.ShellSpec):
    """Specifications for mris_ca_label."""

    subject_id: str = attrs.field(
        metadata={
            "help_string": "subject to process",
            "mandatory": True,
            "argstr": "",
            "position": -5,
        }
    )

    hemisphere: str = attrs.field(
        metadata={
            "help_string": "left or right hemisphere",
            "mandatory": True,
            "argstr": "",
            "position": -4,
            "allowed_values": {"lh", "rh"},
        }
    )

    canonical_surface_file: str = attrs.field(
        metadata={
            "help_string": "canonical surface file",
            "mandatory": True,
            "argstr": "",
            "position": -3,
        }
    )

    surface_atlas_file: str = attrs.field(
        metadata={
            "help_string": "surface atlas file",
            "mandatory": True,
            "argstr": "",
            "position": -2,
        }
    )

    atlas_name: str = attrs.field(
        default="atlas",
        metadata={"help_string": "atlas name"},
    )

    output_annotation_file: str = attrs.field(
        metadata={
            "help_string": "output surface annotation file",
            "argstr": "",
            "position": -1,
            "output_file_template": "{hemisphere}.{atlas_name}.annot",
        }
    )

    subjects_dir: str = attrs.field(
        metadata={
            "help_string": "subjects directory",
            "argstr": "-sdir",
        }
    )

    aseg_volume_file: str = attrs.field(
        metadata={
            "help_string": "use aseg volume to correct midline",
            "argstr": "-aseg",
        }
    )

    original_surface_file: str = attrs.field(
        default="smoothwm",
        metadata={
            "help_string": "original surface file",
            "argstr": "-orig",
        },
    )

    no_covariance: bool = attrs.field(
        metadata={
            "help_string": "set covariance matrices to identity",
            "argstr": "-novar",
        }
    )

    parcellation_table_file: str = attrs.field(
        metadata={
            "help_string": "parcellation table file",
            "argstr": "-t",
        }
    )

    cortex_label_file: str = attrs.field(
        metadata={
            "help_string": "cortex label file",
            "argstr": "-l",
        }
    )


class MRISCALabel(pydra.ShellCommandTask):
    """Task for mris_ca_label."""

    input_spec = pydra.specs.SpecInfo(
        name="MRISCALabelInput",
        bases=(MRISCALabelSpec,),
    )

    output_spec = pydra.specs.SpecInfo(
        name="MRISCALabelOuput",
        bases=(specs.SubjectsDirOutSpec,),
    )

    executable = "mris_ca_label"
