import typing as ty

from pydra.engine.specs import ShellOutSpec, ShellSpec, SpecInfo

from pydra import ShellCommandTask

__all__ = ["MRISurf2Surf"]


class MRISurf2Surf(ShellCommandTask):
    """Task for mri_surf2surf.

    Resamples data from one surface onto another. If both the source and
    target subjects are the same, this is just a format conversion.

    Examples
    --------
    1. Resample a subject's thickness of the left cortical hemisphere on to a 7th order icosahedron and save in
    analyze4d format:

    >>> task = MRISurf2Surf(
    ...     hemifield="lh",
    ...     source_subject_id="bert",
    ...     sval="thickness",
    ...     sfmt="curv",
    ...     target_subject_id="ico",
    ...     trgicoorder=7,
    ...     tval="bert-thickness-lh.img",
    ...     tfmt="analyze4d",
    ... )

    2. Resample data on the icosahedron to the right hemisphere of subject bert:

    >>> task.cmdline
    'mri_surf2surf --srcsubject bert --sval thickness --sfmt curv --trgsubject ico --trgicoorder 7 \
--tval bert-thickness-lh.img --tfmt analyze4d --hemi lh'
    >>> task = MRISurf2Surf(
    ...     hemifield="rh",
    ...     source_subject_id="ico",
    ...     sval="icodata-rh.mgh",
    ...     target_subject_id="bert",
    ...     tval="./bert-ico-rh.mgh",
    ... )
    >>> task.cmdline
    'mri_surf2surf --srcsubject ico --sval icodata-rh.mgh --trgsubject bert --tval ./bert-ico-rh.mgh --hemi rh'

    3. Convert the surface coordinates of the lh.white of a subject to a (talairach) average:

    >>> task = MRISurf2Surf(
    ...     source_subject_id="yoursubject",
    ...     sval_tal_xyz="white",
    ...     target_subject_id="youraveragesubject",
    ...     tval="lh.white.yoursubject",
    ...     tval_xyz="$SUBJECTS_DIR/fsaverage/mri/orig.mgz",
    ... )
    >>> task.cmdline
    'mri_surf2surf --srcsubject yoursubject --sval-tal-xyz white --trgsubject youraveragesubject \
--tval lh.white.yoursubject --tval-xyz $SUBJECTS_DIR/fsaverage/mri/orig.mgz'

    4. Convert the surface coordinates of the lh.white of a subject to the subject's functional space:

    >>> task = MRISurf2Surf(
    ...     reg="register.lta",
    ...     hemifield="lh",
    ...     sval_xyz="white",
    ...     tval_xyz="template.nii.gz",
    ...     tval="./lh.white.func",
    ...     source_subject_id="yoursubject",
    ... )
    >>> task.cmdline
    'mri_surf2surf --srcsubject yoursubject --sval-xyz white --reg register.lta --tval ./lh.white.func --tval-xyz template.nii.gz \
--hemi lh'

    5. Extract surface normals of the white surface and save in a volume-encoded file:

    >>> task = MRISurf2Surf(
    ...     source_subject_id="yoursubject",
    ...     hemifield="lh",
    ...     sval_nxyz="white",
    ...     tval="lh.white.norm.mgh",
    ... )
    >>> task.cmdline
    'mri_surf2surf --srcsubject yoursubject --sval-nxyz white --tval lh.white.norm.mgh --hemi lh'

    6. Convert the annotation for one subject to the surface of another:

    >>> task = MRISurf2Surf(
    ...     source_subject_id="subj1",
    ...     target_subject_id="subj2",
    ...     hemifield="lh",
    ...     sval_annot="$SUBJECTS_DIR/subj1/label/lh.aparc.annot",
    ...     tval="$SUBJECTS_DIR/subj2/label/lh.subj1.aparc.annot",
    ... )
    >>> task.cmdline
    'mri_surf2surf --srcsubject subj1 --sval-annot $SUBJECTS_DIR/subj1/label/lh.aparc.annot --trgsubject subj2 --tval \
$SUBJECTS_DIR/subj2/label/lh.subj1.aparc.annot --hemi lh'
    """

    input_spec = SpecInfo(
        name="MRISurf2SurfInput",
        fields=[
            (
                "subjects_dir",
                str,
                {
                    "help_string": "user defined SUBJECTS_DIR",
                    "argstr": "--sd {subjects_dir}",
                },
            ),
            (
                "source_subject_id",
                str,
                {
                    "help_string": "source subject identifier",
                    "mandatory": True,
                    "argstr": "--srcsubject {source_subject_id}",
                },
            ),
            (
                "sval",
                str,
                {
                    "help_string": "source input surface file",
                    "argstr": "--sval {sval}",
                },
            ),
            (
                "sval_xyz",
                str,
                {
                    "help_string": "source input surface file",
                    "argstr": "--sval-xyz {sval_xyz}",
                },
            ),
            (
                "sval_tal_xyz",
                str,
                {
                    "help_string": "source input surface file",
                    "argstr": "--sval-tal-xyz {sval_tal_xyz}",
                },
            ),
            (
                "sval_area",
                str,
                {
                    "help_string": "source input surface file",
                    "argstr": "--sval-area {sval_area}",
                },
            ),
            (
                "sval_nxyz",
                str,
                {
                    "help_string": "source input surface file",
                    "argstr": "--sval-nxyz {sval_nxyz}",
                },
            ),
            (
                "proj_frac",
                ty.Tuple[str, str],
                {
                    "help_string": "",
                    "argstr": "--projfrac {proj_frac}",
                },
            ),
            (
                "projabs",
                ty.Tuple[str, str],
                {
                    "help_string": "",
                    "argstr": "--projabs {projabs}",
                },
            ),
            (
                "sval_annot",
                str,
                {
                    "help_string": (
                        "Map annotation file to the output. The target data will be saved as an annotation."
                    ),
                    "argstr": "--sval-annot {sval_annot}",
                },
            ),
            (
                "sfmt",
                str,
                {
                    "help_string": "source format type string",
                    "argstr": "--sfmt {sfmt}",
                },
            ),
            (
                "reg",
                str,
                {
                    "help_string": "apply register.dat to sval_xyz",
                    "argstr": "--reg...",
                },
            ),
            (
                "srcicoorder",
                int,
                {
                    "help_string": "icosahedron order of the source",
                    "argstr": "--srcicoorder {srcicoorder}",
                },
            ),
            (
                "target_subject_id",
                str,
                {
                    "help_string": "target subject identifier",
                    "argstr": "--trgsubject {target_subject_id}",
                },
            ),
            (
                "trgicoorder",
                int,
                {
                    "help_string": "icosahedron order of the target",
                    "argstr": "--trgicoorder {trgicoorder}",
                },
            ),
            (
                "tval",
                str,
                {
                    "help_string": "target surface file",
                    "argstr": "--tval {tval}",
                },
            ),
            (
                "tval_xyz",
                str,
                {
                    "help_string": "volume in target space",
                    "argstr": "--tval-xyz {tval_xyz}",
                },
            ),
            (
                "tfmt",
                str,
                {
                    "help_string": "target format type string",
                    "argstr": "--tfmt {tfmt}",
                },
            ),
            (
                "hemifield",
                str,
                {
                    "help_string": "hemifield",
                    "argstr": "--hemi {hemifield}",
                },
            ),
        ],
        bases=(ShellSpec,),
    )

    output_spec = SpecInfo(
        name="MRISurf2SurfOutput",
        fields=[],
        bases=(ShellOutSpec,),
    )

    executable = "mri_surf2surf"
