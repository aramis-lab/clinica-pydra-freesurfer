from pydra.tasks.freesurfer.recon_all.long_recon_all import LongReconAll


def test_executable():
    assert LongReconAll.executable == "recon-all"
