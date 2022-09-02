"""Tools for file operations."""

import os
from typing import List


def filter_for_markdown_files_only(file_list: List[str]) -> List[str]:
    """Filters to only return markdown files.

    :param file_list: list of files to filter.
    :return: filtered list of files.
    """
    return [x for x in file_list if os.path.splitext(x)[-1].lower() == ".md"]
