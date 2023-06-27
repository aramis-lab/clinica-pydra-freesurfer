"""
ReconAll
========

Cross-sectional processing using FreeSurfer's recon-all.
"""

__all__ = ["ReconAll"]

from os import PathLike
from typing import Sequence

from attrs import define, field
from pydra.engine.specs import ShellOutSpec, ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask

from . import specs


@define(slots=False, kw_only=True)
class ReconAllSpec(ShellSpec):
    """Specifications for recon-all."""

    subject_id: str = field(metadata={"help_string": "subject identifier", "mandatory": True, "argstr": "-subjid"})

    t1_volume: PathLike = field(metadata={"help_string": "T1 volume", "argstr": "-i", "xor": ["t1_volumes"]})

    t1_volumes: Sequence[PathLike] = field(
        metadata={"help_string": "T1 volumes", "argstr": "-i...", "xor": ["t1_volume"]}
    )

    t2_volume: PathLike = field(metadata={"help_string": "T2 volume", "argstr": "-t2"})

    flair_volume: PathLike = field(metadata={"help_string": "FLAIR volume", "argstr": "-flair"})


@define(slots=False, kw_only=True)
class ReconAllOutSpec(ShellOutSpec):
    """Output specifications for recon-all."""

    subject_id: str = field(metadata={"help_string": "subject identifier", "callable": lambda subject_id: subject_id})


class ReconAll(ShellCommandTask):
    """Task definition for recon-all."""

    executable = "recon-all"

    input_spec = SpecInfo(name="Input", bases=(ReconAllSpec, specs.ReconAllBaseSpec))

    output_spec = SpecInfo(name="Output", bases=(ReconAllOutSpec, specs.ReconAllBaseOutSpec))
