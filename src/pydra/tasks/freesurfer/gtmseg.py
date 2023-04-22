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
...     output_volume_file="gtmseg.wmseg.hypo.mgz",
...     upsampling_factor=1,
...     use_existing_segmentation=True,
... )
>>> task.cmdline
'gtmseg --s subject --o gtmseg.wmseg.hypo.mgz --no-xcerseg --usf 1 --keep-hypo --subsegwm'
>>> task = GTMSeg(
...     subject_id="subject",
...     output_volume_file="gtmseg+myseg.mgz",
...     segmentation_file="apas+head+myseg.mgz",
...     colortable="myseg.colortable.txt",
... )
>>> task.cmdline
'gtmseg --s subject --o gtmseg+myseg.mgz --head apas+head+myseg.mgz --ctab myseg.colortable.txt'
"""
import attrs

import pydra

from . import specs

__all__ = ["GTMSeg"]


@attrs.define(slots=False, kw_only=True)
class GTMSegSpec(pydra.specs.ShellSpec):
    """Specifications for FreeSurfer's gtmseg."""

    subject_id: str = attrs.field(
        metadata={
            "help_string": "subject to analyze",
            "mandatory": True,
            "argstr": "--s",
        }
    )

    output_volume_file: str = attrs.field(
        default="gtmseg.mgz",
        metadata={
            "help_string": "output volume file relative to the subject's mri directory",
            "argstr": "--o",
        },
    )

    generate_segmentation: bool = attrs.field(
        metadata={
            "help_string": "generate segmentation using xcerebralseg",
            "mandatory": True,
            "argstr": "--xcerseg",
            "xor": {"use_existing_segmentation", "segmentation_file"},
        }
    )

    use_existing_segmentation: bool = attrs.field(
        metadata={
            "help_string": "use existing segmentation",
            "mandatory": True,
            "argstr": "--no-xcerseg",
            "xor": {"generate_segmentation", "segmentation_file"},
        }
    )

    segmentation_file: str = attrs.field(
        metadata={
            "help_string": "use custom segmentation",
            "mandatory": True,
            "argstr": "--head",
            "xor": {"generate_segmentation", "use_existing_segmentation"},
        }
    )

    no_pons_segmentation: bool = attrs.field(
        metadata={
            "help_string": "exclude pons from segmentation",
            "argstr": "--no-pons",
            "requires": {"generate_segmentation"},
        }
    )

    no_vermis_segmentation: bool = attrs.field(
        metadata={
            "help_string": "exclude vermis from segmentation",
            "argstr": "--no-vermis",
            "requires": {"generate_segmentation"},
        }
    )

    colortable: str = attrs.field(
        metadata={
            "help_string": "use custom colortable",
            "argstr": "--ctab",
        }
    )

    upsampling_factor: int = attrs.field(
        metadata={
            "help_string": "upsampling factor (defaults to 2)",
            "argstr": "--usf",
        }
    )

    output_upsampling_factor: int = attrs.field(
        metadata={
            "help_string": "output upsampling factor (if different from upsampling factor)",
            "argstr": "--output-usf",
        }
    )

    keep_hypointensities: bool = attrs.field(
        metadata={
            "help_string": "do not relabel hypointensities as white matter",
            "argstr": "--keep-hypo",
        }
    )

    keep_corpus_callosum: bool = attrs.field(
        metadata={
            "help_string": "do not relabel corpus callosum as white matter",
            "argstr": "--keep-cc",
        }
    )

    subsegment_white_matter: bool = attrs.field(
        metadata={
            "help_string": "subsegment white matter into lobes",
            "argstr": "--subsegwm",
        }
    )


class GTMSeg(pydra.ShellCommandTask):
    """Task generator for FreeSurfer's gtmseg."""

    input_spec = pydra.specs.SpecInfo(
        name="GTMSegInput",
        bases=(GTMSegSpec, specs.SubjectsDirSpec),
    )

    output_spec = pydra.specs.SpecInfo(
        name="GTMSegOutput",
        bases=(specs.SubjectsDirOutSpec,),
    )

    executable = "gtmseg"
