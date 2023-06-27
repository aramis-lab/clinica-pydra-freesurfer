"""
BaseReconAll
============

Base longitudinal template processing using FreeSurfer's recon-all.
"""

__all__ = ["BaseReconAll"]

from typing import Sequence

from attrs import define, field
from pydra.engine.specs import ShellOutSpec, ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask

from . import specs


@define(slots=False, kw_only=True)
class BaseReconAllSpec(ShellSpec):
    """Specifications for the base template workflow of recon-all."""

    base_template_id: str = field(
        metadata={"help_string": "base template identifier", "mandatory": True, "argstr": "-base"}
    )

    base_timepoint_ids: Sequence[str] = field(
        metadata={"help_string": "base timepoint identifiers", "argstr": "-base-tp..."}
    )


@define(slots=False, kw_only=True)
class BaseReconAllOutSpec(ShellOutSpec):
    """Specifications for the base template workflow of recon-all."""

    subject_id: str = field(
        metadata={
            "help_string": "subject identifier where outputs are written",
            "callable": lambda base_template_id: base_template_id,
        }
    )


class BaseReconAll(ShellCommandTask):
    """Task definition for the base template workflow of recon-all."""

    executable = "recon-all"

    input_spec = SpecInfo(name="Input", bases=(BaseReconAllSpec, specs.ReconAllBaseSpec))

    output_spec = SpecInfo(name="Output", bases=(BaseReconAllOutSpec, specs.ReconAllBaseOutSpec))
