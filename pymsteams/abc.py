"""
pymsteams.abc
~~~~~~~~~~~~~
Abstract Base Classes to help functions
inside the package.
"""

from typing import Literal, Optional

MISSING = object()

class Link:
    """
    |abc|

    Represents a URL or URI and if not, tries to encode one to it.
    """

    @staticmethod
    def convert(string: str, *, encode: Literal['utf-8', 'ascii', 'utf-16', 'utf-32', 'unicode'] = 'utf-8') -> str:
        """
        Converts a string to a URL or URI.
        """

        from urllib.parse import quote

        return quote(string, encoding = encode)