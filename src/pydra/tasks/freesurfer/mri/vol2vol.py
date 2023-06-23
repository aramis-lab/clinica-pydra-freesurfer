"""
Vol2Vol
=======

Resamples a volume into another field-of-view using various types
of matrices (FreeSurfer, FSL, SPM, and MNI).

This is meant to be used in conjunction with tkregister2.

Examples
--------

1. Resample functional data into anatomical space:

>>> task = Vol2Vol(
...     moving_volume="func.nii.gz",
...     output_volume="func-in-anat.mgh",
...     registration_file="register.dat",
...     use_registered_volume_as_target=True,
... )
>>> task.cmdline
'mri_vol2vol --mov func.nii.gz --o func-in-anat.mgh --reg register.dat --fstarg'

2. Resample anatomical data into functional space:

>>> task = Vol2Vol(
...     moving_volume="func.nii.gz",
...     output_volume="anat-in-func.mgh",
...     registration_file="register.dat",
...     use_registered_volume_as_target=True,
...     invert_transform=True,
... )
>>> task.cmdline
'mri_vol2vol --mov func.nii.gz --o anat-in-func.mgh --reg register.dat --fstarg --inv'

3. Map functional to anatomical without resampling:

>>> task = Vol2Vol(
...     moving_volume="func.nii.gz",
...     output_volume="func.new.vox2ras.nii.gz",
...     registration_file="register.dat",
...     use_registered_volume_as_target=True,
...     no_resampling=True,
... )
>>> task.cmdline
'mri_vol2vol --mov func.nii.gz --o func.new.vox2ras.nii.gz --reg register.dat --fstarg --no-resample'

4. Map a binary mask in functional space to anatomical space:

>>> task = Vol2Vol(
...     moving_volume="mask.nii.gz",
...     output_volume="mask-in-anat.mgh",
...     registration_file="register.dat",
...     use_registered_volume_as_target=True,
...     interpolation="nearest",
... )
>>> task.cmdline
'mri_vol2vol --mov mask.nii.gz --o mask-in-anat.mgh --reg register.dat --fstarg --interp nearest'

5. Map functional data to talairach (MNI305) space with 2mm isotropic resolution:

>>> task = Vol2Vol(
...     moving_volume="func.nii.gz",
...     output_volume="func-in-tal.2mm.mgh",
...     registration_file="register.dat",
...     resample_to_talairach=True,
...     talairach_resolution=2,
... )
>>> task.cmdline
'mri_vol2vol --mov func.nii.gz --o func-in-tal.2mm.mgh --reg register.dat --tal --talres 2'

6. Apply an MNI transform by resampling the anatomical data into talairach space:

>>> task = Vol2Vol(
...     moving_volume="orig.mgz",
...     target_volume="$FREESURFER_HOME/average/mni305.cor.mgz",
...     output_volume="orig-in-mni305.mgz",
...     xfm_registration_file="transforms/talairach.xfm",
... )
>>> task.cmdline
'mri_vol2vol --mov orig.mgz --targ $FREESURFER_HOME/average/mni305.cor.mgz --o orig-in-mni305.mgz \
--xfm transforms/talairach.xfm'
"""

__all__ = ["Vol2Vol"]

from attrs import define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask

from .. import specs


@define(kw_only=True)
class Vol2VolSpec(ShellSpec):
    """Specifications for mri_vol2vol."""

    moving_volume: str = field(metadata={"help_string": "moving volume", "argstr": "--mov"})

    target_volume: str = field(metadata={"help_string": "target volume", "argstr": "--targ"})

    output_volume: str = field(metadata={"help_string": "output volume", "argstr": "--o"})

    registration_file: str = field(
        metadata={"help_string": "registration file in FreeSurfer format", "argstr": "--reg"}
    )

    use_registered_volume_as_target: bool = field(
        metadata={
            "help_string": "use volume in registration file as target",
            "argstr": "--fstarg",
            "requires": {"registration_file"},
        }
    )

    fsl_registration_file: str = field(metadata={"help_string": "registration file in FSL format", "argstr": "--fsl"})

    xfm_registration_file: str = field(metadata={"help_string": "registration file in XFM format", "argstr": "--xfm"})

    resample_to_talairach: bool = field(
        metadata={"help_string": "resample moving volume to Talairach", "argstr": "--tal"}
    )

    talairach_resolution: int = field(
        metadata={
            "help_string": "resolution of the Talairach template",
            "argstr": "--talres",
            "allowed_values": {1, 2},
            "requires": ["resample_to_talairach"],
        }
    )

    invert_transform: bool = field(metadata={"help_string": "invert transform", "argstr": "--inv"})

    no_resampling: bool = field(
        metadata={"help_string": "change the vox2ras matrix instead of resampling", "argstr": "--no-resample"}
    )

    interpolation: str = field(
        metadata={
            "help_string": "interpolate output with the chosen method",
            "argstr": "--interp",
            "allowed_values": {"cubic", "nearest", "trilin"},
        }
    )


class Vol2Vol(ShellCommandTask):
    """Task definition for mri_vol2vol."""

    executable = "mri_vol2vol"

    input_spec = SpecInfo(name="Input", bases=(Vol2VolSpec, specs.SubjectsDirSpec))
