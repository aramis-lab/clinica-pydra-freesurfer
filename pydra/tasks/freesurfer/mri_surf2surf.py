"""
MRISurf2Surf
============

Resamples data from one surface onto another. If both the source and
target subjects are the same, this is just a format conversion.

Examples
--------
1. Resample a subject's thickness of the left cortical hemisphere on to a 7th order
icosahedron and save in analyze4d format:

>>> task = MRISurf2Surf(
...     hemisphere="lh",
...     source_subject_id="bert",
...     source_surface_file="thickness",
...     source_format="curv",
...     target_subject_id="ico",
...     target_icosahedron_order=7,
...     target_surface_file="bert-thickness-lh.img",
...     target_format="analyze4d",
... )
>>> task.cmdline
'mri_surf2surf --srcsubject bert --sval thickness --sfmt curv --trgsubject ico --trgicoorder 7 \
--tval bert-thickness-lh.img --tfmt analyze4d --hemi lh'

2. Resample data on the icosahedron to the right hemisphere of subject bert:

>>> task = MRISurf2Surf(
...     hemisphere="rh",
...     source_subject_id="ico",
...     source_surface_file="icodata-rh.mgh",
...     target_subject_id="bert",
...     target_surface_file="bert-ico-rh.mgh",
... )
>>> task.cmdline
'mri_surf2surf --srcsubject ico --sval icodata-rh.mgh --trgsubject bert --tval bert-ico-rh.mgh --hemi rh'

3. Convert the surface coordinates of the lh.white of a subject to a (talairach) average:

>>> task = MRISurf2Surf(
...     source_subject_id="yoursubject",
...     use_vertex_coordinates_in_talairach_from_surface="white",
...     target_subject_id="youraveragesubject",
...     target_surface_file="lh.white.yoursubject",
...     save_target_with_vertex_coordinates_from_file="$SUBJECTS_DIR/fsaverage/mri/orig.mgz",
... )
>>> task.cmdline
'mri_surf2surf --srcsubject yoursubject --sval-tal-xyz white --trgsubject youraveragesubject \
--tval lh.white.yoursubject --tval-xyz $SUBJECTS_DIR/fsaverage/mri/orig.mgz'

4. Convert the surface coordinates of the lh.white of a subject to the subject's functional space:

>>> task = MRISurf2Surf(
...     registration_file="register.lta",
...     hemisphere="lh",
...     use_vertex_coordinates_from_surface="white",
...     save_target_with_vertex_coordinates_from_file="template.nii.gz",
...     target_surface_file="./lh.white.func",
...     source_subject_id="yoursubject",
... )
>>> task.cmdline
'mri_surf2surf --srcsubject yoursubject --sval-xyz white --reg register.lta --tval ./lh.white.func \
--tval-xyz template.nii.gz --hemi lh'


5. Extract surface normals of the white surface and save in a volume-encoded file:

>>> task = MRISurf2Surf(
...     source_subject_id="yoursubject",
...     hemisphere="lh",
...     use_vertex_normal_coordinates_from_surface="white",
...     target_surface_file="lh.white.norm.mgh",
... )
>>> task.cmdline
'mri_surf2surf --srcsubject yoursubject --sval-nxyz white --tval lh.white.norm.mgh --hemi lh'

6. Convert the annotation for one subject to the surface of another:

>>> task = MRISurf2Surf(
...     source_subject_id="subj1",
...     target_subject_id="subj2",
...     hemisphere="lh",
...     source_annotation_file="$SUBJECTS_DIR/subj1/label/lh.aparc.annot",
...     target_annotation_file="$SUBJECTS_DIR/subj2/label/lh.subj1.aparc.annot",
... )
>>> task.cmdline
'mri_surf2surf --srcsubject subj1 --sval-annot $SUBJECTS_DIR/subj1/label/lh.aparc.annot --trgsubject subj2 \
--tval $SUBJECTS_DIR/subj2/label/lh.subj1.aparc.annot --hemi lh'


"""
import attrs

import pydra

from . import specs

__all__ = ["MRISurf2Surf"]


