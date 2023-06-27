__all__ = ["ReconAllBaseSpec", "ReconAllBaseOutSpec"]

from os import PathLike
from typing import List

from attrs import define, field
from pydra.engine.specs import ShellSpec

from ..specs import SubjectsDirOutSpec

# FIXME: Change to ty.Tuple[float, float, float] once Pydra supports it, if ever.
SeedPoint = List[float]


@define(slots=False, kw_only=True)
class ReconAllBaseSpec(ShellSpec):
    """Base specifications for recon-all."""

    directive: str = field(
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

    custom_brain_mask: PathLike = field(metadata={"help_string": "custom brain mask", "argstr": "-xmask"})

    hemisphere: str = field(
        metadata={
            "help_string": "restrict processing to this hemisphere",
            "argstr": "-hemi",
            "allowed_values": ["lh", "rh"],
            "xor": {"parallel"},
        }
    )

    pons_seed_point: SeedPoint = field(metadata={"help_string": "seed point for pons", "argstr": "-pons-crs"})

    corpus_callosum_seed_point: SeedPoint = field(
        metadata={"help_string": "seed point for corpus callosum", "argstr": "-cc-crs"}
    )

    left_hemisphere_seed_point: SeedPoint = field(
        metadata={"help_string": "seed point for left hemisphere", "argstr": "-lh-crs"}
    )

    right_hemisphere_seed_point: SeedPoint = field(
        metadata={"help_string": "seed point for right hemisphere", "argstr": "-rh-crs"}
    )

    custom_talairach_atlas: PathLike = field(
        metadata={"help_string": "use a custom talairach atlas", "argstr": "-custom-tal-atlas"}
    )

    deface: bool = field(metadata={"help_string": "deface subject", "argstr": "-deface"})

    no_subcortical_segmentation: bool = field(
        metadata={"help_string": "skip subcortical segmentation steps", "argstr": "-nosubcortseg"}
    )

    conform_width_to_256: bool = field(
        metadata={"help_string": "conform image dimensions to 256 when running mri_convert", "argstr": "-cw256"}
    )

    cache_files_for_qdec: bool = field(
        metadata={
            "help_string": "accelerate analysis of group data by pre-computing files required for the Qdec utility",
            "argstr": "-qcache",
        }
    )

    parallel: bool = field(
        metadata={"help_string": "process both hemispheres in parallel", "argstr": "-parallel", "xor": ["hemisphere"]}
    )

    num_threads: int = field(metadata={"help_string": "set number of threads to use", "argstr": "-threads"})

    subjects_dir: PathLike = field(
        metadata={"help_string": "subjects directory processed by FreeSurfer", "argstr": "-sd"}
    )


class ReconAllBaseOutSpec(SubjectsDirOutSpec):
    """Base output specifications for recon-all."""
