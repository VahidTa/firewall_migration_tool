# AGENTS.md

> Comprehensive developer and AI agent manual for the **Firewall Migration Tool (`fwmig`)** repository.

---

## 1. Project Overview

**Firewall Migration Tool (`fwmig`)** is an offline-capable, web-based network utility written in Python (Flask) designed to simplify migrations between enterprise firewall platforms. It ingests firewall configurations (via file upload or Juniper NETCONF) and translates security policies, network address objects, and service objects into native configuration commands or management files for destination firewalls.

- **Primary Language:** Python (tested and supported on versions `3.11`, `3.12`, `3.13`, `3.14`)
- **Web Framework:** Flask
- **Network / Transport:** `ncclient` (Junos NETCONF), `paramiko`
- **Data Processing:** `pandas`, `xmltodict`, `PyYAML`
- **Documentation:** Sphinx (`docs/`, deployed on ReadTheDocs)
- **Linter / Formatter:** Ruff (`ruff.toml`, `.pre-commit-config.yaml`)

---

## 2. Repository Directory Structure

```text
firewall_migration_tool/
├── app.py                      # Flask web application entry point & routing
├── requirements.txt            # Project dependencies
├── Dockerfile                  # Container build instructions (Python 3.13-slim, port 8008)
├── ruff.toml                   # Ruff linting and formatting configuration
├── .pre-commit-config.yaml     # Git pre-commit hooks for Ruff
├── .readthedocs.yaml           # ReadTheDocs build configuration
├── configs/                    # Temporary staging directory for uploaded or fetched configs
│   └── .keep
├── exported/                   # Output directory where converted configs are saved per vendor
│   ├── .keep
│   ├── asa/                    # Generated Cisco ASA scripts (.txt)
│   ├── chpoint/                # Generated Check Point scripts & CSV batches
│   ├── forti/                  # Generated FortiOS scripts (.txt)
│   ├── palo/                   # Generated Palo Alto scripts (.txt)
│   └── srx/                    # Generated Juniper Junos set commands (.txt)
├── logs/                       # Rotating runtime log directory
│   └── app.log                 # Log output file
├── docs/                       # Sphinx documentation source & build scripts
│   ├── Makefile / make.bat
│   └── source/
│       ├── conf.py             # Sphinx configuration
│       ├── index.rst           # Docs home & supported matrix
│       ├── installation.rst    # Installation guide
│       ├── srx.rst             # Junos XML extraction guidelines
│       ├── forti.rst           # FortiGate YAML extraction guidelines
│       ├── palo.rst            # Palo Alto XML extraction guidelines
│       ├── chpoint.rst         # Check Point CSV extraction guidelines
│       └── final.rst           # Post-conversion paste & import instructions
└── resources/                  # Core package containing domain logic and web assets
    ├── __init__.py             # Rotating file logging initialization (`app_logger`)
    ├── parser.py               # Main parsing dispatcher (`main_parser`)
    ├── ip_address_converter/
    │   └── netmask_convereter.py   # IPv4 prefix, netmask, and host helpers
    ├── protocols/
    │   └── nc_conn.py          # Juniper NETCONF client via ncclient (`NcMGR`)
    ├── dst_vendor/             # Destination generators (implementing VendorAbc)
    │   ├── __init__.py
    │   ├── data_objects.py     # Normalized intermediate dataclasses
    │   ├── vendor_abc.py       # Abstract Base Class for destination vendors
    │   ├── dst_asa.py          # Cisco ASA CLI generator
    │   ├── dst_chpoint.py      # Check Point mgmt_cli & CSV generator
    │   ├── dst_forti.py        # Fortinet FortiOS CLI generator
    │   ├── dst_palo.py         # Palo Alto PAN-OS CLI generator
    │   └── dst_srx.py          # Juniper Junos CLI generator
    ├── src_vendor/             # Source vendor parsers
    │   ├── chpoint/            # Check Point CSV parsers
    │   │   ├── chpoint_config_parser.py
    │   │   └── chpoint_policy_parser.py
    │   ├── forti/              # FortiGate YAML parsers
    │   │   ├── forti_config_converter.py
    │   │   └── forti_policy_convert.py
    │   ├── palo/               # Palo Alto XML parsers
    │   │   ├── palo_config_coverter.py   # Note: named "coverter"
    │   │   └── palo_policy_convert.py
    │   └── srx/                # Juniper Junos XML parsers
    │       ├── srx_config_converter.py
    │       └── srx_policy_convert.py
    └── web/                    # Web frontend templates and assets
        ├── static/
        │   ├── files.css       # Downloads view styling
        │   ├── script.js       # Dynamic form interaction logic
        │   └── style.css       # Main UI styling
        └── templates/
            ├── exported_vendor.html  # Directory listing of vendors
            ├── files.html            # File download list for a specific vendor
            └── home.html             # Main conversion form
```

