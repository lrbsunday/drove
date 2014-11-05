#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""This module contains definitions and classes to handle
plugin packages. A package is formerly a tarball file
which contains a plugin in the normalize plugin packaging
format.

A plugin package must contain a folder ``plugin``, with the
plugin code inside (which can be a module(s) or other
package(s).
"""

import os
import glob
import shutil
import tarfile

from .util import temp
from .util import tester


class PackageError(Exception):
    """Models an error related with a malformed package"""


class Package(object):
    def __init__(self, tarball, verbose=False):
        """Models a package which contains a plugin.

        :type tarball: str
        :param tarball: the filename of the tarball with the plugin
        :type verbose: bool
        :param verbose: if true be more verbose
        """
        self.tarball = tarball
        self.verbose = verbose

    def init_package(self, dir_path, version=None):
        """Initialize a package in specified path. This function
        create the ``__init__.py`` file or update it if exists.

        :type dir_path: str
        :param dir_path: The path to initialize as python package
        :type version: str
        :param version: The version of the package. If exists create
            ``__version__`` variable into ``__init__.py`` file.
        """
        if not os.path.exists(dir_path):
            os.mkdir(dir_path, 0o755)
        elif not os.path.isdir(dir_path):
            raise PackageError("path '%s' is not a directory" % (dir_path,))
        if version is None:
            open(os.path.join(dir_path, "__init__.py"), 'a').close()
        else:
            with open(os.path.join(dir_path, "__init__.py"), 'a') as f:
                f.write("VERSION = '%s'\n" % (version,))
                f.write("__version__ = '%s'\n" % (version,))

    def run_tests(self, path):
        """Run tests with uniitest if exists"""

        for result in tester.run_tests(path):
            if not result.wasSuccessful():
                for fail in result.failures:
                    raise PackageError("Test failure: %s" % (fail[1],))

    def install_requirements(self, path):
        """Resolve and install requirements. This function will read
        the file ``requirements.txt`` from path passed as argument, and
        then use pip to install them.
        """
        requirements = os.path.join(path, "requirements.txt")
        if os.path.exists(requirements):
            try:
                from pip import main as pip_main
            except ImportError:
                raise PackageError("This module needs python dependencies. " +
                                   "You need pip to install dependencies, " +
                                   "please install pip libraries before.")

            verbose = ["-q"] if not self.verbose else []
            pip_main(verbose + ["install", "-r", requirements])

    def get_candidates(self, dir):
        """Given a directory, find plugin candidates, which are
        folders that match the expression *author*-*plugin*-*version*.
        """
        candidates = glob.glob(os.path.join(dir, "*-*-*"))
        if len(candidates) == 0:
            raise PackageError("Package doesn't contains " +
                               "installable candidates")

        for candidate in candidates:
            if os.path.isdir(candidate):
                items = os.path.split(candidate.strip())[-1].split("-")
                yield items[0], "-".join(items[1:-1]), items[-1]

    def is_installed(self, dir, author, plugin):
        """Return true if the specified plugin of author is
        installed in directory passed as first argument.
        """
        path = os.path.join(dir, author, plugin)
        return os.path.isdir(path)

    def install(self, dir, upgrade=False):
        """Generic package installer. This method install a drove package.

        :type dir: str
        :param dir: directory to install the package

        :type upgrade: bool
        :param upgrade: if true override installed package with new one
        """
        with temp.directory() as tmp_dir:
            with tarfile.open(self.tarball, "r:gz") as tarball:
                tarball.extractall(path=tmp_dir)

            for (author, plugin, version) in self.get_candidates(tmp_dir):

                if self.is_installed(dir, author, plugin) and not upgrade:
                    raise PackageError("Package '%s.%s' already installed"
                                       % (author, plugin,))

                plugin_path = os.path.join(tmp_dir,
                                           "%s-%s-%s" % (author, plugin,
                                                         version,))
                local_plugin = os.path.join(plugin_path, "plugin")
                if not os.path.isdir(local_plugin):
                        raise PackageError("Package '%s.%s' " %
                                           (author, plugin,) +
                                           "does not contain any plugin")

                self.run_tests(plugin_path)

                dest_dir = os.path.join(dir, author, plugin)

                # create author package
                self.init_package(os.path.join(dir, author))

                # copy plugin
                shutil.copytree(local_plugin, dest_dir)
                self.init_package(dest_dir, version)
                self.install_requirements(plugin_path)
