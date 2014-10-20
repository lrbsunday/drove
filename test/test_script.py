#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
import sys
import drove.script
import drove.plugin
from nose.tools import with_setup
from nose.tools import raises


_exit = sys.exit
_args = sys.argv
_loop = drove.plugin.PluginManager.loop


def _teardown():
    sys.exit = _exit
    sys.argv = _args
    drove.plugin.PluginManager.loop = _loop


def _mock_loop(*args, **kwargs):
    raise ValueError()


@with_setup(teardown=_teardown)
def test_script():
    """Testing script: basic behaviour"""
    sys.exit = lambda x: None
    sys.argv = ["prog", "-h"]
    pid = drove.script.cli()
    os.kill(pid, 2)
    os.kill(pid, 9)
    sys.argv = ["prog", "-s", "logconsole=true",
                "-np", "-v", "-C", "./test/config/empty.yml"]
    pid = drove.script.cli()
    os.kill(pid, 9)
    sys.argv = ["prog", "-np"]
    pid = drove.script.cli()
    os.kill(pid, 9)


@raises(ValueError)
@with_setup(teardown=_teardown)
def test_script_loop():
    """Testing script: loop()"""
    sys.argv = ["prog", "-f", "-v"]
    drove.plugin.PluginManager.loop = _mock_loop
    drove.script.cli()


def _fail(*args, **kwargs):
    raise ValueError()


@raises(ValueError)
@with_setup(teardown=_teardown)
def test_script_bad_key():
    """Testing script: invalid set key"""
    sys.exit = _fail
    sys.argv = ["prog", "-np", "-s", "key"]
    pid = drove.script.cli()
    os.kill(pid, 9)
