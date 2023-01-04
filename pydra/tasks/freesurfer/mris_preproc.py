"""
MRISPreproc
===========

Script to prepare surface-based data for high-level analysis
by resampling surface or volume source data to a common subject (usually an average subject)
and then concatenating them into one file which can then be used by a number of programs (eg, mri_glmfit).

Examples
--------

>>> source_subject_ids = [f"abc{s:02d}-anat" for s in range(1, 5)]

1. Resample abcXX-anat/surf/lh.thickness onto fsaverage:

>>> task = MRISPreproc(
...     source_subject_ids=source_subject_ids,
...     target_subject_id="fsaverage",
...     hemisphere="lh",
...     measure="thickness",
...     output_surface_file="abc-lh-thickness.mgh",
... )
>>> task.cmdline
'mris_preproc --out abc-lh-thickness.mgh --target fsaverage --hemi lh --meas thickness \
--s abc01-anat --s abc02-anat --s abc03-anat --s abc04-anat'

2. Same as above but using a fsgd file (which would have the abcXXs as Inputs):

>>> task = MRISPreproc(
...     fsgd_file="abc.fsgd",
...     target_subject_id="fsaverage",
...     hemisphere="lh",
...     measure="thickness",
...     output_surface_file="abc-lh-thickness.mgh",
... )
>>> task.cmdline
'mris_preproc --out abc-lh-thickness.mgh --target fsaverage --hemi lh --meas thickness --fsgd abc.fsgd'

3. Same as #1 with additional smoothing by 5mm:

>>> task = MRISPreproc(
...     source_subject_ids=source_subject_ids,
...     target_subject_id="fsaverage",
...     hemisphere="lh",
...     measure="thickness",
...     output_surface_file="abc-lh-thickness.sm5.mgh",
...     target_smoothing=5,
... )
>>> task.cmdline
'mris_preproc --out abc-lh-thickness.sm5.mgh --target fsaverage --hemi lh --meas thickness \
--s abc01-anat --s abc02-anat --s abc03-anat --s abc04-anat --fwhm 5'

4. Same as #1 but using full paths.

>>> task = MRISPreproc(
...     target_subject_id="fsaverage",
...     hemisphere="lh",
...     output_surface_file="abc-lh-thickness.mgh",
...     fsgd_file="abc.fsgd",
...     source_format="curv",
...     input_surface_measures=[f"abc{s:02d}-anat/surf/lh.thickness" for s in range(1, 5)],
... )
>>> task.cmdline
'mris_preproc --out abc-lh-thickness.mgh --target fsaverage --hemi lh --fsgd abc.fsgd \
--isp abc01-anat/surf/lh.thickness --isp abc02-anat/surf/lh.thickness --isp abc03-anat/surf/lh.thickness \
--isp abc04-anat/surf/lh.thickness --srcfmt curv'

5. Same as #2 but computes paired differences.

>>> task = MRISPreproc(
...     fsgd_file="abc.fsgd",
...     target_subject_id="fsaverage",
...     hemisphere="lh",
...     measure="thickness",
...     output_surface_file="abc-lh-thickness-pdiff.mgh",
...     compute_paired_differences=True,
... )
>>> task.cmdline
'mris_preproc --out abc-lh-thickness-pdiff.mgh --target fsaverage --hemi lh --meas thickness --fsgd abc.fsgd \
--paired-diff'
"""

import typing as ty

import attrs

import pydra

from . import specs

__all__ = ["MRISPreproc"]


@attrs.define(slots=False, kw_only=True)
class MRISPreprocSpec(pydra.specs.ShellSpec):

    output_surface_file: str = attrs.field(
        metadata={
            "help_string": "output file",
            "argstr": "--out",
            "requires": {"target_subject_id", "hemisphere"},
            "output_file_template": "{target_subject_id}_{hemisphere}.mgz",
        }
    )

    target_subject_id: str = attrs.field(
        metadata={
            "help_string": "subject identifier to use as common space",
            "mandatory": True,
            "argstr": "--target",
        }
    )

    hemisphere: str = attrs.field(
        metadata={
            "help_string": "left or right hemisphere",
            "mandatory": True,
            "argstr": "--hemi",
            "allowed_values": {"lh", "rh"},
        }
    )

    measure: str = attrs.field(
        metadata={
            "help_string": "use source subject's measure as input",
            "argstr": "--meas",
        }
    )

    source_subject_ids: ty.Iterable[str] = attrs.field(
        metadata={
            "help_string": "source subjects used as input",
            "argstr": "--s ...",
            "requires": {"measure"},
            "xor": {"fsdg_file"},
        }
    )

    fsgd_file: str = attrs.field(
        metadata={
            "help_string": "fsgd file containing the source subjects",
            "argstr": "--fsgd",
            "xor": {"source_subject_ids"},
        }
    )

    input_surface_measures: ty.Iterable[str] = attrs.field(
        metadata={
            "help_string": "paths to input surface measure files",
            "argstr": "--isp ...",
            "requires": {"fsgd_file"},
        }
    )

    source_format: str = attrs.field(
        metadata={
            "help_string": "source format of input surface measure files",
            "argstr": "--srcfmt",
            "requires": {"input_surface_measures"},
        }
    )

    target_smoothing: float = attrs.field(
        metadata={
            "help_string": "smooth target surface by X mm",
            "argstr": "--fwhm",
        }
    )

    source_smoothing: float = attrs.field(
        metadata={
            "help_string": "smooth source surface by X mm",
            "argstr": "--fwhm-src",
        }
    )

    compute_paired_differences: bool = attrs.field(
        metadata={
            "help_string": "compute paired differences",
            "argstr": "--paired-diff",
        }
    )


class MRISPreproc(pydra.ShellCommandTask):
    """Task for mris_preproc."""

    input_spec = pydra.specs.SpecInfo(
        name="MRISPreprocInput",
        bases=(MRISPreprocSpec, specs.SubjectsDirSpec),
    )

    executable = "mris_preproc"
