"""Cross-sectional processing using FreeSurfer's recon-all."""

import os
import typing as ty

import attrs

import pydra

from . import specs

__all__ = ["ReconAll"]


@attrs.define(slots=False, kw_only=True)
class ReconAllSpec(pydra.specs.ShellSpec):
    subject_id: str = attrs.field(
        metadata={
            "help_string": "subject identifier",
            "mandatory": True,
            "argstr": "-subjid",
        }
    )

    t1_volume_file: os.PathLike = attrs.field(
        metadata={
            "help_string": "input T1 volume",
            "argstr": "-i",
            "xor": ["t1_volume_files"],
        }
    )

    t1_volume_files: ty.Iterable[os.PathLike] = attrs.field(
        metadata={
            "help_string": "input T1 volumes",
            "argstr": "-i...",
            "xor": ["t1_volume_file"],
        }
    )

    t2_volume_file: os.PathLike = attrs.field(
        metadata={
            "help_string": "input T2 volume",
            "argstr": "-t2",
        }
    )

    flair_volume_file: os.PathLike = attrs.field(
        metadata={
            "help_string": "input FLAIR volume",
            "argstr": "-flair",
        }
    )


@attrs.define(slots=False, kw_only=True)
class ReconAllOutSpec(pydra.specs.ShellOutSpec):
    @staticmethod
    def get_subject_id(subject_id: str) -> str:
        return subject_id

    subject_id: str = attrs.field(
        metadata={
            "help_string": "subject identifier where outputs are written",
            "callable": get_subject_id,
        }
    )


class ReconAll(pydra.ShellCommandTask):
    input_spec = pydra.specs.SpecInfo(
        name="ReconAllInput",
        bases=(ReconAllSpec, specs.ReconAllBaseSpec),
    )

    output_spec = pydra.specs.SpecInfo(
        name="ReconAllOutput",
        bases=(ReconAllOutSpec, specs.ReconAllBaseOutSpec),
    )

    executable = "recon-all"
