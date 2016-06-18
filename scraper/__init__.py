"""
A simple, multithreaded web scraping framework.
"""

from .models import Job, Page
from .spider import BaseScraper


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