---

## 3. Core Architecture & Data Flow

```text
                  +-----------------------------------+
                  |        Web UI or NETCONF          |
                  +-----------------------------------+
                                    |
                                    v
                          Uploaded Config File
                           (Saved to configs/)
                                    |
                                    v
                    +-------------------------------+
                    |  resources/parser.py          |
                    |  main_parser() Router         |
                    +-------------------------------+
                                    |
               +--------------------+--------------------+
               |                    |                    |
               v                    v                    v
          SrxCfg               FortiCfg             PaloCfg / ChPointCfg
   (XML -> Dataclasses) (YAML -> Dataclasses)  (XML/CSV -> Dataclasses)
               |                    |                    |
               +--------------------+--------------------+
                                    |
                                    v
                 Intermediate Normalized Dataclasses:
                 • ServiceData       • ServiceSetData
                 • AddressData       • AddressSetData
                 • PolicyData
                                    |
                                    v
                 Destination Generator (VendorAbc):
                 • FortiDst          • PaloDst
                 • SrxDst            • AsaDst
                 • ChPointDst
                                    |
                                    v
                    Generated Files in exported/<vendor>/
                 (policies.txt, addresses.txt, services.txt, etc.)
```

### 3.1 Intermediate Normalized Data Layer (`resources/dst_vendor/data_objects.py`)
All source parsers translate vendor-specific structures into normalized Python `dataclasses`:

- `ServiceData`: Custom port/protocol service (fields: `application_name`, `destination_port`, `source_port`, `application_protocol`, `application_desc`, `app_session_ttl`, `icmp_code`, `icmp_type`, `protocol_number`).
- `ServiceSetData`: Service group definition (fields: `app_set_name`, `app_set_desc`, `app_list`, `app_name`).
- `AddressData`: IP/Host/Subnet object (fields: `address_name`, `address_ip`, `address_desc`, `address_type`).
- `AddressSetData`: Address group definition (fields: `address_set_name`, `address_name_list`, `address_set_desc`, `address_name`).
- `PolicyData`: Firewall rule (fields: `policy_name`, `source_zone`, `destination_zone`, `policy_src_address`, `policy_dst_address`, `policy_app`, `policy_log`, `policy_state`, `policy_action`, `policy_id`, `position`).

### 3.2 Destination Interface (`resources/dst_vendor/vendor_abc.py`)
Destination vendors implement the `VendorAbc` abstract base class:

```python
class VendorAbc(ABC):
    @abstractmethod
    def service(self, data: ServiceData): ...
    @abstractmethod
    def service_set(self, data: ServiceSetData): ...
    @abstractmethod
    def address(self, data: AddressData): ...
    @abstractmethod
    def address_set(self, data: AddressSetData): ...
    @abstractmethod
    def policy(self, data: PolicyData): ...
```

### 3.3 Request & Execution Lifecycle
1. **Request Received:** `app.py:main` receives a `POST` request.
   - If `type == "netconf"`: `NcMGR.junos_nc_conn` executes Junos XML retrieval and writes `configs/nc_fw_result.log`.
   - If `type == "file"`: Uploaded file is validated against allowed extensions (`txt`, `log`, `csv`, `yaml`, `yml`) and saved to `configs/<secure_filename>`.
2. **Parser Invocation:** `main_parser(action, cfg, src_vendor, dst_vendor, acts)` is invoked.
3. **Execution:**
   - If `action == "policy"`: Invokes `output.policy` on the source class, translating policies into destination syntax.
   - If `action == "config"`:
     - Calls `output.cleaner` (prepares `exported/<dst_vendor>/` and purges previous non-policy files).
     - Sequentially calls `output.address`, `output.service`, and `output.service_set` based on selected checkboxes in `acts`.
     - Calls `output.delete` to remove the temporary file in `configs/`.
