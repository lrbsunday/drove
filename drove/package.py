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
        if not os.path.exists(dir_path):
            os.mkdir(dir_path, mode=0o755)
        elif not os.path.isdir(dir_path):
            raise PackageError("path '%s' is not a directory" % (dir_path,))
        if version is None:
            open(os.path.join(dir_path, "__init__.py"), 'a').close()
        else:
            with open(os.path.join(dir_path, "__init__.py"), 'a') as f:
                f.write("VERSION = %s\n" % (version,))
                f.write("__version__ = %s\n" % (version,))

    def install_requirements(self, path):
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
        candidates = glob.glob(os.path.join(dir, "*-*-*"))
        if len(candidates) == 0:
            raise PackageError("Package doesn't contains " +
                               "installable candidates")

        for candidate in candidates:
            if os.path.isdir(candidate):
                yield os.path.split(candidate.strip())[-1].split("-", 2)

    def is_installed(self, dir, author, plugin):
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

                dest_dir = os.path.join(dir, author, plugin)

                # create author package
                self.init_package(os.path.join(dir, author))

                # copy plugin
                shutil.copytree(local_plugin, dest_dir)
                self.init_package(dest_dir, version)
                self.install_requirements(plugin_path)
