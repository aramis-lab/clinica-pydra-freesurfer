"""Pydra tasks for FreeSurfer.

Core interfaces can be imported directly from the package namespace.

>>> from pydra.tasks.freesurfer import MRIConvert

Some modules such as :mod:`recon_all` provide additional interfaces for advanced
use cases. Those interfaces have to be imported from their corresponding subpackage.

>>> from pydra.tasks.freesurfer.recon_all import BaseReconAll, LongReconAll

.. automodule:: pydra.tasks.freesurfer.gtmseg
.. automodule:: pydra.tasks.freesurfer.mri_convert
.. automodule:: pydra.tasks.freesurfer.mri_surf2surf
.. automodule:: pydra.tasks.freesurfer.mri_vol2vol
.. automodule:: pydra.tasks.freesurfer.mris_expand
.. automodule:: pydra.tasks.freesurfer.mris_preproc
.. automodule:: pydra.tasks.freesurfer.recon_all
.. automodule:: pydra.tasks.freesurfer.tkregister2
"""
from .gtmseg import GTMSeg
from .mri_convert import MRIConvert
from .mri_surf2surf import MRISurf2Surf
from .mri_vol2vol import MRIVol2Vol
from .mris_expand import MRISExpand
from .mris_preproc import MRISPreproc
from .recon_all import ReconAll
from .tkregister2 import TkRegister2

__all__ = [
    "GTMSeg",
    "MRIConvert",
    "MRISurf2Surf",
    "MRIVol2Vol",
    "MRISExpand",
    "MRISPreproc",
    "ReconAll",
    "TkRegister2",
]