4. **Result / Download:** User is redirected to `/exported/<dst_vendor>/` where generated files are downloadable.

---

## 4. Vendor Support Matrix

| Source Vendor | Juniper SRX | Fortigate | Cisco ASA | Checkpoint | Palo Alto | Ingest Format |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Juniper SRX** | N/A | Yes | Yes | Yes | Yes | Junos XML (`display xml`) / NETCONF |
| **Fortigate** | Yes | N/A | Yes | No | Yes | FortiOS YAML export |
| **Cisco ASA** | No | No | N/A | No | No | *(Destination only)* |
| **Checkpoint** | Yes | Yes | Yes | N/A | Yes | SmartConsole CSV export |
| **Palo Alto** | Yes | Yes | Yes | Yes | N/A | PAN-OS XML (wrapped in `<root>`) |

> [!NOTE]
> **Check Point Source Services:** Check Point SmartConsole CSV exports lack protocol identifiers (TCP vs UDP), so service conversion from Check Point source is currently not supported and returns `"no"`.
>
> **Interfaces, Zones, & NAT:** Interface, Zone, and NAT conversions are currently unhandled. Users must ensure target zones and interfaces exist before applying generated policy commands.

---

## 5. Development Environment & Setup

### 5.1 Local Environment
Ensure Python 3.10, 3.11, 3.12, or 3.13 is installed:

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application locally
python app.py
```
The application runs on `http://0.0.0.0:8008`.

### 5.2 Containerized Run
Using Docker:
```bash
docker build -t fwmig .
docker run -p 8080:8008 --name=fwmig -d -v "$(pwd)/logs:/code/logs/" -ti fwmig:latest
```

Using Podman:
```bash
podman build -t fwmig .
podman run -p 8080:8008 --name=fwmig -d -v "$(pwd)/logs:/code/logs/" -ti fwmig:latest
```

### 5.3 Building Documentation
Documentation uses Sphinx:
```bash
# Build HTML docs using sphinx
sphinx-build -b html docs/source docs/build/html
# Or using make
make -C docs html
```

---

## 6. Coding Standards & Linter Rules

The project uses **Ruff** for linting and code formatting, governed by `ruff.toml` and `.pre-commit-config.yaml`.

### 6.1 Ruff Configuration Summary
- **Line Length:** 120
- **Excluded Paths:** `docs/`
- **Selected Rules:**
  - `E`, `W`: Pycodestyle errors and warnings
  - `F`: Pyflakes
  - `I`: isort (import sorting)
  - `UP`: pyupgrade (modern Python syntax)
  - `SIM`: flake8-simplify
  - `C4`: flake8-comprehensions
- **Ignored Rules:** `E501` (Line length handled by formatter)
- **Formatting:** `line-ending = "auto"`

### 6.2 Lint & Format Commands
Before submitting code changes, always format and lint:
```bash
ruff format .
ruff check . --fix
```

### 6.3 Code Conventions
- **Type Annotations:** Use modern Python 3.10+ union syntax (`str | int | None`, `list[str]`, `dict[str, Any]`).
- **Relative File Paths:** All file operations assume the application is executed from the repository root (`configs/`, `exported/`, `logs/app.log`). Never use absolute paths or rely on `__file__`-relative assumptions without testing.
- **Logging:**
  - Standard logger is instantiated via `resources.app_logger()`.
  - Submodules should create child loggers: `logger = logging.getLogger("fwmig.<submodule>")`.
  - Always pass `exc_info=True` when catching exceptions to preserve stack traces in `logs/app.log`.
- **Safe Cleanup:** Use `with contextlib.suppress(BaseException):` when attempting file cleanup (e.g. `os.remove(f"configs/{cfg}")`) to prevent crashes during error handling.

---

## 7. Instructions for Common AI Agent Tasks

### 7.1 Adding a New Source Vendor

