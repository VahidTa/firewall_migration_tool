Installation
############

Here are two option for using firewall migration tool:

Bash
****

- Make a clone from the fwmig: ``git clone https://github.com/VahidTa/firewall_migration_tool.git``
- go into the directory: ``cd firewall_migration_tool``
- Create a virtual env: ``python3.13 -m venv .venv``
- Activate the virtual env: ``source .venv/bin/activate``
- Use ``pip install -r requirements.txt`` to install required packages
- Start the app using ``python app.py``
- Connect to ``http://localhost:5000`` on browser.

Container
*********

- Make a clone from the fwmig: ``git clone https://github.com/VahidTa/firewall_migration_tool.git``
- To build and run container using Docker:

.. code-block:: bash
    :linenos:

    docker build -t fwmig:latest
    docker run -p 8080:5000 --name=fwmig -d -v $(pwd)/logs:/code/logs/ -ti fwmig:latest

- To build and run container using Podman:

.. code-block:: bash
    :linenos:

    podman build -t fwmig:latest
    podman run -p 8080:5000 --name=fwmig -d -v $(pwd)/logs:/code/logs/ -ti fwmig:latest

- Connect to ``http://127.0.0.1:8080`` on browser.