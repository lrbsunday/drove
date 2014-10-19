drove
=====

.. image:: https://travis-ci.org/droveio/drove.svg?branch=master
    :target: https://travis-ci.org/droveio/drove
    :alt: Build

.. image:: https://pypip.in/download/drove/badge.svg
    :target: https://pypi.python.org/pypi//drove/
    :alt: Downloads

.. image:: https://pypip.in/v/drove/badge.png
    :target: https://pypi.python.org/pypi/drove/
    :alt: Latest PyPI version

.. image:: https://coveralls.io/repos/droveio/drove/badge.png?branch=master
    :target: https://coveralls.io/r/droveio/drove?branch=master


**drove** is a modern monitoring tool which support alerting
(with escalation), auto-register nodes, statistics gathering
and much more in a few lines of python code.

Installation
------------

The stable releases of drove will be uploaded to
`PyPi <https://pypi.python.org/pypi>`_, so you can install
and upgrade versions using `pip <https://pypi.python.org/pypi/pip>`_::

    pip install drove

You can use unstable versions at your risk using pip as well::

   pip install -e git://github.com/ajdiaz/drove

By the way: **drove** works better with python3, but 2.7 is also
supported.

Usage
-----

You need to configure **drove** to enable the features that you
like to use. In fact **drove** act as a producer-consumer daemon,
which means that there are read *plugins* and write
*plugins*.

- A **reader** read a metric or an event from somewhere and
  report it to **drove** (in a internal cache).

- A **consumer** write a metric (taken from the internal cache)
  in somewhere.

Some *plugins* can act as reader and writer at the same time.

By default **drove** start with a very basic readers configured.

To start the daemon just type::

    drove -c myconfig.conf

You can avoid to daemonize with ``--no-daemon`` option in the
command line.

Development
-----------

**drove** is under heavy development. If you want to contribute,
please us the usual github worflow:

1. Clone the repo
2. Hack!
3. Make a pull-request
4. Merged!

If you don't have programming skills, just open a
`issue <https://github.com/ajdiaz/drove/issues>`_ in the
Github project.


