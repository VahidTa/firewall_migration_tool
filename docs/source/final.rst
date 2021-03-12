After Conversion
################

After successfull conversion of source config, based on destination vendor you were selected you must follow related steps.

Cisco ASA
*********

Cisco ASA policy works only for global policy.

- You must copy/paste configuration first and then configuration.
- Each .txt file contains related configuration.


Checkpoint
**********

* It supports from release R80 and later.
* API must be enabled. Please refer to Checkpoint documentation. 
* Network and Service Objects will force to replace if there is existing object with the same name.
* For objects, ssh to device and go to expert mode
* Use these steps:

    .. code-block:: bash
        :linenos:
    
        mgmt_cli add host --batch network_objects_host.csv #Host objects
        mgmt_cli add network --batch network_objects_network.csv #Network with subnets
        mgmt_cli add group --batch network_groups.csv #Object group objects
        mgmt_cli set group --batch network_group_members.csv #Object group members
        mgmt_cli add service-group --batch service_groups.csv #Service group members
        mgmt_cli set service-group --batch service_groups_members.csv #Service group members

* For Policies:
    * Set ``username`` and ``password`` inside the policies.txt.
    * SSH to decvice and go to expert mode. Then paste output policy.
    * This method using `sid` for authentication.
    * Because of the platform, you must paste rules by grouping 3 or 4 rules for each copy.
    * Please note that about per 100 lines there is a ``publish`` action.


Fortigate
*********

Because of the platform limitations, Policy names will be support upto 35 charachter. So, if there is a policy name with more than 35 charachter length will be convert to only first 35 characters.


Palo Alto
*********

May not allow more than 30 inputs in one copy/paste. So partition the output in clipboard.