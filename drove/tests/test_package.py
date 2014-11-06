#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
import sys
import unittest
from six import BytesIO
from six.moves import urllib
from base64 import b64decode

import drove.package
from drove.util import temp
from drove.package import Package, PackageError


# base64 encoded tar.gz for tests.

_test_package_bad = """
H4sIAOYnUVQAA+3U32qDMBiHYY+9ioyeDaxfNNFR6G5FbE27jDU6jbLu6hcLg7o/uDHrKPweD8RY
iPL61arGRsEmLwK+pNC7CHJSKfszTyWdn995PBLuIClF4pG7iLnH5GUeZ6htbF4z5uWPhc5fv//d
2P0rZQf9q6d2r83Un8Gv+iex6x+nUYL+c/iyf5Zpo22WLavjFHv0gRMhftZf9vOfUJR6jKbYfAz6
f+7vLidKfzLWnxP/0F9SROg/h8UNC9umDjcuuzIdq472oTT+ggW3AduWhTb7FWvtLrjrV9x6pw+r
nTLb9WnR9//7BeBPhvNfq+dW1+qgjG2W9sVOs8fo/z8/m38h+/lPSWD+51DUZafu14Q5BgAAAAAA
AAAAAAAAALh+b+OT9yAAKAAA
"""

_test_package_empty = """
H4sIAIY1UVQAA+3OMQqDQBCF4TnKXkAzs5thz7OgRQIBiZsinl4tBBGClan+7xWvmCle7ccam/41
1G9jrd7kArrI7mtbdt33Rizel6To2UQtacoS/IoxR5+xlncIUp7do0y//87uAAAAAAAAAAAAAAAA
AAD80QwnI0dmACgAAA==
"""

_test_package_none = """
H4sIADw2UVQAA+3OMQoCMRAF0BwlR8i4MXuegBYKC6Jroad3FQQbsVqr937xi5ni76fTfEvrKotW
67Nj3JbPfkuxqUuGobQxlYgaLeWy8q6X62Xu55xTP+4O/f7979cdAAAAAAAAAAAA/ugBC0Tm2gAo
AAA=
"""

_test_package_okay = """
H4sIAAU4UVQAA+3WwWqDMBwGcM8+RUYv28CaWKOj0B32BHsDsZp26droNMrc0y8pbHSlxR6so/D9
PASTQJQv/6gWtQ684j3tPDalvnMN1Ig5ty2LOT1sfzgsCM1FOQ8jh7IgMg3hV3maI02t04oQJ93k
Mv06P69v/Ebpv/mX22Yt1cDb4PL8Z7M4Zib/kIUc+Y/hdP5JIpXUSTItuwHWsAFHYXhZ/XNb/1Fg
phM6wNq9kP+J/O39MNlbffkzM/Zb/zNzTjDzFWDIfwyTO+I3deUvTepCtaTs9Fuh3AnxHj2SFblU
6zlp9Mp7sj2mv5W7+UqobLHvdF0326Z1TV7S/HW/d+6L5UZk+mHuEqM0Y+5/vyOcd1T/lfhoZCV2
Qul6qj/1IGv0nv+MHfz/2fqPWID6H0VeFa14XlAUKQAAAAAAAAAAAAAAAMDt+wbfsVP0ACgAAA==
"""

_test_package_failure = """
H4sIAN1VWVQAA+2XTU+EMBCGOfMrarysJsu2QKnZRA+aePZg4pHUpWiVBaRl4/rrnW78CnHDJosY
4zyHQmeAQt6ZYWqVseHUwphPWUBn3g9AAcG5OzLB6dfjOx4L4zAJqYhC4VEW0Yh5hP/Ey3RpjZUN
IZ58yLR82X5dn/+PYjv610V7p8thw2BX/eMwioRgoH/swgD1H4Et+qepLrVN06Be77+GEziJ4x30
p5zzBPRPoBh4hO6/dD+o/3f6V49yPYj2jj79Gfg+8j+COsF4Ekeo/xgcHpBZa5rZLYiuyhWp1/a+
Kv1DMj2ekkWV6fJuTloIjhNnAftKL+e5KhenG6Pv+4tCGkPOZXa1CZ1JdfugFvZo7hOgBp//29+I
bKeb/416anWjlqq0JrDPdog1eus/Y5/1P3b5n0ADiPk/BllTrdTZKcUk/Z9089+dmYF3gbvv/3go
wk3/zwTu/0bhe/3dmOZSFyoboAvsq/8gfEd/QbH/H4e9+z+9rKvGkha2iy5qPhrCa5jcaHt/CVE0
efcGznohjXprDzOVk02smWqpJkYV+ZvD4aYBPEo19rpp1eRSFnAj/qgQBEEQBEEQBEEQBEEQBEF2
4hXkTHqrACgAAA==
"""

