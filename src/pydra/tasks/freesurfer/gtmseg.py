"""
GTMSeg
======

Examples
--------
>>> task = GTMSeg(subject_id="subject", generate_segmentation=True)
>>> task.cmdline
'gtmseg --s subject --o gtmseg.mgz --xcerseg'

>>> task = GTMSeg(
...     subject_id="subject",
...     keep_hypointensities=True,
...     subsegment_white_matter=True,
...     output_volume="gtmseg.wmseg.hypo.mgz",
...     upsampling_factor=1,
...     generate_segmentation=False,
... )
>>> task.cmdline
'gtmseg --s subject --o gtmseg.wmseg.hypo.mgz --no-xcerseg --usf 1 --keep-hypo --subsegwm'

>>> task = GTMSeg(
...     subject_id="subject",
...     output_volume="gtmseg+myseg.mgz",
...     head_segmentation="apas+head+myseg.mgz",
...     colortable="myseg.colortable.txt",
... )
>>> task.cmdline
'gtmseg --s subject --o gtmseg+myseg.mgz --head apas+head+myseg.mgz --ctab myseg.colortable.txt'
"""

__all__ = ["GTMSeg"]

from os import PathLike

from attrs import NOTHING, define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask

from . import specs


@define(kw_only=True)
class GTMSegSpec(ShellSpec):
    """Specifications for gtmseg."""

    subject_id: str = field(metadata={"help_string": "subject identifier", "mandatory": True, "argstr": "--s"})

    output_volume: str = field(
        default="gtmseg.mgz",
        metadata={"help_string": "output volume relative to the subject's mri directory", "argstr": "--o"},
    )

    generate_segmentation: bool = field(
        metadata={
            "help_string": "generate or use subject's head segmentation",
            "mandatory": True,
            "formatter": lambda generate_segmentation: (
                "" if generate_segmentation is NOTHING else "--xcerseg" if generate_segmentation else "--no-xcerseg"
            ),
            "xor": {"head_segmentation"},
        }
    )

    head_segmentation: PathLike = field(
        metadata={
            "help_string": "custom head segmentation",
            "mandatory": True,
            "argstr": "--head",
            "xor": {"generate_segmentation"},
        }
    )

    no_pons_segmentation: bool = field(
        metadata={
            "help_string": "exclude pons from segmentation",
            "argstr": "--no-pons",
            "requires": {"generate_segmentation"},
        }
    )

    no_vermis_segmentation: bool = field(
        metadata={
            "help_string": "exclude vermis from segmentation",
            "argstr": "--no-vermis",
            "requires": {"generate_segmentation"},
        }
    )

    colortable: str = field(metadata={"help_string": "use custom colortable", "argstr": "--ctab"})

    upsampling_factor: int = field(metadata={"help_string": "upsampling factor (defaults to 2)", "argstr": "--usf"})

    output_upsampling_factor: int = field(
        metadata={
            "help_string": "output upsampling factor (if different from upsampling factor)",
            "argstr": "--output-usf",
        }
    )

    keep_hypointensities: bool = field(
        metadata={"help_string": "do not relabel hypointensities as white matter", "argstr": "--keep-hypo"}
    )

    keep_corpus_callosum: bool = field(
        metadata={"help_string": "do not relabel corpus callosum as white matter", "argstr": "--keep-cc"}
    )

    subsegment_white_matter: bool = field(
        metadata={"help_string": "subsegment white matter into lobes", "argstr": "--subsegwm"}
    )


class GTMSeg(ShellCommandTask):
    """Task definition for gtmseg."""

    executable = "gtmseg"

    input_spec = SpecInfo(name="Output", bases=(GTMSegSpec, specs.SubjectsDirSpec))

    output_spec = SpecInfo(name="Input", bases=(specs.SubjectsDirOutSpec,))
