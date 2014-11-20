.. toctree::
  :maxdepth: 2
  :hidden:

  self
  quickstart
  installation
  usage
  plugins
  internals
  reference

.. image:: _static/drove-logo.svg
  :height: 200
  :width: 197
  :align: right

Introduction
============

**drove** is a modern monitoring tool which support alerting
(with escalation), auto-register nodes, statistics gathering
and much more in a few lines of python code.

There are a lot of features in **drove**, for example:

* Easy to extend in python and other languages
* Easy to install, only ``python>=2.7`` as dependency
* Lots of plugins in the community_
* Compatible with nagios checks using `nagios plugin`_
* Support smart alerting (escalation, collapsing, hysteresis etc.)
* Multiple backends to store metrics (influxdb, sql, redis, statsd...)
* ... and much more!



.. _community: https://plugins.drove.io
.. _`nagios plugin`: https://plugins.drove.io/plugins/droveio/nagios


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


