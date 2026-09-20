Firewall Migration Tool (fwmig)
###############################

The Fwmig tool helps you migrate from one firewall to another using simple copy-and-paste steps.

- Multi-Vendor Support: Compatible with most major firewall vendors.
- Web-Based Interface: Built with Flask and JavaScript, it provides an intuitive web UI to convert firewall objects and policies.
- Offline Operation: The application runs self-contained without requiring an internet connection once started.
- Container-Ready: Includes a Dockerfile for straightforward deployment in containerized environments.
- Built-in Logging: Implements comprehensive logging to simplify troubleshooting.
- Python Compatibility: Fully tested and compatible with Python versions 3.10, 3.11, 3.12, and 3.13.

|

Supported Matrix:
=================

================  ===========  ==========  ==========  ===========  ===========
Source Vendor                  Destination Vendor
----------------  -------------------------------------------------------------
 ..               Juniper SRX  Fortigate   Cisco ASA   Checkpoint   Palo Alto
================  ===========  ==========  ==========  ===========  ===========
**Juniper SRX**   N/A          Yes         Yes         Yes          Yes
----------------  -----------  ----------  ----------  -----------  -----------
**Fortigate**     Yes          N/A         Yes         No           Yes
----------------  -----------  ----------  ----------  -----------  -----------
**Cisco ASA**     No           No          N/A         No           No
----------------  -----------  ----------  ----------  -----------  -----------
**Checkpoint**    Yes          Yes         Yes         N/A          Yes
----------------  -----------  ----------  ----------  -----------  -----------
**Palo Alto**     Yes          Yes         Yes         Yes          N/A
================  ===========  ==========  ==========  ===========  ===========

|

Any predefined services that are not included in fwmig or are not defined on the destination vendor (e.g., Palo Alto) will remain the same as on the source platform. For example, if there is an object called ``junos-who`` that this tool cannot convert, you will find an ``Error`` in the description of the policy it uses.

|

.. warning::
   This tool **does not** support Zone, Interface, and NAT conversions yet. Please note that you **must** create interfaces and zones before using policy output.

Getting Started
===============

.. toctree::
   :maxdepth: 2

   installation
   srx
   forti
   palo
   chpoint
   final


Feedback
********

Please share your experience with me about Firewall Migration Tool through `@tavajjohi <https://x.com/tavajjohi>`_ on X (formerly Twitter).
