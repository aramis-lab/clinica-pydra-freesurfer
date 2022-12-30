import attrs

import pydra

from . import specs

__all__ = ["GTMSeg"]


@attrs.define(slots=False, kw_only=True)
class GTMSegSpec(pydra.specs.ShellSpec):
    subject_id: str = attrs.field(
        metadata={
            "help_string": "subject to analyze",
            "mandatory": True,
            "argstr": "--s {subject_id}",
        }
    )

    output_volume: str = attrs.field(
        default="gtmseg.mgz",
        metadata={
            "help_string": "output volume relative to subject's mri directory",
            "argstr": "--o {output_volume}",
        },
    )

    xcerseg: bool = attrs.field(
        metadata={
            "help_string": "(re)generate or use apas+head.mgz",
            "mandatory": True,
            # See https://github.com/nipype/pydra/issues/611
            "formatter": (
                lambda field: ""
                if field is None
                else "--xcerseg"
                if field
                else "--no-xcerseg"
            ),
            "xor": {"headseg"},
        }
    )

    headseg: str = attrs.field(
        metadata={
            "help_string": "use custom headseg instead of apas+head.mgz",
            "mandatory": True,
            "argstr": "--head {headseg}",
            "xor": {"xcerseg"},
        }
    )

    no_pons: bool = attrs.field(
        metadata={
            "help_string": "no pons segmentation with xcerebralseg",
            "argstr": "--no-pons",
            "requires": ["xcerseg"],
        }
    )

    no_vermis: bool = attrs.field(
        metadata={
            "help_string": "no vermis segmentation with xcerebralseg",
            "argstr": "--no-vermis",
            "requires": ["xcerseg"],
        }
    )

    colortable: str = attrs.field(
        metadata={
            "help_string": "use custom colortable",
            "argstr": "--ctab {colortable}",
        }
    )

    upsampling_factor: int = attrs.field(
        metadata={
            "help_string": "upsampling factor (defaults to 2)",
            "argstr": "--usf {upsampling_factor}",
        }
    )

    output_upsampling_factor: int = attrs.field(
        metadata={
            "help_string": "output upsampling factor (if different from upsampling factor)",
            "argstr": "--output-usf {output_upsampling_factor}",
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
    """Task for PETSurfer's gtmseg.

    Examples
    --------
    >>> task = GTMSeg(subject_id="subject", xcerseg=True)
    >>> task.cmdline
    'gtmseg --s subject --o gtmseg.mgz --xcerseg'
    >>> task = GTMSeg(
    ...     subject_id="subject",
    ...     keep_hypointensities=True,
    ...     subsegment_white_matter=True,
    ...     output_volume="gtmseg.wmseg.hypo.mgz",
    ...     upsampling_factor=1,
    ...     xcerseg=False,
    ... )
    >>> task.cmdline
    'gtmseg --s subject --o gtmseg.wmseg.hypo.mgz --no-xcerseg --usf 1 --keep-hypo --subsegwm'
    >>> task = GTMSeg(
    ...     subject_id="subject",
    ...     output_volume="gtmseg+myseg.mgz",
    ...     headseg="apas+head+myseg.mgz",
    ...     colortable="myseg.colortable.txt",
    ... )
    >>> task.cmdline
    'gtmseg --s subject --o gtmseg+myseg.mgz --head apas+head+myseg.mgz --ctab myseg.colortable.txt'
    """

    input_spec = pydra.specs.SpecInfo(
        name="GTMSegInput",
        bases=(GTMSegSpec, specs.SubjectsDirSpec),
    )

    output_spec = pydra.specs.SpecInfo(
        name="GTMSegOutput",
        bases=(specs.SubjectsDirOutSpec,),
    )

    executable = "gtmseg"
