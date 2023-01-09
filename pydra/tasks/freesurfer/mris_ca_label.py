"""
MRISCaLabel
===========

Assign an anatomical label to each cortical surface vertex.

Examples
--------

In this example, mris_ca_label takes sphere.reg as the canonical surface input file,
lh.rahul.gcs as the classifier array input file, and writes the annotated surface info
to lh.raparc.annot. The file colortable_final.txt is embedded into the output file, so
that tksurfer (and other utilities) can read it in.

>>> task = MRISCaLabel(
...     subject_id="my_subject",
...     hemisphere="lh",
...     canonical_surface_file="sphere.reg",
...     classifier_array_file="$SUBJECTS_DIR/average/lh.rahul.gcs",
...     output_annotation_file="$SUBJECTS_DIR/my_subject/label/lh.raparc.annot",
...     original_surface_file="white",
...     no_covariance=True,
...     parcellation_table_file="$SUBJECTS_DIR/scripts/colortable_final.txt",
... )
>>> task.cmdline
'mris_ca_label -orig white -novar -t $SUBJECTS_DIR/scripts/colortable_final.txt \
my_subject lh sphere.reg $SUBJECTS_DIR/average/lh.rahul.gcs \
$SUBJECTS_DIR/my_subject/label/lh.raparc.annot'
"""

import attrs

import pydra

from . import specs

__all__ = ["MRISCaLabel"]


@attrs.define(slots=False, kw_only=True)
class MRISCaLabelSpec(pydra.specs.ShellSpec):
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

    canonical_surface_file = attrs.field(
        metadata={
            "help_string": "canonical surface file",
            "mandatory": True,
            "argstr": "",
            "position": -3,
        }
    )

    classifier_array_file = attrs.field(
        metadata={
            "help_string": "classifier array file",
            "mandatory": True,
            "argstr": "",
            "position": -2,
        }
    )

    output_annotation_file = attrs.field(
        metadata={
            "help_string": "output surface annotation file",
            "mandatory": True,
            "argstr": "",
            "position": -1,
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

    no_covariance: bool = attrs.field(
        metadata={
            "help_string": "set all covariance matrices to identify",
            "argstr": "-novar",
        }
    )

    parcellation_table_file = attrs.field(
        metadata={
            "help_string": "parcellation table file",
            "argstr": "-t",
        }
    )


class MRISCaLabel(pydra.ShellCommandTask):
    """Task for mris_ca_label."""

    input_spec = pydra.specs.SpecInfo(
        name="MRISCaLabelInput",
        bases=(MRISCaLabelSpec,),
    )

    output_spec = pydra.specs.SpecInfo(
        name="MRISCaLabelOuput",
        bases=(specs.SubjectsDirOutSpec,),
    )

    executable = "mris_ca_label"
