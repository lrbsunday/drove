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
    pid = drove.script.cli()
    os.kill(pid, 2)
    sys.argv = ["prog", "-s", "logconsole=true",
                "-np", "-v", "-C", "./test/config/empty.yml"]
    sys.argv = ["prog", "-np"]
    pid = drove.script.cli()
    os.kill(pid, 2)


@raises(ValueError)
@with_setup(teardown=_teardown)
def test_script_bad_key():
    """Testing script: invalid set key"""
    sys.exit = lambda x: None
    sys.argv = ["prog", "-np", "-s", "key"]
    pid = drove.script.cli()
    os.kill(pid, 2)
