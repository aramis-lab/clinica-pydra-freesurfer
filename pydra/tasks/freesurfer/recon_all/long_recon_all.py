"""Longitudinal timepoint processing using FreeSurfer's recon-all."""

import attrs

import pydra

from . import specs

__all__ = ["LongReconAll"]


@attrs.define(slots=False, kw_only=True)
class LongReconAllSpec(pydra.specs.ShellSpec):
    longitudinal_timepoint_id: str = attrs.field(
        metadata={
            "help_string": "longitudinal timepoint identifier",
            "mandatory": True,
            "argstr": "-long {longitudinal_timepoint_id} {longitudinal_template_id}",
            "requires": ["longitudinal_template_id"],
        }
    )

    longitudinal_template_id: str = attrs.field(
        metadata={
            "help_string": "longitudinal template identifier",
            "argstr": None,
        }
    )


@attrs.define(slots=False, kw_only=True)
class LongReconAllOutSpec(pydra.specs.ShellOutSpec):
    @staticmethod
    def get_subject_id(
        longitudinal_timepoint_id: str, longitudinal_template_id: str
    ) -> str:
        return f"{longitudinal_timepoint_id}.long.{longitudinal_template_id}"

    subject_id: str = attrs.field(
        metadata={
            "help_string": "subject identifier where outputs are written",
            "callable": get_subject_id,
        }
    )


class LongReconAll(pydra.ShellCommandTask):
    input_spec = pydra.specs.SpecInfo(
        name="LongReconAllInput",
        bases=(LongReconAllSpec, specs.ReconAllBaseSpec),
    )

    output_spec = pydra.specs.SpecInfo(
        name="LongReconAllOutput",
        bases=(LongReconAllOutSpec, specs.ReconAllBaseOutSpec),
    )

    executable = "recon-all"
