"""
Aparc2Aseg
==========

Maps the cortical labels from the automatic cortical parcellation (aparc)
to the automatic segmentation volume (aseg).

Examples
--------

>>> task = Aparc2Aseg(subject_id="subjid", annotation_file="atlas.annot", output_image="atlas.mgz")
>>> task.cmdline
'mri_aparc2aseg --s subjid --o atlas.mgz --new-ribbon --annot atlas.annot'
"""

__all__ = ["Aparc2Aseg"]

from os import PathLike

from attrs import define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask

from .. import specs


@define(slots=False, kw_only=True)
class Aparc2AsegSpec(ShellSpec):
    """Specifications for mri_aparc2aseg."""

    subject_id: str = field(metadata={"help_string": "subject identifier", "mandatory": True, "argstr": "--s"})

    output_image: str = field(
        default="mri/aparc+aseg.mgz", metadata={"help_string": "output segmented volume", "argstr": "--o"}
    )

    cortex_mask: str = field(
        default="new",
        metadata={
            "help_string": "mask cortical voxels with mri/ribbon.mgz (new) or mri/?h.ribbon.mgz (old)",
            "argstr": "--{cortex_mask}-ribbon",
            "allowed_values": {"new", "old"},
        },
    )

    use_a2005s_annotation: bool = field(
        metadata={
            "help_string": "use label/?h.aparc.a2005s.annot as annotation file",
            "argstr": "--a2005s",
            "xor": {"use_a2009s_annotation", "annotation_file"},
        }
    )

    use_a2009s_annotation: bool = field(
        metadata={
            "help_string": "use label/?h.aparc.a2009s.annot as annotation file",
            "argstr": "--a2009s",
            "xor": {"use_a2005s_annotation", "annotation_file"},
        }
    )

    annotation_file: PathLike = field(
        metadata={
            "help_string": "use annotation file",
            "argstr": "--annot",
            "xor": {"use_a2005s_annotation", "use_a2009s_annotation"},
        }
    )

    num_threads: int = field(
        metadata={"help_string": "run in parallel with this number of threads", "argstr": "--nthreads"}
    )


class Aparc2Aseg(ShellCommandTask):
    """Task definition for mri_aparc2aseg."""

    input_spec = SpecInfo(name="Input", bases=(Aparc2AsegSpec, specs.HemisphereSpec, specs.SubjectsDirSpec))

    output_spec = SpecInfo(name="Output", bases=(specs.SubjectsDirOutSpec,))

    executable = "mri_aparc2aseg"
