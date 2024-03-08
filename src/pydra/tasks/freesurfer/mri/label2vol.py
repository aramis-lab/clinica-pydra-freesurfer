"""
Label2Vol
=========

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

>>> task = Label2Vol(
...     label_file="lh-avg_central_sulcus.label",
...     template_volume="f.nii.gz",
...     registration_file="register.dat",
...     threshold=0.5,
...     output_volume="cent-lh.nii.gz",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'mri_label2vol --label lh-avg_central_sulcus.label --temp f.nii.gz --reg register.dat --fillthresh 0.5 \
--o cent-lh.nii.gz'

2. Convert a surface label into a binary mask in the functional space.
Fill in all the cortical gray matter.
Require that a functional voxel be filled at least 30% by the label.

>>> task = Label2Vol(
...     label_file="lh-avg_central_sulcus.label",
...     template_volume="f.nii.gz",
...     registration_file="register.dat",
...     threshold=0.3,
...     projection=["frac", 0, 1, 0.1],
...     subject_id="bert",
...     hemisphere="lh",
...     output_volume="cent-lh.nii.gz",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'mri_label2vol --label lh-avg_central_sulcus.label --temp f.nii.gz --reg register.dat --fillthresh 0.3 \
--proj frac 0 1 0.1 --subject bert --o cent-lh.nii.gz --hemi lh'

3. Convert a surface label into a binary mask in the functional space.
Sample a 1mm ribbon 2mm below the gray / white surface.
Do not require a fill threshold.

>>> task = Label2Vol(
...     label_file="lh-avg_central_sulcus.label",
...     template_volume="f.nii.gz",
...     registration_file="register.dat",
...     projection=["abs", -3, -2, 0.1],
...     subject_id="bert",
...     hemisphere="lh",
...     output_volume="cent-lh.nii.gz",
... )
>>> task.cmdline  # doctest: +ELLIPSIS
'mri_label2vol --label lh-avg_central_sulcus.label --temp f.nii.gz --reg register.dat --proj abs -3 -2 0.1 \
--subject bert --o cent-lh.nii.gz --hemi lh'

4. Convert two labels into a volume in the same space as the labels.
The voxels corresponding to lh-avg_central_sulcus.label will have a value of 1
whereas those assigned to lh-avg_calcarine_sulcus.label will have a value of 2.

>>> task = Label2Vol(
...     label_files=["lh-avg_central_sulcus.label", "lh-avg_calcarine_sulcus.label"],
...     template_volume="$SUBJECTS_DIR/bert/orig",
...     no_registration=True,
...     output_volume="cent_calc.img",
... )
>>> task.cmdline
'mri_label2vol --label lh-avg_central_sulcus.label --label lh-avg_calcarine_sulcus.label \
--temp $SUBJECTS_DIR/bert/orig --identity --o cent_calc.img'

"""

__all__ = ["Label2Vol"]

from os import PathLike
from typing import Sequence, Tuple

from attrs import define, field

from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask
from pydra.tasks.freesurfer import specs


@define(kw_only=True)
class Label2VolSpec(ShellSpec):
    """Specifications for mri_label2vol."""

    _xor = frozenset(["label_file", "label_files", "annotation_file", "segmentation_file"])

    label_file: PathLike = field(
        metadata={"help_string": "label file", "mandatory": True, "argstr": "--label", "xor": _xor}
    )

    label_files: Sequence[PathLike] = field(
        metadata={"help_string": "label files", "mandatory": True, "argstr": "--label ...", "xor": _xor}
    )

    annotation_file: PathLike = field(
        metadata={"help_string": "annotation file", "mandatory": True, "argstr": "--annot", "xor": _xor}
    )

    segmentation_file: PathLike = field(
        metadata={"help_string": "segmentation file", "mandatory": True, "argstr": "--seg", "xor": _xor}
    )

    template_volume: PathLike = field(
        metadata={
            "help_string": "template volume file",
            "mandatory": True,
            "argstr": "--temp",
        }
    )

    registration_file: PathLike = field(
        metadata={
            "help_string": "map label coordinates to the template volume",
            "argstr": "--reg",
            "xor": {"no_registration"},
        }
    )

    threshold: float = field(
        metadata={
            "help_string": "threshold value at which a voxel may be considered for membership to a label",
            "argstr": "--fillthresh",
        }
    )

    projection: Tuple[str, float, float, float] = field(
        metadata={
            "help_string": "projection along the surface normal as (type, start, stop, delta).",
            "argstr": "--proj",
            "requires": {"subject_id", "hemisphere"},
        }
    )

    subject_id: str = field(
        metadata={"help_string": "subject identifier to load the surface from", "argstr": "--subject"}
    )

    no_registration: bool = field(
        metadata={
            "help_string": "use the identity matrix for registration",
            "argstr": "--identity",
            "xor": {"registration_file"},
        }
    )

    output_volume: str = field(metadata={"help_string": "output volume", "argstr": "--o"})


class Label2Vol(ShellCommandTask):
    """Task definition for mri_label2vol."""

    executable = "mri_label2vol"

    input_spec = SpecInfo(name="Input", bases=(Label2VolSpec, specs.HemisphereSpec, specs.SubjectsDirSpec))

    output_spec = SpecInfo(name="Output", bases=(specs.SubjectsDirOutSpec,))
