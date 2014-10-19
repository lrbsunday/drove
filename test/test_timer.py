#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import time
import drove.timer
from drove.timer import Timer
from nose.tools import raises


def _mock_sleep(value):
    if value != 1000:
        raise ValueError(value)


def _testing_fn(argument, d):
    d["value"] = argument


def test_timer_stop():
    """Testing Timer: stop"""
    x = Timer(0.2, lambda: None)
    x.run()
    x.stop()
    x.wait(1, 0)


def test_timer():
    """Testing Timer: basic behaviour"""
    d = {}
    x = Timer(0.1, _testing_fn, "test", d)
    x.run()
    time.sleep(0.5)
    assert d["value"] == "test"
    x.stop()


def _testing_fn_raise():
    raise ValueError


def test_not_runnin():
    """Testing Timer: not running thread"""
    x = Timer(0.1, lambda: None)
    x.running = True
    x.stop()
    x._run()


@raises(ValueError)
def test_timer_except():
    """Testing Timer: internal run"""
    x = Timer(0.1, _testing_fn_raise)
    x.running = True
    x._run()


def test_timer_sleep():
    """Testing Timer: internal sleep"""
    x = Timer(0.1, lambda: None)
    x.running = True
    x.run()
    x.stop()
    Timer.wait(1, seconds=0.1)
