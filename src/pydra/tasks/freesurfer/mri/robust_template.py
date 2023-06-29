"""
RobustTemplate
==============

Examples
--------

>>> task = RobustTemplate(
...     input_volumes=["tp1.mgz", "tp2.mgz", "tp3.mgz"],
...     output_volume="mean.mgz",
...     output_transforms=["tp1.lta", "tp2.lta", "tp3.lta"],
...     method="mean",
...     enable_intensity_scaling=True,
... )
>>> task.cmdline
'mri_robust_template --mov tp1.mgz tp2.mgz tp3.mgz --template mean.mgz --satit --lta tp1.lta tp2.lta tp3.lta \
--average 0 --iscale'
"""

__all__ = ["RobustTemplate"]

from os import PathLike
from typing import Sequence

from attrs import define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask


@define(kw_only=True)
class RobustTemplateSpec(ShellSpec):
    """Specifications for mri_robust_template."""

    input_volumes: Sequence[PathLike] = field(
        metadata={"help_string": "input volumes to be compute template from", "argstr": "--mov"}
    )

    output_volume: str = field(
        metadata={
            "help_string": "output template volume",
            "argstr": "--template",
            "output_file_template": "template.mgz",
        }
    )

    saturation: float = field(
        metadata={
            "help_string": "set outlier sensitivity or auto-detect it",
            "formatter": lambda saturation: f"--sat {saturation}" if saturation else "--satit",
        }
    )

    output_transforms: Sequence[PathLike] = field(
        metadata={"help_string": "output transforms to template space", "argstr": "--lta"}
    )

    output_resampled_volumes: Sequence[PathLike] = field(
        metadata={"help_string": "output resampled volumes to template space", "argstr": "--mapmov"}
    )

    output_weights_volumes: Sequence[PathLike] = field(
        metadata={"help_string": "output weights volumes to template space", "argstr": "--weights"}
    )

    method: str = field(
        default="median",
        metadata={
            "help_string": "--average",
            "allowed_values": {"mean", "median"},
            "formatter": lambda method: "--average {}".format({"mean": "0", "median": "1"}.get(method)),
        },
    )

    initial_template_index: int = field(
        metadata={"help_string": "volume index used as initial template", "argstr": "--inittp"}
    )

    resample_to_initial_template: bool = field(
        metadata={"help_string": "resample other volumes to initial template", "argstr": "--fixtp"}
    )

    enable_intensity_scaling: bool = field(metadata={"help_string": "enable intensity scaling", "argstr": "--iscale"})

    initial_transforms: PathLike = field(
        metadata={"help_string": "initial transforms to apply to input volumes", "argstr": "--ixforms"}
    )

    find_affine_transform: bool = field(
        metadata={"help_string": "find 12-parameter affine transform", "argstr": "--affine"}
    )

    internal_datatype: str = field(
        metadata={
            "help_string": "force internal datatype to float or double",
            "allowed_values": {"float", "double"},
            "formatter": lambda internal_datatype: (
                {"float": "--floattype", "double": "--doubleprec"}.get(internal_datatype, "")
            ),
        }
    )


class RobustTemplate(ShellCommandTask):
    """Task definition for mri_robust_template."""

    executable = "mri_robust_template"

    input_spec = SpecInfo(name="Input", bases=(RobustTemplateSpec,))
