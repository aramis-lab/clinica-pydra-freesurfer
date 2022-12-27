import os

from pydra.tasks.freesurfer.recon_all import specs


def test_get_subjects_dir_from_input():
    subjects_dir = "/path/to/subjects/dir"

    assert (
        specs.ReconAllBaseOutSpec.get_subjects_dir(subjects_dir=subjects_dir)
        == subjects_dir
    )


def test_get_subjects_dir_from_envvar():
    subjects_dir = "/path/to/subjects/dir"
    os.environ["SUBJECTS_DIR"] = subjects_dir

    assert specs.ReconAllBaseOutSpec.get_subjects_dir(subjects_dir=None) == subjects_dir
