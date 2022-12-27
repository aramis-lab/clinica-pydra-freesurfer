import os

from pydra.tasks.freesurfer.recon_all import recon_all


def test_executable():
    assert recon_all.ReconAll.executable == "recon-all"
