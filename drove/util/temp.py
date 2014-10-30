#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""This module provides utilities related with temporary files
and directories which are auto-removed
"""

import shutil
import tempfile
import contextlib


@contextlib.contextmanager
def directory():
    """Create temporary directory and destroy it after use

    >>> with directory() as d:
    ...    # do stuff
    """
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)
