import dataclasses
import os

import pytest

from pydra.tasks.freesurfer.recon_all import ReconAll


@dataclasses.dataclass
class ReconAllInputs:
    subject_id: str = None
    base_template_id: str = None
    longitudinal_template_id: str = None
    longitudinal_timepoint_id: str = None
    subjects_dir: str = None


@pytest.mark.parametrize(
    "inputs,subject_id",
    [
        ({"subject_id": "sub"}, "sub"),
        ({"base_template_id": "base"}, "base"),
        (
            {"longitudinal_template_id": "base", "longitudinal_timepoint_id": "tp"},
            "tp.long.base",
        ),
    ],
)
def test_get_output_subject_id(inputs, subject_id):
    assert ReconAll.get_output_subject_id(ReconAllInputs(**inputs)) == subject_id


def test_get_output_subjects_dir_as_input():
    subjects_dir = "/path/to/subjects/dir"

    assert (
        ReconAll.get_output_subjects_dir(ReconAllInputs(subjects_dir=subjects_dir))
        == subjects_dir
    )


def test_get_output_subjects_dir_as_envvar():
    subjects_dir = "/path/to/subjects/dir"
    os.environ["SUBJECTS_DIR"] = subjects_dir

    assert ReconAll.get_output_subjects_dir(ReconAllInputs()) == subjects_dir
