"""
LongReconAll
============

Longitudinal timepoint processing using FreeSurfer's recon-all.
"""

__all__ = ["LongReconAll"]

from attrs import define, field
from pydra.engine.specs import ShellOutSpec, ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask

from . import specs


@define(slots=False, kw_only=True)
class LongReconAllSpec(ShellSpec):
    """Specifications for the longitudinal workflow of recon-all."""

    longitudinal_timepoint_id: str = field(
        metadata={
            "help_string": "longitudinal timepoint identifier",
            "mandatory": True,
            "argstr": "-long {longitudinal_timepoint_id} {longitudinal_template_id}",
            "requires": ["longitudinal_template_id"],
        }
    )

    longitudinal_template_id: str = field(metadata={"help_string": "longitudinal template identifier", "argstr": None})


@define(slots=False, kw_only=True)
class LongReconAllOutSpec(ShellOutSpec):
    """Output specifications for the longitudinal workflow of recon-all."""

    subject_id: str = field(
        metadata={
            "help_string": "subject identifier where outputs are written",
            "callable": lambda longitudinal_timepoint_id, longitudinal_template_id: (
                f"{longitudinal_timepoint_id}.long.{longitudinal_template_id}"
            ),
        }
    )


class LongReconAll(ShellCommandTask):
    """Task definition for the longitudinal workflow of recon-all."""

    executable = "recon-all"

    input_spec = SpecInfo(name="Input", bases=(LongReconAllSpec, specs.ReconAllBaseSpec))

    output_spec = SpecInfo(name="Output", bases=(LongReconAllOutSpec, specs.ReconAllBaseOutSpec))
