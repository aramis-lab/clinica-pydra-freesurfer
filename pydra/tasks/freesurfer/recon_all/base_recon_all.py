"""Base longitudinal template processing using FreeSurfer's recon-all."""

import typing as ty

import attrs

import pydra

from . import specs

__all__ = ["BaseReconAll"]


@attrs.define(slots=False, kw_only=True)
class BaseReconAllSpec(pydra.specs.ShellSpec):
    base_template_id: str = attrs.field(
        metadata={
            "help_string": "base template identifier",
            "mandatory": True,
            "argstr": "-base",
        }
    )

    base_timepoint_ids: ty.Iterable[str] = attrs.field(
        metadata={
            "help_string": "base timepoint identifiers",
            "argstr": "-base-tp...",
        }
    )


@attrs.define(slots=False, kw_only=True)
class BaseReconAllOutSpec(pydra.specs.ShellOutSpec):
    @staticmethod
    def get_subject_id(base_template_id: str) -> str:
        return base_template_id

    subject_id: str = attrs.field(
        metadata={
            "help_string": "subject identifier where outputs are written",
            "callable": get_subject_id,
        }
    )


class BaseReconAll(pydra.ShellCommandTask):
    input_spec = pydra.specs.SpecInfo(
        name="BaseReconAllInput",
        bases=(BaseReconAllSpec, specs.ReconAllBaseSpec),
    )

    output_spec = pydra.specs.SpecInfo(
        name="BaseReconAllOutput",
        bases=(BaseReconAllOutSpec, specs.ReconAllBaseOutSpec),
    )

    executable = "recon-all"
