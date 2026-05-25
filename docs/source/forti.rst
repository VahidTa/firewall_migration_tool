Fortigate conversion
####################

It uses YAML format to convert configs and policies.

Features
========
- Address objects

  - Subnet
  - IP Range
  - FQDN

- Address Groups
- Custom Services

  - TCP / UDP (with source and destination ports)
  - ICMP
  - IP protocol

- Service Groups
- Policies

|

File Base
*********

If you want to convert Fortigate configs and policies, you need to select ``file``
under ``Type of conversion`` and export your config as YAML. Follow the steps below.

Fortigate config export
=======================

- Login to your Fortigate device (GUI or CLI).
- Export the configuration in YAML format.
- Supported file extension is ``.yaml`` or ``.yml``.

YAML format
===========

Policy field reference:

- ``srcintf`` / ``dstintf``: interface names (used as zones)
- ``srcaddr`` / ``dstaddr``: list of address names, or the string ``any``
- ``service``: list of service names, or the string ``any``
- ``action``: ``accept`` or ``deny``
- ``status``: ``enable`` or ``disable`` (default: ``enable``)
- ``logtraffic``: ``enable`` or ``disable``

Using conversion
================

After preparing your YAML file, upload it through the web UI. For policy
conversion choose ``policy`` under ``Action`` and upload the YAML file.
For address objects, services, and groups choose ``other configs``.


Final step
**********

Go to `After conversion <final.html>`_
