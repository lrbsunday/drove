#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
import sys
import drove.script
from nose.tools import with_setup
from nose.tools import raises


_exit = sys.exit
_dirname = os.path.dirname
_args = sys.argv


def _teardown():
    sys.exit = _exit
    os.path.dirname = _dirname
    sys.argv = _args


@with_setup(teardown=_teardown)
def test_script():
    """Testing script: basic behaviour"""
    sys.exit = lambda x: None
    sys.argv = ["prog", "-h"]
    drove.script.cli()
    sys.argv = ["prog", "-np", "-v", "-C", "./test/config/empty.yml"]
    os.path.dirname = lambda x: ""
    sys.argv = ["prog", "-np"]
    drove.script.cli()
    sys.argv = ["prog", "-np", "-s", "key=value"]
    drove.script.cli()

