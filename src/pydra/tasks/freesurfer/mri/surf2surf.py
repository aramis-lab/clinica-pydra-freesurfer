"""
parcellation_tableSurf2Surf
============

Resamples data from one surface onto another. If both the source and
target subjects are the same, this is just a format conversion.

Examples
--------
1. Resample a subject's thickness of the left cortical hemisphere on to a 7th order
icosahedron and save in analyze4d format:

>>> task = Surf2Surf(
...     hemisphere="lh",
...     source_subject_id="bert",
...     source_surface="thickness",
...     source_format="curv",
...     target_subject_id="ico",
...     target_icosahedron_order=7,
...     target_surface="bert-thickness-lh.img",
...     target_format="analyze4d",
... )
>>> task.cmdline
'mri_surf2surf --srcsubject bert --sval thickness --sfmt curv --trgsubject ico --trgicoorder 7 \
--tval bert-thickness-lh.img --tfmt analyze4d --hemi lh'

2. Resample data on the icosahedron to the right hemisphere of subject bert:

>>> task = Surf2Surf(
...     hemisphere="rh",
...     source_subject_id="ico",
...     source_surface="icodata-rh.mgh",
...     target_subject_id="bert",
...     target_surface="bert-ico-rh.mgh",
... )
>>> task.cmdline
'mri_surf2surf --srcsubject ico --sval icodata-rh.mgh --trgsubject bert --tval bert-ico-rh.mgh --hemi rh'

3. Convert the surface coordinates of the lh.white of a subject to a (talairach) average:

>>> task = Surf2Surf(
...     source_subject_id="yoursubject",
...     use_vertex_coordinates_in_talairach="white",
...     target_subject_id="youraveragesubject",
...     target_surface="lh.white.yoursubject",
...     save_vertex_coordinates_from_file="$SUBJECTS_DIR/fsaverage/mri/orig.mgz",
... )
>>> task.cmdline
'mri_surf2surf --srcsubject yoursubject --sval-tal-xyz white --trgsubject youraveragesubject \
--tval lh.white.yoursubject --tval-xyz $SUBJECTS_DIR/fsaverage/mri/orig.mgz'

4. Convert the surface coordinates of the lh.white of a subject to the subject's functional space:

>>> task = Surf2Surf(
...     registration_file="register.lta",
...     hemisphere="lh",
...     use_vertex_coordinates_in_surface="white",
...     save_vertex_coordinates_from_file="template.nii.gz",
...     target_surface="./lh.white.func",
...     source_subject_id="yoursubject",
... )
>>> task.cmdline
'mri_surf2surf --srcsubject yoursubject --sval-xyz white --reg register.lta --tval ./lh.white.func \
--tval-xyz template.nii.gz --hemi lh'


5. Extract surface normals of the white surface and save in a volume-encoded file:

>>> task = Surf2Surf(
...     source_subject_id="yoursubject",
...     hemisphere="lh",
...     use_vertex_normal_coordinates="white",
...     target_surface="lh.white.norm.mgh",
... )
>>> task.cmdline
'mri_surf2surf --srcsubject yoursubject --sval-nxyz white --tval lh.white.norm.mgh --hemi lh'

6. Convert the annotation for one subject to the surface of another:

>>> task = Surf2Surf(
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

__all__ = ["Surf2Surf"]

from os import PathLike
from typing import Sequence, Tuple

from attrs import define, field
from pydra.engine.specs import ShellSpec, SpecInfo
from pydra.engine.task import ShellCommandTask

from .. import specs


@define(kw_only=True)
class Surf2SurfSpec(ShellSpec):
    """Specifications for mri_surf2surf."""

    source_subject_id: str = field(
        metadata={
            "help_string": "source subject identifier within FreeSurfer's subjects directory",
            "argstr": "--srcsubject",
        }
    )

    source_surface: str = field(
        metadata={
            "help_string": "source surface file",
            "argstr": "--sval",
        }
    )

    use_vertex_coordinates_in_surface: str = field(
        metadata={
            "help_string": "extract coordinates for each vertex of the surface",
            "argstr": "--sval-xyz",
            "xor": {
                "use_vertex_coordinates_in_talairach",
                "use_vertex_area",
                "use_vertex_normal_coordinates",
            },
        }
    )

    use_vertex_coordinates_in_talairach: str = field(
        metadata={
            "help_string": "extract coordinates for each vertex and transform them to Talairach",
            "argstr": "--sval-tal-xyz",
            "xor": {
                "use_vertex_coordinates_in_surface",
                "use_vertex_area",
                "use_vertex_normal_coordinates",
            },
        }
    )

    use_vertex_area: str = field(
        metadata={
            "help_string": "extract surface area for each vertex of the surface",
            "argstr": "--sval-area",
            "xor": {
                "use_vertex_coordinates_in_surface",
                "use_vertex_coordinates_in_talairach",
                "use_vertex_normal_coordinates",
            },
        }
    )

    use_vertex_normal_coordinates: str = field(
        metadata={
            "help_string": "extract surface normal coordinates for each vertex of the surface",
            "argstr": "--sval-nxyz",
            "xor": {
                "use_vertex_coordinates_in_surface",
                "use_vertex_coordinates_in_talairach",
                "use_vertex_area",
            },
        }
    )

    source_annotation_file: str = field(
        metadata={
            "help_string": "source annotation file",
            "argstr": "--sval-annot",
            "requires": {"target_annotation_file"},
        }
    )

    source_format: str = field(
        metadata={
            "help_string": "source format type string",
            "argstr": "--sfmt",
        }
    )

    source_icosahedron_order: int = field(
        metadata={
            "help_string": "source icosahedron order number",
            "argstr": "--srcicoorder",
        }
    )

    registration_file: str = field(
        metadata={
            "help_string": "apply registration to vertex coordinates",
            "argstr": "--reg",
            "requires": {"use_vertex_coordinates_in_surface"},
            "xor": {"inverse_registration_file"},
        }
    )

    inverse_registration_file: str = field(
        metadata={
            "help_string": "apply inverse registration to vertex coordinates",
            "argstr": "--reg-inv",
            "requires": {"use_vertex_coordinates_in_surface"},
            "xor": {"registration_file"},
        }
    )

    target_subject_id: str = field(
        metadata={
            "help_string": "target subject identifier within FreeSurfer's subjects directory",
            "argstr": "--trgsubject",
        }
    )

    target_icosahedron_order: int = field(
        metadata={
            "help_string": "target icosahedron order number",
            "argstr": "--trgicoorder",
        }
    )

    target_surface: str = field(
        metadata={
            "help_string": "target surface file",
            "argstr": "--tval",
            "xor": {"target_annotation_file"},
        }
    )

    save_vertex_coordinates_from_file: str = field(
        metadata={
            "help_string": "save target surface with different vertex coordinates",
            "argstr": "--tval-xyz",
            "requires": {"target_surface"},
        }
    )

    target_annotation_file: str = field(
        metadata={
            "help_string": "target annotation file",
            "argstr": "--tval",
            "xor": {"target_surface"},
        }
    )

    target_format: str = field(
        metadata={
            "help_string": "target format type string",
            "argstr": "--tfmt",
        }
    )


class Surf2Surf(ShellCommandTask):
    """Task definition for mri_surf2surf."""

    input_spec = SpecInfo(name="Input", bases=(Surf2SurfSpec, specs.HemisphereSpec, specs.SubjectsDirSpec))

    executable = "mri_surf2surf"
