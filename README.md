# Firewall Migration Tool

fwmig tool helps you to migrate from one existing firewall to another one with simple copy/past steps.

- It supports most well-known vendors.
- This Tool is based on Flask and JS to provide Web UI for conversion of firewall objects and policies.
- There is no online dependencies after you run the app.
- Dockerfile is available for container implementaions.
- Logging for troubleshoot is implemented.
- Tested on python 3.8 and 3.9
- Supported Matrix is table below:

| | |    |   | Destination Vendor |  |  |
| :-----| :---------- |:-------------:| :-----:| :-------------: |:-------------:| :-----:|
| Source Vendor |  | SRX           | Fortigate  | Cisco ASA | Checkpoint | Palo Alto |
| SRX      | | N/A | X | X | X | X |
| Fortigate | |  | N/A | | | | |
| Cisco ASA | |  | | N/A | | |
| Checkpoint | | X | X | X | N/A | X | 
| Palo Alto | | X | X | X | X |N/A |

</br>
</br>


![fwmig](https://github.com/VahidTa/firewall_migration_tool/blob/main/docs/image/main.png?raw=true)

# Documentation

Firewall Migration Tool (fwmig) documentation lives at [fwmig.readthedocs.io](https://fwmig.readthedocs.io/en/latest/?)


# Feedback

Please share your experience with me about Firewall Migration Tool through [@tavajjohi](https://twitter.com/tavajjohi) on twitter.
