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
    drove.script.CliScript()()
    sys.argv = ["prog", "-v", "-C", "./test/config/empty.yml"]
    drove.script.CliScript()()
    os.path.dirname = lambda x: ""
    sys.argv = ["prog"]
    drove.script.CliScript()()


@raises(ValueError)
@with_setup(teardown=_teardown)
def test_script_env_failed():
    """Testing script: set wrong flag"""
    sys.exit = lambda x: None
    sys.argv = ["prog", "-v", "-s", "invalid"]
    drove.script.CliScript()()


class _MockLog(object):
    def error(self, *args, **kwargs):
        pass


class _MockPlugins(object):
    def stop_all(self, *args, **kwargs):
        pass

    def start_all(self, *args, **kwargs):
        pass


@with_setup(teardown=_teardown)
def test_script_env_success():
    """Testing script: set fine flag"""
    sys.exit = lambda x: None
    sys.argv = ["prog", "-v", "-s", "valid=true"]
    sys.path.insert(0, "./importer")
    x = drove.script.CliScript()
    x.log = _MockLog()
    x.plugins = _MockPlugins()
    x._exit_handler()