_test_package_duplicate = """
H4sIAFtLW1QAA+3W0WqDMBgFYK99iozebAOriUkcwm7GHmBvIFZtl+JUaix0T78odIxiLaOSbnC+
G+FPQOVEPLpoNfPyrilVlurCo8vAd2YWGJEQ/ZVGIvh5PXIo40xKLjg1cxpKs52IuR9kTNfqdEeI
k25zlX6e33dp/Z/SI/k3ZbdR1XzH4Ff5h9zkL6ikyN+GifyTRFVKJ8myOVx3jz5gyfnF/DkLhBDS
5B8xETokmOcVpyH/c/l/D689AJfyp4KdfP9mFflbsbgjftfu/JUJvKj2pDno97pyF8R79EhW56ra
xKTTa++pn5j5Xn3E66LKnoeh67pZmbYteT0elrfh8NzXq22R6YfYJUZjdri3flMYc/r9s1v3P86G
/idD/P9tGMv/pv1PUPQ/iybyt97/hvwDiv5n0UT+9vqfWTvJn0cR8rdhrv73kuZofgAAAAAAAAAA
AAB/yBeNo8qQACgAAA==
"""


class TestPackage(unittest.TestCase):
    def setUp(self):
        if not hasattr(BytesIO, "__exit__"):
            BytesIO.__exit__ = lambda *a, **k: None
        if not hasattr(BytesIO, "__enter__"):
            BytesIO.__enter__ = lambda self, *a, **k: self

    def test_package_okay(self):
        with temp.directory() as dir:
            p = Package.from_tarballfd(
                BytesIO(b64decode(_test_package_okay)), [dir], True
            )

            # Try to reinstall without upgrade
            with self.assertRaises(PackageError):
                Package.from_tarballfd(
                    BytesIO(b64decode(_test_package_okay)), [dir]
                )

            o = Package.from_installed("test2", "okay", [dir])
            assert o.name == p.name

            p.remove()

    def test_package_error(self, pkg=_test_package_none):
        with temp.directory() as dir:
            with self.assertRaises(PackageError):
                Package.from_tarballfd(
                    BytesIO(b64decode(pkg)), [dir]
                )

    def test_package_empty(self):
        self.test_package_error(_test_package_empty)

    def test_package_failure(self):
        self.test_package_error(_test_package_failure)

    def test_package_duplicate(self):
        self.test_package_error(_test_package_duplicate)

    def test_package_bad(self):
        with temp.directory() as dir:
            open(os.path.join(dir, "test2"), 'w').close()
            with self.assertRaises(PackageError):
                Package.from_tarballfd(
                    BytesIO(b64decode(_test_package_okay)), [dir]
                )

    def test_package_nopip(self):
        sys.modules["pip"] = os
        self.test_package_error(_test_package_okay)
        del sys.modules["pip"]

    def test_package_tarball(self):
        self._mock_flag = False
        self._mock_orig = drove.package.__builtins__["open"]

        # Weird hack to mock __builtins__ function to be compatible
        # between py27 and py3
        def _mock_open(*a, **kw):
            if not self._mock_flag:
                self._mock_flag = True
                return BytesIO(
                    b64decode(_test_package_okay)
                )
            else:
                return self._mock_orig(*a, **kw)

        with temp.directory() as dir:
            drove.package.__builtins__["open"] = _mock_open
            try:
                Package.from_tarball("mocked", [dir])
            finally:
                drove.package.__builtins__["open"] = self._mock_orig

    def test_package_url(self):
        with temp.directory() as dir:
            _urlopen = urllib.request.urlopen
            urllib.request.urlopen = lambda *a, **kw: \
                BytesIO(b64decode(_test_package_okay))
            try:
                Package.from_url("http://none", [dir])
            finally:
                urllib.request.urlopen = _urlopen
