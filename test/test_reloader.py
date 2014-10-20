#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import drove.timer
import drove.reloader
from nose.tools import raises
from nose.tools import with_setup


class MockObject(object):
    def reload(self):
        pass


def test_reloader():
    """Testing Reloader: basic behaviour"""
    x = drove.reloader.Reloader([MockObject()])
    x.reload()


_Timer = drove.reloader.Timer
def _teardown():
    drove.timer.Timer = _Timer


@with_setup(teardown=_teardown)
def test_reloader_start():
    """Testing Reloader: start()"""
    x = drove.reloader.Reloader([MockObject()])
    x.start()
