import os
import typing as ty

import attrs

import pydra

from ..specs import SubjectsDirOutSpec as ReconAllBaseOutSpec

__all__ = ["ReconAllBaseSpec", "ReconAllBaseOutSpec"]

# FIXME: Change to ty.Tuple[float, float, float] once Pydra supports it, if ever.
SeedPoint = ty.List[float]


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

    custom_brain_mask_file: os.PathLike = attrs.field(
        metadata={
            "help_string": "use a custom brain mask",
            "argstr": "-xmask",
        },
    )

    hemisphere: str = attrs.field(
        metadata={
            "help_string": "restrict processing to this hemisphere",
            "argstr": "-hemi {hemisphere}",
            "allowed_values": ["lh", "rh"],
        },
    )

    pons_seed_point: SeedPoint = attrs.field(
        metadata={
            "help_string": "col, row, slice of seed point for pons",
            "argstr": "-pons-crs",
        }
    )

    corpus_callosum_seed_point: SeedPoint = attrs.field(
        metadata={
            "help_string": "col, row, slice of seed point for corpus callosum",
            "argstr": "-cc-crs",
        }
    )

    left_hemisphere_seed_point: SeedPoint = attrs.field(
        metadata={
            "help_string": "col, row, slice of seed point for left hemisphere",
            "argstr": "-lh-crs",
        }
    )

    right_hemisphere_seed_point: SeedPoint = attrs.field(
        metadata={
            "help_string": "col, row, slice of seed point for right hemisphere",
            "argstr": "-rh-crs",
        }
    )

    custom_talairach_atlas_file: os.PathLike = attrs.field(
        metadata={
            "help_string": "use a custom talairach atlas",
            "argstr": "-custom-tal-atlas",
        }
    )

    deface: bool = attrs.field(
        metadata={
            "help_string": "deface subject",
            "argstr": "-deface",
        }
    )

    no_subcortical_segmentation: bool = attrs.field(
        metadata={
            "help_string": "skip subcortical segmentation steps",
            "argstr": "-nosubcortseg",
        }
    )

    conform_width_to_256: bool = attrs.field(
        metadata={
            "help_string": (
                "conform image dimensions to 256 when running mri_convert",
            ),
            "argstr": "-cw256",
        }
    )

    cache_files_for_qdec: bool = attrs.field(
        metadata={
            "help_string": (
                "accelerate analysis of group data "
                "by pre-computing files required for the Qdec utility"
            ),
            "argstr": "-qcache",
        }
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
