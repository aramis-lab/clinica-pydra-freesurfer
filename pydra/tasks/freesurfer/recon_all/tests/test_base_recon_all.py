from pydra.tasks.freesurfer.recon_all.base_recon_all import BaseReconAll


def test_executable():
    assert BaseReconAll.executable == "recon-all"
