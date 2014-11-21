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


Philosophy
----------

We designed **drove** keeping in mind to create a monitoring tool to be easy
to adapt to new elements, with a strong community behind which provides
useful reusable plugins.

With **drove**, you can basically install the core module as any other
python software (read the :doc:`installation` manual for more information)
and then install plugins with drove itself with the command:

.. code-block:: sh

  $ drove install [plugin]

.. note::
  Actually droves has not the concept of server or daemon *per se*. It's
  agnostic about that, are the plugins which gives the role of server or
  client to a drove installation. The plugin |droveio.network|_ allows you to
  listen a port for incoming drove messages, and also the same plugin allows
  you to configure your drove installation to send message to any other drove
  installation.

  In short, the plugin |droveio.network|_ is the responsible of the
  client-server architecture, but drove core itself does nothing about that.

How it works
------------

Essentially **drove** is just a queue system which read from plugins (called
readers) some data, and write that data in other plugins (called writers).

.. image:: _static/doc-fig-1.svg
  :align: center

For example the plugin ``droveio.cpu`` read CPU data from the operating
system, then drove core store that data in internal queues. On the other
hand we've the ``droveio.influxdb`` plugin, which read data from internal
queues and save the data into InfluxDB_ database.

If you want to know more about how **drove** works internally, please read
the manual :doc:`internals`.


.. _community: https://plugins.drove.io
.. _`nagios plugin`: https://plugins.drove.io/plugins/droveio/nagios
.. _InfluxDB: http://influxdb.com


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |droveio.network| replace:: ``droveio.network``
.. _droveio.network: https://plugins.drove.io/droveio/network
.. |droveio.influxdb| replace:: ``droveio.influxdb``
.. _droveio.influxdb: https://plugins.drove.io/droveio/influxdb
