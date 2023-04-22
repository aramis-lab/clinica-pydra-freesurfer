"""
MRIVol2Vol
==========

Resamples a volume into another field-of-view using various types
of matrices (FreeSurfer, FSL, SPM, and MNI).

This is meant to be used in conjunction with tkregister2.

Examples
--------

1. Resample functional data into anatomical space:

>>> task = MRIVol2Vol(
...     moving_volume_file="func.nii.gz",
...     output_volume_file="func-in-anat.mgh",
...     registration_file="register.dat",
...     use_registered_volume_as_target=True,
... )
>>> task.cmdline
'mri_vol2vol --mov func.nii.gz --o func-in-anat.mgh --reg register.dat --fstarg'

2. Resample anatomical data into functional space:

>>> task = MRIVol2Vol(
...     moving_volume_file="func.nii.gz",
...     output_volume_file="anat-in-func.mgh",
...     registration_file="register.dat",
...     use_registered_volume_as_target=True,
...     invert_transform=True,
... )
>>> task.cmdline
'mri_vol2vol --mov func.nii.gz --o anat-in-func.mgh --reg register.dat --fstarg --inv'

3. Map functional to anatomical without resampling:

>>> task = MRIVol2Vol(
...     moving_volume_file="func.nii.gz",
...     output_volume_file="func.new.vox2ras.nii.gz",
...     registration_file="register.dat",
...     use_registered_volume_as_target=True,
...     no_resampling=True,
... )
>>> task.cmdline
'mri_vol2vol --mov func.nii.gz --o func.new.vox2ras.nii.gz --reg register.dat --fstarg --no-resample'

4. Map a binary mask in functional space to anatomical space:

>>> task = MRIVol2Vol(
...     moving_volume_file="mask.nii.gz",
...     output_volume_file="mask-in-anat.mgh",
...     registration_file="register.dat",
...     use_registered_volume_as_target=True,
...     interpolation="nearest",
... )
>>> task.cmdline
'mri_vol2vol --mov mask.nii.gz --o mask-in-anat.mgh --reg register.dat --fstarg --interp nearest'

5. Map functional data to talairach (MNI305) space with 2mm isotropic resolution:

>>> task = MRIVol2Vol(
...     moving_volume_file="func.nii.gz",
...     output_volume_file="func-in-tal.2mm.mgh",
...     registration_file="register.dat",
...     resample_to_talairach=True,
...     talairach_resolution=2,
... )
>>> task.cmdline
'mri_vol2vol --mov func.nii.gz --o func-in-tal.2mm.mgh --reg register.dat --tal --talres 2'

6. Apply an MNI transform by resampling the anatomical data into talairach space:

>>> task = MRIVol2Vol(
...     moving_volume_file="orig.mgz",
...     target_volume_file="$FREESURFER_HOME/average/mni305.cor.mgz",
...     output_volume_file="orig-in-mni305.mgz",
...     xfm_registration_file="transforms/talairach.xfm",
... )
>>> task.cmdline
'mri_vol2vol --mov orig.mgz --targ $FREESURFER_HOME/average/mni305.cor.mgz --o orig-in-mni305.mgz \
--xfm transforms/talairach.xfm'
"""

import attrs

import pydra

from . import specs

__all__ = ["MRIVol2Vol"]


@attrs.define(slots=False, kw_only=True)
class MRIVol2VolSpec(pydra.specs.ShellSpec):
    """Specifications for mri_vol2vol."""

    moving_volume_file: str = attrs.field(
        metadata={
            "help_string": "moving volume (target volume if transform is inverted)",
            "argstr": "--mov",
        }
    )

    target_volume_file: str = attrs.field(
        metadata={
            "help_string": "target volume (moving volume if transform is inverted)",
            "argstr": "--targ",
        }
    )

    output_volume_file: str = attrs.field(
        metadata={
            "help_string": "output volume",
            "argstr": "--o",
        }
    )

    registration_file: str = attrs.field(
        metadata={
            "help_string": "registration file in FreeSurfer format",
            "argstr": "--reg",
        }
    )

    use_registered_volume_as_target: bool = attrs.field(
        metadata={
            "help_string": "use volume in registration file as target",
            "argstr": "--fstarg",
            "requires": {"registration_file"},
        }
    )

    fsl_registration_file: str = attrs.field(
        metadata={
            "help_string": "registration file in FSL format",
            "argstr": "--fsl",
        }
    )

    xfm_registration_file: str = attrs.field(
        metadata={
            "help_string": "registration file in XFM format",
            "argstr": "--xfm",
        }
    )

    resample_to_talairach: bool = attrs.field(
        metadata={
            "help_string": "resample moving volume to Talairach",
            "argstr": "--tal",
        }
    )

    talairach_resolution: int = attrs.field(
        metadata={
            "help_string": "resolution of the Talairach template",
            "argstr": "--talres",
            "allowed_values": {1, 2},
            "requires": ["resample_to_talairach"],
        }
    )

    invert_transform: bool = attrs.field(
        metadata={
            "help_string": "invert transform",
            "argstr": "--inv",
        }
    )

    no_resampling: bool = attrs.field(
        metadata={
            "help_string": "change the vox2ras matrix instead of resampling",
            "argstr": "--no-resample",
        }
    )

    interpolation: str = attrs.field(
        metadata={
            "help_string": "interpolate output with the chosen method",
            "argstr": "--interp",
            "allowed_values": {"cubic", "nearest", "trilin"},
        }
    )


class MRIVol2Vol(pydra.ShellCommandTask):
    """Task for mri_vol2vol."""

    input_spec = pydra.specs.SpecInfo(
        name="MRIVol2VolInput",
        bases=(MRIVol2VolSpec, specs.SubjectsDirSpec),
    )

    executable = "mri_vol2vol"
