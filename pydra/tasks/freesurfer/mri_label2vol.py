"""
MRILabel2Vol
============

Converts a label or a set of labels to a volume.

For a single label,
the output volume will be binary:
1 where the label is and 0 where it is not.

For multiple labels,
the output volume will be 0 where no labels were found,
otherwise the value will be the label number.

For a voxel to be assigned a label,
it must have enough hits in the voxel (threshold parameter)
and more hits than any other label.

Examples
--------

1. Convert a label to a binary mask in the functional space.
Require that a functional voxel be filled at least 50% by the label.

>>> task = MRILabel2Vol(
...     label_file="lh-avg_central_sulcus.label",
...     template_volume_file="f.nii.gz",
...     registration_file="register.dat",
...     threshold=0.5,
...     output_volume_file="cent-lh.nii.gz",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'mri_label2vol --label lh-avg_central_sulcus.label --temp f.nii.gz --reg register.dat --fillthresh 0.5 \
--o cent-lh.nii.gz'

2. Convert a surface label into a binary mask in the functional space.
Fill in all the cortical gray matter.
Require that a functional voxel be filled at least 30% by the label.

>>> task = MRILabel2Vol(
...     label_file="lh-avg_central_sulcus.label",
...     template_volume_file="f.nii.gz",
...     registration_file="register.dat",
...     threshold=0.3,
...     projection=["frac", 0, 1, 0.1],
...     subject_id="bert",
...     hemisphere="lh",
...     output_volume_file="cent-lh.nii.gz",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'mri_label2vol --label lh-avg_central_sulcus.label --temp f.nii.gz --reg register.dat --fillthresh 0.3 \
--proj frac 0 1 0.1 --subject bert --hemi lh --o cent-lh.nii.gz'

3. Convert a surface label into a binary mask in the functional space.
Sample a 1mm ribbon 2mm below the gray / white surface.
Do not require a fill threshold.

>>> task = MRILabel2Vol(
...     label_file="lh-avg_central_sulcus.label",
...     template_volume_file="f.nii.gz",
...     registration_file="register.dat",
...     projection=["abs", -3, -2, 0.1],
...     subject_id="bert",
...     hemisphere="lh",
...     output_volume_file="cent-lh.nii.gz",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'mri_label2vol --label lh-avg_central_sulcus.label --temp f.nii.gz --reg register.dat --proj abs -3 -2 0.1 \
--subject bert --hemi lh --o cent-lh.nii.gz'

4. Convert two labels into a volume in the same space as the labels.
The voxels corresponding to lh-avg_central_sulcus.label will have a value of 1
whereas those assigned to lh-avg_calcarine_sulcus.label will have a value of 2.

>>> task = MRILabel2Vol(
...     label_files=["lh-avg_central_sulcus.label", "lh-avg_calcarine_sulcus.label"],
...     template_volume_file="$SUBJECTS_DIR/bert/orig",
...     no_registration=True,
...     output_volume_file="cent_calc.img",
... )
>>> task.cmdline
'mri_label2vol --label lh-avg_central_sulcus.label --label lh-avg_calcarine_sulcus.label \
--temp $SUBJECTS_DIR/bert/orig --identity --o cent_calc.img'

"""
import os
import typing as ty

import attrs

import pydra

from . import specs

__all__ = ["MRILabel2Vol"]


@attrs.define(slots=False, kw_only=True)
class MRILabel2VolSpec(pydra.specs.ShellSpec):
    """Specifications for mri_label2vol."""

    _input_file_fields = {
        "label_file",
        "label_files",
        "annotation_file",
        "segmentation_file",
    }

    label_file: os.PathLike = attrs.field(
        metadata={
            "help_string": "label file",
            "mandatory": True,
            "argstr": "--label",
            "xor": _input_file_fields,
        }
    )

    label_files: ty.List[os.PathLike] = attrs.field(
        metadata={
            "help_string": "label files",
            "mandatory": True,
            "argstr": "--label ...",
            "xor": _input_file_fields,
        }
    )

    annotation_file: os.PathLike = attrs.field(
        metadata={
            "help_string": "annotation file",
            "mandatory": True,
            "argstr": "--annot",
            "xor": _input_file_fields,
        }
    )

    segmentation_file: os.PathLike = attrs.field(
        metadata={
            "help_string": "segmentation file",
            "mandatory": True,
            "argstr": "--seg",
            "xor": _input_file_fields,
        }
    )

    template_volume_file: os.PathLike = attrs.field(
        metadata={
            "help_string": "template volume file",
            "mandatory": True,
            "argstr": "--temp",
        }
    )

    registration_file: os.PathLike = attrs.field(
        metadata={
            "help_string": "map label coordinates to the template volume",
            "argstr": "--reg",
            "xor": {"no_registration"},
        }
    )

    threshold: float = attrs.field(
        metadata={
            "help_string": "threshold value at which a voxel may be considered for membership to a label",
            "argstr": "--fillthresh",
        }
    )

    projection: ty.Tuple[str, float, float, float] = attrs.field(
        metadata={
            "help_string": "projection along the surface normal as (type, start, stop, delta).",
            "argstr": "--proj",
            "requires": {"subject_id", "hemisphere"},
        }
    )

    subject_id: str = attrs.field(
        metadata={
            "help_string": "subject identifier to load the surface from",
            "argstr": "--subject",
        }
    )

    hemisphere: str = attrs.field(
        metadata={
            "help_string": "load surface for this hemisphere",
            "argstr": "--hemi",
            "allowed_values": ["lh", "rh"],
        }
    )

    no_registration: bool = attrs.field(
        metadata={
            "help_string": "use the identity matrix for registration",
            "argstr": "--identity",
            "xor": {"registration_file"},
        }
    )

    output_volume_file: str = attrs.field(
        metadata={
            "help_string": "output volume file in any format supported by mri_convert",
            "argstr": "--o",
        }
    )


class MRILabel2Vol(pydra.engine.ShellCommandTask):
    """Task definition for mri_label2vol."""

    input_spec = pydra.specs.SpecInfo(
        name="MRILabel2VolInput",
        bases=(MRILabel2VolSpec, specs.SubjectsDirSpec),
    )

    output_spec = pydra.specs.SpecInfo(
        name="MRILabel2VolOutput",
        bases=(specs.SubjectsDirOutSpec,),
    )

    executable = "mri_label2vol"