1. **Create Source Modules:**
   Create a new directory under `resources/src_vendor/<new_vendor>/`. Implement two files:
   - `<new_vendor>_config_converter.py`: Implements a class with `address`, `service`, `service_set`, `cleaner`, and `delete` properties.
   - `<new_vendor>_policy_convert.py`: Implements policy extraction that instantiates `PolicyData` and passes it to the corresponding destination generator (`forti.policy(...)`, `palo.policy(...)`, etc.).
2. **Translate to Dataclasses:**
   In the parser methods, extract raw data from the input format and instantiate normalized objects from `resources.dst_vendor.data_objects`.
3. **Register in `main_parser`:**
   In `resources/parser.py`, import the new configuration converter and add an `elif src_vendor == "<new_vendor>":` branch.
4. **Update Web UI:**
   Add `<option value="<new_vendor>">...</option>` to the `src_vendor` select element in `resources/web/templates/home.html`.
5. **Update Documentation:**
   Add documentation in `docs/source/<new_vendor>.rst`, add to `docs/source/index.rst`, and update the support matrix table in `README.md` and `docs/source/index.rst`.

### 7.2 Adding a New Destination Vendor

1. **Implement `VendorAbc`:**
   Create `resources/dst_vendor/dst_<new_vendor>.py` and subclass `VendorAbc`:
   ```python
   from resources.dst_vendor.data_objects import (
       AddressData, AddressSetData, PolicyData, ServiceData, ServiceSetData
   )
   from resources.dst_vendor.vendor_abc import VendorAbc

   class NewVendorDst(VendorAbc):
       def service(self, data: ServiceData): ...
       def service_set(self, data: ServiceSetData): ...
       def address(self, data: AddressData): ...
       def address_set(self, data: AddressSetData): ...
       def policy(self, data: PolicyData): ...
   ```
2. **Handle Output Directory & Files:**
   Append generated commands into `exported/<new_vendor>/<filename>.txt`.
3. **Connect to Existing Source Parsers:**
   Import `NewVendorDst` in each source vendor's config and policy converter modules (`srx`, `forti`, `palo`, `chpoint`), add translation dictionaries if needed, and dispatch to the new destination instance when `self.vendor == "<new_vendor>"`.
4. **Update UI & Support Matrix:**
   Add the destination vendor option to `dst_vendor` in `resources/web/templates/home.html` and update `README.md` and docs.

### 7.3 Adding Unit / Integration Tests

Since the repository currently has no automated tests, when introducing tests:
- Create a `tests/` directory at the project root.
- Use `pytest`.
- Create sample input fixtures for Junos XML, FortiOS YAML, PAN-OS XML, and Check Point CSV in `tests/fixtures/`.
- Mock file writing or use `tmp_path` fixtures to verify that `main_parser` outputs valid command strings.
- Add `pytest` to development dependencies.

---

## 8. Critical Codebase Quirks & Pitfalls for Agents

- **Spelling in Filenames:**
  - Note that `resources/src_vendor/palo/palo_config_coverter.py` is named `palo_config_coverter.py` (missing the 'n' in "converter"). Do not accidentally alter the import path without renaming the file and updating all references.
  - Similarly, `resources/ip_address_converter/netmask_convereter.py` is spelled `netmask_convereter.py`.
- **Destructive `cleaner` Property:**
  - When `action == "config"` is executed, `output.cleaner` deletes all files in `exported/<dst_vendor>/` except `policies.txt`. Keep this in mind when debugging output generation.
- **Uploaded File Deletion:**
  - `output.delete` removes `configs/<cfg_file>` immediately upon completing config processing. If you need to inspect the input during debugging, either comment out `output.delete` temporarily or copy the file before running.
- **Flask Secret Key:**
  - `app.secret_key` in `app.py` is currently hardcoded for session messages. If refactoring for production, load it from an environment variable with a safe fallback.
- **Palo Alto XML Input Requirement:**
  - PAN-OS XML configurations exported via CLI are not wrapped in a single root element. `PaloCfg._job` expects XML to be wrapped in `<root>...</root>` tags containing `<response>`.
- **Check Point Policy Batching:**
  - Check Point R80+ `mgmt_cli` can fail if too many commands are pasted at once. The generated script issues `publish` actions every ~100 lines and requires manual session ID or authentication insertion.
- **FortiGate Name Length:**
  - FortiOS policy names are restricted to 35 characters. Longer names from source firewalls are truncated in FortiOS policy converters.
