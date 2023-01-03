"""
The cross-sectional processing interface to `recon-all` is available through the following import statement:

>>> from pydra.tasks.freesurfer.recon_all import ReconAll

In addition, the longitudinal processing interfaces to `recon-all` are available using this set of imports:

>>> from pydra.tasks.freesurfer.recon_all import BaseReconAll, LongReconAll

1. Cross-sectionally process timepoints:
>>> task = ReconAll(
...     subject_id="tp1",
...     t1_volume_file="/path/to/tp1.dcm",
... )
>>> task.cmdline
'recon-all -subjid tp1 -i /path/to/tp1.dcm -all'

2. Create and process the unbiased base template:
>>> task = BaseReconAll(
...     base_template_id="longbase",
...     base_timepoint_ids=["tp1", "tp2"],
... )
>>> task.cmdline
'recon-all -base longbase -base-tp tp1 -base-tp tp2 -all'

3. Longitudinally process timepoints:
>>> task = LongReconAll(
...    longitudinal_timepoint_id="tp1",
...    longitudinal_template_id="longbase",
... )
>>> task.cmdline
'recon-all -long tp1 longbase -all'
"""

from .base_recon_all import BaseReconAll
from .long_recon_all import LongReconAll
from .recon_all import ReconAll

__all__ = ["ReconAll", "BaseReconAll", "LongReconAll"]
