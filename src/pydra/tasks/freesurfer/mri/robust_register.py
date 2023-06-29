"""
RobustRegister
==============

Symmetrically align a source to a target volume
using a method based on robust statistics
to detect outliers and removes them from the registration.

Examples
--------

>>> task = RobustRegister(source_volume="src.mgz", target_volume="trg.mgz")
>>> task.cmdline    # doctest: +ELLIPSIS
'mri_robust_register --mov src.mgz --dst trg.mgz --lta .../src_xfm.lta --satit --mapmov .../src_resampled.mgz \
--mapmovhdr .../src_aligned.mgz --weights .../src_weights.mgz'
"""

__all__ = ["RobustRegister"]

from os import PathLike

from attrs import define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


@define(kw_only=True)
class RobustRegisterSpec(ShellSpec):
    """Specifications for mri_robust_register."""

    source_volume: PathLike = field(metadata={"help_string": "source volume", "mandatory": True, "argstr": "--mov"})

    target_volume: PathLike = field(metadata={"help_string": "target volume", "mandatory": True, "argstr": "--dst"})

    output_transform: str = field(
        metadata={
            "help_string": "output transform",
            "argstr": "--lta",
            "output_file_template": "{source_volume}_xfm.lta",
            "keep_extension": False,
        }
    )

    saturation: float = field(
        metadata={
            "help_string": "set outlier sensitivity or auto-detect it",
            "formatter": lambda saturation: f"--sat {saturation}" if saturation else "--satit",
        }
    )

    output_resampled_volume: str = field(
        metadata={
            "help_string": "source image resampled to target",
            "argstr": "--mapmov",
            "output_file_template": "{source_volume}_resampled",
        }
    )

    output_aligned_volume: str = field(
        metadata={
            "help_string": "source image aligned to target",
            "argstr": "--mapmovhdr",
            "output_file_template": "{source_volume}_aligned",
        }
    )

    output_weights_volume: str = field(
        metadata={
            "help_string": "output weights in target space",
            "argstr": "--weights",
            "output_file_template": "{source_volume}_weights",
        }
    )

    find_translation_only: bool = field(
        metadata={"help_string": "find 3-parameter translation only", "argstr": "--transonly"}
    )

    find_affine_transform: bool = field(
        metadata={"help_string": "find 12-parameter affine transform", "argstr": "--affine"}
    )

    initial_transform: PathLike = field(
        metadata={"help_string": "initial transform to apply to source volume", "argstr": "--ixform"}
    )

    initialize_orientation: bool = field(
        metadata={"help_string": "initialize orientation using moments", "argstr": "--initorient"}
    )

    no_initialization: bool = field(metadata={"help_string": "skip transform initialization", "argstr": "--noinit"})

    internal_datatype: str = field(
        metadata={
            "help_string": "force internal datatype to float or double",
            "allowed_values": {"float", "double"},
            "formatter": lambda internal_datatype: (
                {"float": "--floattype", "double": "--doubleprec"}.get(internal_datatype, "")
            ),
        }
    )

    source_mask: PathLike = field(metadata={"help_string": "mask applied to source volume", "argstr": "--maskmov"})

    target_mask: PathLike = field(metadata={"help_string": "mask applied to target volume", "argstr": "--maskdst"})


class RobustRegister(ShellCommandTask):
    """Task definition for mri_robust_register."""

    executable = "mri_robust_register"

    input_spec = SpecInfo(name="Input", bases=(RobustRegisterSpec,))
