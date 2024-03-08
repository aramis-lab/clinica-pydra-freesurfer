"""
Coreg
=====

Perform linear registration between two volumes similar to SPM's spm_coreg.

Examples
--------

>>> task = Coreg(source_volume="template.nii", target_volume="orig.mgz", degrees_of_freedom=12)
>>> task.cmdline    # doctest: +ELLIPSIS
'mri_coreg --mov template.nii --ref orig.mgz --reg .../template_coreg.lta --regdat .../template_coreg.dat --dof 12 ...'
"""

__all__ = ["Coreg"]

from os import PathLike

from attrs import define, field

from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


@define(kw_only=True)
class CoregSpec(ShellSpec):
    """Specifications for mri_coreg."""

    source_volume: PathLike = field(metadata={"help_string": "source volume", "mandatory": True, "argstr": "--mov"})

    target_volume: PathLike = field(metadata={"help_string": "target volume", "mandatory": True, "argstr": "--ref"})

    output_registration_file: str = field(
        metadata={
            "help_string": "output registration file",
            "argstr": "--reg",
            "output_file_template": "{source_volume}_coreg.lta",
            "keep_extension": False,
        }
    )

    output_registration_data: str = field(
        metadata={
            "help_string": "output registration data",
            "argstr": "--regdat",
            "output_file_template": "{source_volume}_coreg.dat",
            "keep_extension": False,
        }
    )

    subject_id: str = field(
        metadata={"help_string": "use subject's aparc+aseg.mgz as target mask", "argstr": "--s", "xor": {"target_mask"}}
    )

    degrees_of_freedom: int = field(default=6, metadata={"help_string": "degrees of freedom", "argstr": "--dof"})

    source_mask: PathLike = field(metadata={"help_string": "mask for source volume", "argstr": "--mov-mask"})

    target_mask: PathLike = field(
        metadata={"help_string": "mask for target volume", "argstr": "--ref-mask", "xor": {"subject_id"}}
    )

    num_threads: int = field(metadata={"help_string": "number of threads", "argstr": "--threads"})

    subjects_dir: PathLike = field(metadata={"help_string": "subjects directory", "argstr": "--sd"})

    random_seed: int = field(default=53, metadata={"help_string": "random seed", "argstr": "--seed"})


class Coreg(ShellCommandTask):
    """Task definition for mri_coreg."""

    executable = "mri_coreg"

    input_spec = SpecInfo(name="Input", bases=(CoregSpec,))
