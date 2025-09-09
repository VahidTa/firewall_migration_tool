Firewall Migration Tool (fwmig)
###############################

fwmig tool helps you to migrate from one existing firewall to another one with simple copy/past steps.

- It supports most well-known vendors.
- This tool is based on Flask and JS to provide Web UI for conversion of firewall objects and policies.
- There is no online dependencies after you run the app.
- Dockerfile is available for container implementaions.
- Logging for troubleshoot is implemented.
- Tested on python 3.9, 3.10, 3.11, 3.12, 3.13

|

Supported Matrix table:

================  ======  ==========  ==========  ===========  ===========
Source Vendor                  Destination Vendor
----------------  --------------------------------------------------------
 ..                SRX     Fortigate   Cisco ASA   Checkpoint   Palo Alto
================  ======  ==========  ==========  ===========  ===========
**SRX**           N/A         Yes         Yes         Yes          Yes
----------------  ------  ----------  ----------  -----------  -----------
**Fortigate**      No         N/A          No          No          No
----------------  ------  ----------  ----------  -----------  -----------
**Cisco ASA**      No         No         N/A          No          No
----------------  ------  ----------  ----------  -----------  -----------
**Checkpoint**      Yes       Yes        Yes           N/A        Yes
----------------  ------  ----------  ----------  -----------  -----------
**Palo Alto**        Yes        Yes         Yes          Yes        N/A
================  ======  ==========  ==========  ===========  ===========

|

Any predefined services that are not included in fwmig or are not defined on the destination vendor (e.g., Palo Alto) will remain the same as on the source platform. For example, if there is an object called ``junos-who`` that this tool cannot convert, you will find an ``Error`` in the description of the policy it uses.

|

.. warning::
   This tool **does not** support Zone, Interfaces, and NAT conversion yet. Please note that you **must** create interfaces and Zones before using policy output.

Getting Start:
==============
.. toctree::
   :maxdepth: 2

   installation
   srx
   palo
   chpoint
   final


Feedback
********

Please share your experience with me about Firewall Migration Tool through `@tavajjohi <https://twitter.com/tavajjohi>`_ on twitter.