# Firewall Migration Tool

fwmig tool helps you to migrate from one existing firewall to another one with simple copy/past steps.

- It supports most well-known vendors.
- This Tool is based on Flask and JS to provide Web UI for conversion of firewall objects and policies.
- There is no online dependencies after you run the app.
- Dockerfile is available for container implementaions.
- Logging for troubleshoot is implemented.
- Tested on python 3.8 and 3.9
- Supported Matrix is table below:

<table>
    <tr>
        <td>Source Vendor</td>
        <td colspan="6">Destination Vendor</td>
    </tr>
    <tr>
        <td></td>
        <td>Juniper SRX</td>
        <td>Fortigate</td>
        <td>Cisco ASA</td>
        <td>Checkpoint</td>
        <td>Palo Alto</td>
    </tr>
    <tr>
        <td>Juniper SRX</td>
        <td>N/A</td>
        <td>X</td>
        <td>X</td>
        <td>X</td>
        <td>X</td>
    </tr>
    <tr>
        <td>Fortigate</td>
        <td></td>
        <td>N/A</td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>Cisco ASA</td>
        <td></td>
        <td></td>
        <td>N/A</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td>Checkpoint</td>
        <td>X</td>
        <td>X</td>
        <td>X</td>
        <td>N/A</td>
        <td>X</td>
    </tr>
    <tr>
        <td>Palo Alto</td>
        <td>X</td>
        <td>X</td>
        <td>X</td>
        <td>X</td>
        <td>N/A</td>
    </tr>
</table>



![fwmig](https://github.com/VahidTa/firewall_migration_tool/blob/main/docs/image/main.png?raw=true)

# Documentation

Firewall Migration Tool (fwmig) documentation lives at [fwmig.readthedocs.io](https://fwmig.readthedocs.io/en/latest/?)


# Feedback

Please share your experience with me about Firewall Migration Tool through [@tavajjohi](https://twitter.com/tavajjohi) on twitter.
