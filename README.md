# firewall_migration_tool
It supports only SRX -> Fortigate.

Use Python 3.x

## Instruction

SRX:<br />
  It uses XML format to convert configs and policies. Reason that policies are extracted from config is in configuration output of SRX, it does not provide **rule order** . So, from "show security" you can find orders.

  Also, this tool **does not** support Zone, Interfaces, and NAT. Please note that you must create interfaces and Zones before using output of policy.

Here are steps to provide correct output file from SRX:

- __Policy__:
  1. Login to SRX and execute `show security | display xml`
  2. Copy the output into file.
    1. Make sure only XML output is in the file.
- __General Config__:
  1. Login to SRX and execute `show configuration| display xml`
  2. Copy the output into file.
    1. Make sure only XML output is in the file.

Use `$python3.8 app.py -h` to see help.

## Example
- Convert Policy: `python3 app.py --file policy.txt --action policy`

- Convert Configs: `python3 app.py --file config.txt --action config`