from pydra.engine.specs import ShellOutSpec, ShellSpec, SpecInfo

from pydra import ShellCommandTask

__all__ = ["TkRegister2"]


class TkRegister2(ShellCommandTask):
    """Task for tkregister2.

    tkregister2 is a tool to assist in the manual tuning of the linear registration between two volumes, mainly for the
    purpose of interacting with the FreeSurfer anatomical stream.

    Examples
    --------

    1. Create a registration matrix between the conformed space (orig.mgz) and the native anatomical (rawavg.mgz):

    >>> task = TkRegister2(
    ...     moving_volume="rawavg.mgz",
    ...     target_volume="orig.mgz",
    ...     registration_file="register.native.dat",
    ...     init_registration_from_headers=True,
    ... )
    >>> task.cmdline
    'tkregister2 --noedit --mov rawavg.mgz --targ orig.mgz --reg register.native.dat --regheader'

    2. Create a registration matrix for a smaller field-of-view of the talairach atlas:

    >>> task = TkRegister2(
    ...     target_volume="mni305.cor.mgz",
    ...     moving_volume="mni305.cor.subfov1.mgz",
    ...     init_registration_from_headers=True,
    ...     registration_file="mni305.cor.subfov1.reg",
    ...     subject_id="fsaverage",
    ... )
    >>> task.cmdline
    'tkregister2 --noedit --mov mni305.cor.subfov1.mgz --targ mni305.cor.mgz --reg mni305.cor.subfov1.reg --regheader \
--s fsaverage'
    """

    input_spec = SpecInfo(
        name="TkRegister2Input",
        fields=[
            (
                "moving_volume",
                str,
                {
                    "help_string": "moving volume",
                    "mandatory": True,
                    "argstr": "--mov {moving_volume}",
                },
            ),
            (
                "target_volume",
                str,
                {
                    "help_string": "target volume",
                    "argstr": "--targ {target_volume}",
                    "xor": {"fs_target_volume"},
                },
            ),
            (
                "fs_target_volume",
                bool,
                {
                    "help_string": "use T1 volume from subject found in the input registration matrix",
                    "argstr": "--fstarg",
                    "xor": {"target_volume"},
                },
            ),
            (
                "registration_file",
                str,
                {
                    "help_string": "input or output registration file",
                    "argstr": "--reg {registration_file}",
                    "output_file_template": "{registration_file}",
                },
            ),
            (
                "init_registration_from_headers",
                bool,
                {
                    "help_string": "compute the initial registration from the input volumes headers",
                    "argstr": "--regheader",
                },
            ),
            (
                "subject_id",
                str,
                {
                    "help_string": "user defined subject identifier",
                    "argstr": "--s {subject_id}",
                },
            ),
            (
                "subjects_dir",
                str,
                {
                    "help_string": "user defined subjects directory",
                    "argstr": "--sd {subjects_dir}",
                },
            ),
        ],
        bases=(ShellSpec,),
    )

    output_spec = SpecInfo(
        name="TkRegisterOutput",
        fields=[],
        bases=(ShellOutSpec,),
    )

    executable = "tkregister2 --noedit"
