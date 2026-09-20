FortiGate Conversion
####################

fwmig uses the YAML format to convert configurations and policies.

Features
========
- Address Objects

  - Subnet
  - IP Range
  - FQDN

- Address Groups
- Custom Services

  - TCP / UDP (with source and destination ports)
  - ICMP
  - IP Protocol

- Service Groups
- Policies

|

File-based Conversion
*********************

If you want to convert FortiGate configurations and policies, select ``file``
under ``Type of conversion`` and export your configuration as YAML. Follow the steps below:

FortiGate Configuration Export
==============================

- Log in to your FortiGate device (via GUI or CLI).
- Export the configuration in YAML format.
- Supported file extensions are ``.yaml`` and ``.yml``.

YAML Format
===========

Policy field reference:

- ``srcintf`` / ``dstintf``: Interface names (used as zones)
- ``srcaddr`` / ``dstaddr``: List of address names, or the string ``any``
- ``service``: List of service names, or the string ``any``
- ``action``: ``accept`` or ``deny``
- ``status``: ``enable`` or ``disable`` (default: ``enable``)
- ``logtraffic``: ``enable`` or ``disable``

Using Conversion
================

After preparing your YAML file, upload it through the web UI. For policy
conversion, choose ``policy`` under ``Action`` and upload the YAML file.
For address objects, services, and groups, choose ``other configs``.


Final Step
**********

Go to `After conversion <final.html>`_.