@attrs.define(slots=False, kw_only=True)
class MRISurf2SurfSpec(pydra.specs.ShellSpec):
    """Specifications for mri_surf2surf."""

    source_subject_id: str = attrs.field(
        metadata={
            "help_string": "source subject identifier within FreeSurfer's subjects directory",
            "argstr": "--srcsubject",
        }
    )

    source_surface_file: str = attrs.field(
        metadata={
            "help_string": "source surface file",
            "argstr": "--sval",
        }
    )

    use_vertex_coordinates_from_surface: str = attrs.field(
        metadata={
            "help_string": "extract coordinates for each vertex of the surface",
            "argstr": "--sval-xyz",
            "xor": {
                "use_vertex_coordinates_in_talairach_from_surface",
                "use_vertex_area_from_surface",
                "use_vertex_normal_coordinates_from_surface",
            },
        }
    )

    use_vertex_coordinates_in_talairach_from_surface: str = attrs.field(
        metadata={
            "help_string": "extract coordinates and transform them to Talairach for each vertex of the surface",
            "argstr": "--sval-tal-xyz",
            "xor": {
                "use_vertex_coordinates_from_surface",
                "use_vertex_area_from_surface",
                "use_vertex_normal_coordinates_from_surface",
            },
        }
    )

    use_vertex_area_from_surface: str = attrs.field(
        metadata={
            "help_string": "extract surface area for each vertex of the surface",
            "argstr": "--sval-area",
            "xor": {
                "use_vertex_coordinates_from_surface",
                "use_vertex_coordinates_in_talairach_from_surface",
                "use_vertex_normal_coordinates_from_surface",
            },
        }
    )

    use_vertex_normal_coordinates_from_surface: str = attrs.field(
        metadata={
            "help_string": "extract surface normal coordinates for each vertex of the surface",
            "argstr": "--sval-nxyz",
            "xor": {
                "use_vertex_coordinates_from_surface",
                "use_vertex_coordinates_in_talairach_from_surface",
                "use_vertex_area_from_surface",
            },
        }
    )

    source_annotation_file: str = attrs.field(
        metadata={
            "help_string": "source annotation file",
            "argstr": "--sval-annot",
            "requires": {"target_annotation_file"},
        }
    )

    source_format: str = attrs.field(
        metadata={
            "help_string": "source format type string",
            "argstr": "--sfmt",
        }
    )

    source_icosahedron_order: int = attrs.field(
        metadata={
            "help_string": "source icosahedron order number",
            "argstr": "--srcicoorder",
        }
    )

    registration_file: str = attrs.field(
        metadata={
            "help_string": "apply registration to vertex coordinates",
            "argstr": "--reg",
            "requires": {"use_vertex_coordinates_from_surface"},
            "xor": {"inverse_registration_file"},
        }
    )

    inverse_registration_file: str = attrs.field(
        metadata={
            "help_string": "apply inverse registration to vertex coordinates",
            "argstr": "--reg-inv",
            "requires": {"use_vertex_coordinates_from_surface"},
            "xor": {"registration_file"},
        }
    )

    target_subject_id: str = attrs.field(
        metadata={
            "help_string": "target subject identifier within FreeSurfer's subjects directory",
            "argstr": "--trgsubject",
        }
    )

    target_icosahedron_order: int = attrs.field(
        metadata={
            "help_string": "target icosahedron order number",
            "argstr": "--trgicoorder",
        }
    )

    target_surface_file: str = attrs.field(
        metadata={
            "help_string": "target surface file",
            "argstr": "--tval",
            "xor": {"target_annotation_file"},
        }
    )

    save_target_with_vertex_coordinates_from_file: str = attrs.field(
        metadata={
            "help_string": "save target surface with different vertex coordinates",
            "argstr": "--tval-xyz",
            "requires": {"target_surface_file"},
        }
    )

    target_annotation_file: str = attrs.field(
        metadata={
            "help_string": "target annotation file",
            "argstr": "--tval",
            "xor": {"target_surface_file"},
        }
    )

    target_format: str = attrs.field(
        metadata={
            "help_string": "target format type string",
            "argstr": "--tfmt",
        }
    )


class MRISurf2Surf(pydra.ShellCommandTask):
    """Task for mri_surf2surf."""

    input_spec = pydra.specs.SpecInfo(
        name="MRISurf2SurfInput",
        bases=(MRISurf2SurfSpec, specs.HemisphereSpec, specs.SubjectsDirSpec),
    )

    executable = "mri_surf2surf"
