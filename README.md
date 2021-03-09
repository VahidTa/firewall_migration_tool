# Firewall Migration Tool
It supports:
  - SRX -> Fortigate (policy, objects)
  - SRX -> ASA (global policy, objects)
  - SRX -> Palo Alto (policy, objects)
  - SRX -> Check Point (policy, objects)
  - Check Point -> Fortigate (policy, address objects)
  - Check Point -> Palo Alto (policy, address objects)
  - Check Point -> ASA (global policy, address objects)
  - Check Point -> SRX (global policy, address objects)

python 3.8 and later.

## ⚠️Warning:
  This tool **does not** support Zone, Interfaces, and NAT conversion yet. Please note that you must create interfaces and Zones before using policy output.

## Instruction

This Tool is based on Flask and JS to provide Web UI for conversion of firewall objects and policies.


### __SRX__
  This tool is tested on Junos 12.x , 15.x , 18.x .
  It uses XML format to convert configs and policies.
  Policies can not be extracted from SRX configuration output, because it does not provide **rule order** . So, from `show security policies` it can find out rule/policy orders.


Here are steps to provide correct output file from SRX:

- __Policy__:
  1. Login to SRX and execute `show security policies | display xml`
  2. Copy the output into file.
    1. Make sure only XML output is in the file.
- __General Config__:
  1. Login to SRX and execute `show configuration | display xml`
  2. Copy the output into file.
    1. Make sure only XML output is in the file.

Notes:
- __Fortigate__:
  - Because of the platform limitations, Policy names will be support upto 35 charachter. So, if there is a policy name with more than 35 charachter length will be convert to only first 35 characters.

- __Palo Alto__:
  - May not allow more than 30 inputs in one copy/paste. So partition the output in clipboard.
  - Applications are pre-defined as `any`. So, if you need to change it you must edit the output.
- __Check Point__:
  * From release R80 and later supports.
  * API must be enabled. Please refer to Checkpoint documentation. 
  * Use below instructions:
    * For objects, ssh to device and go to expert mode:
        * Network and Service Objects will force to replace if there is existing object with the same name.
        * use `mgmt_cli add host --batch network_objects_host.csv` for host objects.
        * use `mgmt_cli add network --batch network_objects_network.csv` for network with subnets.
        * use `mgmt_cli add group --batch network_groups.csv` for object group objects.
        * use `mgmt_cli set group --batch network_group_members.csv` for object group members.
        * use `mgmt_cli add service-group --batch service_groups.csv` for service group members.
        * use `mgmt_cli set service-group --batch service_groups_members.csv` for service group members.
  
    * For Policies:
        * Set `username` and `password` inside the policies.txt.
        * SSH to decvice and go to expert mode. Then paste output policy.
        * This method using `sid` for authentication.
        * Because of the platform, you must paste rules by grouping 3 or 4 rules for each copy.
        * Please note that about per 100 lines there is a `publish` action.

Any predefined services are not included in Firewall Migration Tool, or not defined on destionation vendor (e.g. Palo Alto), will be same as SRX platform. For example, `junos-who` may will be the same on output of conversion. If there is `junos` object that this tool can't convert it, you can find `Error` on description of policy that it uses.

### __Check Point__
  This tool is tested on SmartConsle __csv__  policy and address object exporting format.
  Because of insufficient information on csv output, Service part does not have protocol part to understand wheter it is TCP/UDP and etc.

  Here are steps to provide correct output file from Check Point:
  - __Policy__:
  1. Login to SmartConsole, go to `Security Policies`.
  2. Click on actions and select export.

  - __Objects__:
  1. Login to SmartConsole, on the right panel find 3 dots on toolbar and click.
  2. Select Address section from left selection part
  3. Click actions and select export.

## Troubleshoot
* Check file content before upload it for conversion.
* SRX content must be pure XML with no extra lines and Checkpoint must be CSV formatted.

## Feedback
Please share your experience with me about Firewall Migration Tool through [@tavajjohi](https://twitter.com/tavajjohi "twitter") on twitter.