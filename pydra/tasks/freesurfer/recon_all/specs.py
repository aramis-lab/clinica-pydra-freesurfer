import os
import typing as ty

import attrs

import pydra

from ..specs import SubjectsDirOutSpec as ReconAllBaseOutSpec

__all__ = ["ReconAllBaseSpec", "ReconAllBaseOutSpec"]


@attrs.define(slots=False, kw_only=True)
class ReconAllBaseSpec(pydra.specs.ShellSpec):
    directive: str = attrs.field(
        default="all",
        metadata={
            "help_string": "process directive",
            "argstr": "-{directive}",
            "allowed_values": {
                # All steps.
                "all",
                # Steps 1 to 5.
                "autorecon1",
                # Steps 6 to 23.
                "autorecon2",
                # Steps 12 to 23.
                "autorecon2-cp",
                # Steps 15 to 23.
                "autorecon2-wm",
                # Steps 21 to 23.
                "autorecon2-pial",
                # Steps 24 to 31.
                "autorecon3",
            },
        },
    )

    custom_mask_input: os.PathLike = attrs.field(
        metadata={
            "help_string": "input custom brain mask",
            "argstr": "-xmask {custom_mask_input}",
        },
    )

    hemisphere: str = attrs.field(
        metadata={
            "help_string": "restrict processing to this hemisphere",
            "argstr": "-hemi {hemisphere}",
            "allowed_values": ["lh", "rh"],
        },
    )

    parallel: bool = attrs.field(
        metadata={
            "help_string": "process both hemispheres in parallel",
            "argstr": "-parallel",
            "xor": ["hemisphere"],
        },
    )

    threads: int = attrs.field(
        metadata={
            "help_string": "set number of threads to use",
            "argstr": "-threads {threads}",
        },
    )

    subjects_dir: os.PathLike = attrs.field(
        metadata={
            "help_string": "subjects directory processed by FreeSurfer",
            "argstr": "-sd {subjects_dir}",
        },
    )
