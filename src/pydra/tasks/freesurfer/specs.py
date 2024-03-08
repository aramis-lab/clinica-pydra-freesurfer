from __future__ import annotations

import os

import attrs

import pydra

__all__ = ["SubjectsDirSpec", "SubjectsDirOutSpec", "HemisphereSpec"]


@attrs.define(slots=False, kw_only=True)
class SubjectsDirSpec(pydra.specs.ShellSpec):
    subjects_dir: os.PathLike = attrs.field(
        metadata={
            "help_string": "subjects directory processed by FreeSurfer",
            "argstr": "--sd {subjects_dir}",
        }
    )


@attrs.define(slots=False, kw_only=True)
class SubjectsDirOutSpec(pydra.specs.ShellOutSpec):
    @staticmethod
    def get_subjects_dir(subjects_dir: str | None) -> str:
        return os.fspath(subjects_dir or os.getenv("SUBJECTS_DIR"))

    subjects_dir: str = attrs.field(
        metadata={
            "help_string": "subjects directory processed by FreeSurfer",
            "callable": get_subjects_dir,
        }
    )


@attrs.define(slots=False, kw_only=True)
class HemisphereSpec(pydra.specs.ShellSpec):
    """Specifications for hemisphere parameter."""

    hemisphere: str = attrs.field(
        metadata={
            "help_string": "process left or right hemisphere",
            "argstr": "--hemi",
            "allowed_values": ["lh", "rh"],
        }
    )
