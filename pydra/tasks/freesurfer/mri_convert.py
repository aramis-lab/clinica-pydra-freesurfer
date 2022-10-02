from pydra.engine.specs import ShellOutSpec, ShellSpec, SpecInfo

from pydra import ShellCommandTask

__all__ = ["MRIConvert"]


class MRIConvert(ShellCommandTask):
    """Task for mri_convert.

    General purpose utility for converting between different file formats.

    Examples
    --------

    1. Convert data to float:

    >>> task = MRIConvert(
    ...     input_volume="orig.nii.gz",
    ...     output_volume="float.nii.gz",
    ...     output_data_type="float",
    ... )
    >>> task.cmdline
    'mri_convert orig.nii.gz float.nii.gz -odt float'
    """

    input_spec = SpecInfo(
        name="MRIConvertInput",
        fields=[
            (
                "input_volume",
                str,
                {
                    "help_string": "input volume",
                    "mandatory": True,
                    "argstr": "{input_volume}",
                    "position": 1,
                },
            ),
            (
                "output_volume",
                str,
                {
                    "help_string": "output volume",
                    "mandatory": True,
                    "argstr": "{output_volume}",
                    "position": 2,
                    "output_file_template": "{out_volume}",
                },
            ),
            (
                "output_data_type",
                str,
                {
                    "help_string": "output data type",
                    "argstr": "-odt {output_data_type}",
                },
            ),
        ],
        bases=(ShellSpec,),
    )

    output_spec = SpecInfo(
        name="MRIConvertOutput",
        fields=[],
        bases=(ShellOutSpec,),
    )

    executable = "mri_convert"
