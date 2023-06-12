# Firewall Migration Tool

fwmig tool helps you to migrate from one existing firewall to another one with simple copy/past steps.

- It supports most well-known vendors.
- This Tool is based on Flask and JS to provide Web UI for conversion of firewall objects and policies.
- There is no online dependencies after you run the app.
- Dockerfile is available for container implementaions.
- Logging for troubleshoot is implemented.
- Tested on python 3.8 and 3.9, and 3.10

----
## Run the code:

```sh
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Or use Docker:

```sh
docker build -t fwmig .
docker run -p 8080:5000 --name=fwmig -d -v $(pwd)/logs:/code/logs/ -ti fwmig:latest
```

-----

## Supported Matrix:

<table>
    <tr>
        <td><strong>Source Vendor</strong></td>
        <td colspan="6"><strong>Destination Vendor</strong></td>
    </tr>
    <tr>
        <td></td>
        <td><strong>Juniper SRX</strong></td>
        <td><strong>Fortigate</strong></td>
        <td><strong>Cisco ASA</strong></td>
        <td><strong>Checkpoint</strong></td>
        <td><strong>Palo Alto</strong></td>
    </tr>
    <tr>
        <td><strong>Juniper SRX</strong></td>
        <td>N/A</td>
        <td>Yes</td>
        <td>Yes</td>
        <td>Yes</td>
        <td>Yes</td>
    </tr>
    <tr>
        <td><strong>Fortigate</strong></td>
        <td>No</td>
        <td>N/A</td>
        <td>No</td>
        <td>No</td>
        <td>No</td>
    </tr>
    <tr>
        <td><strong>Cisco ASA</strong></td>
        <td>No</td>
        <td>No</td>
        <td>N/A</td>
        <td>No</td>
        <td>No</td>
    </tr>
    <tr>
        <td><strong>Checkpoint</strong></td>
        <td>Yes</td>
        <td>Yes</td>
        <td>Yes</td>
        <td>N/A</td>
        <td>Yes</td>
    </tr>
    <tr>
        <td><strong>Palo Alto</strong></td>
        <td>Yes</td>
        <td>Yes</td>
        <td>Yes</td>
        <td>Yes</td>
        <td>N/A</td>
    </tr>
</table>

</br>

![fwmig](https://github.com/VahidTa/firewall_migration_tool/blob/main/docs/image/main.png?raw=true)

# Documentation

Firewall Migration Tool (fwmig) documentation lives at [fwmig.readthedocs.io](https://fwmig.readthedocs.io/en/latest/?)


# Feedback

Please share your experience with me about Firewall Migration Tool through [@tavajjohi](https://twitter.com/tavajjohi) on twitter.
