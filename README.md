# Firewall Migration Tool

The Fwmig tool helps you migrate from one firewall to another using simple copy-and-paste steps.

- Multi-Vendor Support: Compatible with most major firewall vendors.
- Web-Based Interface: Built with Flask and JavaScript, it provides an intuitive web UI to convert firewall objects and policies.
- Offline Operation: The application runs self-contained without requiring an internet connection once started.
- Container-Ready: Includes a Dockerfile for straightforward deployment in containerized environments.
- Built-in Logging: Implements comprehensive logging to simplify troubleshooting.
- Python Compatibility: Fully tested and compatible with Python versions 3.9, 3.10, 3.11, 3.12, and 3.13.

----
## Run the code:

Clone the repository:

```sh
git clone https://github.com/VahidTa/firewall_migration_tool.git
cd firewall_migration_tool
```
For running locally, create a virtual environment and install dependencies:

```sh
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
For Docker:

```sh
docker build -t fwmig .
docker run -p 8080:5000 --name=fwmig -d -v $(pwd)/logs:/code/logs/ -ti fwmig:latest
```

For Podman:

```sh
podman build -t fwmig .
podman run -p 8080:5000 --name=fwmig -d -v $(pwd)/logs:/code/logs/ -ti fwmig:latest
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

Please share your experience with me about Firewall Migration Tool through [@tavajjohi](https://x.com/tavajjohi) on X (formerly Twitter).
