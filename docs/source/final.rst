After Conversion
################

After successfully converting your source configuration, follow the instructions below for your selected destination vendor:


Cisco ASA
*********

Cisco ASA policy conversion currently applies to global access lists.

- Log in to the device.
- Enter global configuration mode (``configure terminal``).
- You must copy/paste configuration first and then the policy.
- Each generated ``.txt`` file contains the respective configuration section.


Check Point
***********

* Supports Check Point R80 and later releases.
* The Management API must be enabled (refer to Check Point documentation).
* Network and service objects will overwrite existing objects with the same name (via ``set-if-exists``).
* For objects, log in to the device and enter expert mode.
* Run the batch commands in the following order:

    .. code-block:: bash
        :linenos:

        mgmt_cli add host --batch network_objects_host.csv                 # Host objects
        mgmt_cli add network --batch network_objects_network.csv           # Network with subnets
        mgmt_cli add group --batch network_groups.csv                      # Object groups
        mgmt_cli set group --batch network_group_members.csv               # Object group members
        mgmt_cli add service-group --batch service_groups.csv              # Service groups
        mgmt_cli set service-group --batch service_groups_members.csv      # Service group members

* For policies:
    * Set your ``username`` and ``password`` inside ``policies.txt``.
    * Log in to the device, enter expert mode, and paste the generated policy commands.
    * This script uses a session ID (``sid``) for API authentication.
    * Due to CLI limitations, paste rules in batches of 3 to 4 at a time.
    * A ``publish`` command is automatically included approximately every 100 lines.


FortiGate
*********

Due to FortiOS limitations, policy names support a maximum of 35 characters. Any policy name exceeding 35 characters is automatically truncated to the first 35 characters.

* Log in to the device.
* You must copy/paste configuration first and then the policy.


Palo Alto
*********

The PAN-OS CLI may not accept more than 30 commands per paste; partition the output into smaller batches from your clipboard.

* Log in to the device.
* Enter configuration mode (``configure``).
* You must copy/paste configuration first and then the policy.
* Commit the configuration at the end (``commit``).


Juniper SRX
***********

For SRX, the generated output consists of Junos ``set`` commands.

* Log in to the device.
* Enter configuration mode (``configure``).
* You must copy/paste configuration first and then the policy.
* Commit the configuration at the end (``commit``).
