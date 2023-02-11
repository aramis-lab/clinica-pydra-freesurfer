"""
MRIAparc2Aseg
=============

Maps the cortical labels from the automatic cortical parcellation (aparc)
to the automatic segmentation volume (aseg).

Examples
--------

>>> task = MRIAparc2Aseg(
...     subject_id="subjid",
...     annotation_file="atlas.annot",
...     mask_cortical_voxels=True,
...     output_volume_file="atlas.mgz",
... )
>>> task.cmdline
'mri_aparc2aseg --s subjid --o atlas.mgz --volmask --annot atlas.annot'
"""
import os

import attrs

import pydra

from . import specs

__all__ = ["MRIAparc2Aseg"]


@attrs.define(slots=False, kw_only=True)
class MRIAparc2AsegSpec(pydra.specs.ShellSpec):
    """Specifications for mri_aparc2aseg."""

    subject_id: str = attrs.field(
        metadata={"help_string": "subject identifier", "argstr": "--s"}
    )

    output_volume_file: str = attrs.field(
        metadata={"help_string": "output segmented volume", "argstr": "--o"}
    )

    mask_cortical_voxels: bool = attrs.field(
        metadata={"help_string": "mask cortical voxels with mri/ribbon.mgz", "argstr": "--volmask"}
    )

    use_a2005s_annotation: bool = attrs.field(
        metadata={
            "help_string": "use label/?h.aparc.a2005s.annot as annotation file",
            "argstr": "--a2005s",
            "xor": {"use_a2009s_annotation", "annotation_file"},
        }
    )

    use_a2009s_annotation: bool = attrs.field(
        metadata={
            "help_string": "use label/?h.aparc.a2009s.annot as annotation file",
            "argstr": "--a2009s",
            "xor": {"use_a2005s_annotation", "annotation_file"},
        }
    )

    annotation_file: os.PathLike = attrs.field(
        metadata={
            "help_string": "use annotation file",
            "argstr": "--annot",
            "xor": {"use_a2005s_annotation", "use_a2009s_annotation"},
        }
    )

    hemisphere: str = attrs.field(
        metadata={
            "help_string": "only process hemisphere",
            "argstr": "--{hemisphere}",
            "allowed_values": {"lh", "rh"},
        }
    )

    threads: int = attrs.field(
        metadata={"help_string": "run in parallel", "argstr": "--threads"}
    )


class MRIAparc2Aseg(pydra.engine.ShellCommandTask):
    """Task definition for mri_aparc2aseg."""

    input_spec = pydra.specs.SpecInfo(
        name="MRIAparc2AsegInput",
        bases=(MRIAparc2AsegSpec, specs.SubjectsDirSpec),
    )

    output_spec = pydra.specs.SpecInfo(
        name="MRIAparc2AsegOutput",
        bases=(specs.SubjectsDirOutSpec,),
    )

    executable = "mri_aparc2aseg"
