import logging

from .catalog import Catalog
from .nrsur_result import NRsurResult
from .style import set_style
from ._version import __version__

__website__ = "https://nrsur-catalog.github.io/NRSurCat-1"
__uri__ = "https://github.com/nrsur-catalog/nrsur_catalog"
__author__ = "NRSurrogate Catalog Team"
__email__ = "avi.vajpeyi@gmail.com"
__license__ = "MIT"
__description__ = "GW event posteriors obtained using numerical relativity surrogate models"
__copyright__ = "Copyright 2023 NRSurrogate Catalog Team"
__contributors__ = "https://github.com/nrsur-catalog/nrsur_catalog/graphs/contributors"

logging.getLogger("bilby").setLevel(logging.ERROR)
set_style()
