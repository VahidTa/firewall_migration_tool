Installation
############

Here are two option for using firewall migration tool:

Bash
****

- Make a clone from the `Firewall Migration Tool <https://github.com/VahidTa/firewall_migration_tool>`_ link
- Use ``pip install -r requirements.txt`` to install required packages
- Start the app using ``python3 app.py``
- Connect to ``http://localhost:5000`` on browser.

Container
*********

- Make a clone from the `Firewall Migration Tool <https://github.com/VahidTa/firewall_migration_tool>`_ link
- To build and run container use:

.. code-block:: bash
    :linenos:

    docker build -t fwmig:latest
    docker run -p 8080:5000 -d -v ./logs/:/app/logs/ -ti fwmig:latest

- Connect to ``http://container_ip:8080`` on browser.