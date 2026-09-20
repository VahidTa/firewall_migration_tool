Installation
############

Here are two options for running the Firewall Migration Tool:

Local Environment
*****************

- Clone the repository: ``git clone https://github.com/VahidTa/firewall_migration_tool.git``
- Navigate into the directory: ``cd firewall_migration_tool``
- Create a virtual environment: ``python3.13 -m venv .venv``
- Activate the virtual environment: ``source .venv/bin/activate``
- Install dependencies: ``pip install -r requirements.txt``
- Start the application: ``python app.py``
- Open ``http://localhost:8008`` in your browser.

Containers
**********

- Clone the repository: ``git clone https://github.com/VahidTa/firewall_migration_tool.git``
- To build and run the container using Docker:

.. code-block:: bash
    :linenos:

    docker build -t fwmig:latest .
    docker run -p 8080:8008 --name=fwmig -d -v $(pwd)/logs:/code/logs/ -ti fwmig:latest

- To build and run the container using Podman:

.. code-block:: bash
    :linenos:

    podman build -t fwmig:latest .
    podman run -p 8080:8008 --name=fwmig -d -v $(pwd)/logs:/code/logs/ -ti fwmig:latest

- Open ``http://127.0.0.1:8080`` in your browser.
