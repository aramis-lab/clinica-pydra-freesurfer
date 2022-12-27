import os
import typing as ty

import attrs

import pydra

__all__ = ["FreeSurferBaseSpec", "FreeSurferBaseOutSpec"]


@attrs.define(kw_only=True)
class FreeSurferBaseSpec(pydra.specs.ShellSpec):

    subjects_dir: os.PathLike = attrs.field(
        metadata={
            "help_string": "subjects directory processed by FreeSurfer",
            "argstr": "-sd {subjects_dir}",
        }
    )


@attrs.define(kw_only=True)
class FreeSurferBaseOutSpec(pydra.specs.ShellOutSpec):
    @staticmethod
    def get_subjects_dir(subjects_dir: ty.Optional[str]) -> str:
        return os.fspath(subjects_dir or os.getenv("SUBJECTS_DIR"))

    subjects_dir: str = attrs.field(
        metadata={
            "help_string": "subjects directory processed by FreeSurfer",
            "callable": get_subjects_dir,
        }
    )
