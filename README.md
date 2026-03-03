Vector Role
===========

This role provides automated installation and configuration of Vector, a lightweight and ultra-fast tool for building observability pipelines that aggregate, transform and route data (logs, metrics, traces, etc.) to numerous popular destinations.

Requirements
------------

- Ansible >= 2.9
- RedHat/CentOS/AlmaLinux 8+ (EL 8, 9)
- Systemd service manager

Role Variables
--------------

Available variables in `defaults/main.yml`:

- `vector_version`: Vector version to install (default: "0.21.0")
- `clickhouse_host`: ClickHouse server hostname/IP (default: "127.0.0.1")
- `clickhouse_user`: ClickHouse user (default: "default")
- `clickhouse_password`: ClickHouse password (default: empty)
- `vector_logs_owner`: Owner of Vector logs directory (default: "root")
- `vector_logs_group`: Group of Vector logs directory (default: "root")
- `vector_logs_path`: Path to Vector logs directory (default: "/var/log/vector")
- `vector_config_dir`: Vector configuration directory (set in vars)

Dependencies
------------

None

Example Playbook
----------------

```yaml
---
- hosts: servers
  roles:
    - role: vector
      vars:
        vector_version: "0.21.0"
        clickhouse_host: "clickhouse.example.com"
        clickhouse_user: "vector_user"
        clickhouse_password: "secure_password"
        vector_logs_path: "/var/log/vector"
```

License
-------

MIT

Author Information
------------------

- **Author**: R.Grivnyashkin
- **Company**: netology-students

Testing & Development
---------------------

### Molecule Test Scenarios

This role includes two Molecule test scenarios:

#### 1. **Default Scenario** (Docker)

Located in `molecule/default/`, this scenario uses Docker to test against 3 platforms:
- AlmaLinux 9
- Ubuntu 22.04
- Debian 12

Run with:
```bash
molecule test
```

#### 2. **Podman Scenario**

Located in `molecule/podman/`, this scenario uses Podman and tests against:
- AlmaLinux 9

Run with:
```bash
molecule test -s podman
```

### Test Sequence

The test sequence performed by `molecule test` includes:

1. `cleanup` / `destroy` – ensure a clean slate
2. `create` – start containers
3. `prepare` – install `python3`/`openssh` and gather facts (see note below)
4. `converge` – apply the role under test
5. `verify` – run simple assertions (package installed, config directory exists,
   version command returns success)
6. `idempotence` – run the role a second time and assert that **no task
   changes anything** (this is how idempotency is automatically verified)
7. additional steps for side effects and cleanup

> ⚠️ during preparation the first `setup` task may report an interpreter error
> on Debian/Ubuntu images; this is normal because Python is not yet
> installed. The playbook now installs Python first and re-runs `setup` so the
> error is harmless.

### Using Tox

[Tox](https://tox.readthedocs.io/) is configured to automate testing across multiple Python and Ansible versions.

#### Installation

Install tox:
```bash
pip install tox
```

Or use the included requirements file:
```bash
pip install -r tox-requirements.txt
```

#### Running Tests with Tox

Run all test environments:
```bash
tox
```

Run a specific test environment:
```bash
tox -e py39-ansible210
tox -e py37-ansible30
```

List available environments:
```bash
tox -l
```

By default, tox uses the **Podman scenario** (`-s podman`) and cleans up containers
(`--destroy always`) after testing. This is configured in `tox.ini`.

### Systemd Note

Container images do not run systemd as PID 1. In those containers any attempt to
run the `systemd` module results in messages such as:

```
Service is in unknown state
System has not been booted with systemd as init system (PID 1)
```

These failures are caught by rescue blocks in the role and are no longer shown
because the task is guarded with `when: ansible_facts['service_mgr']=='systemd'`.
They do not indicate a problem with the role; they simply reflect the limited
container environment. If you wish to test real service management, use a VM
or an image that boots systemd.

Configuration
-------------

A minimal `ansible.cfg` is created at the role root (and also injected via
`molecule.yml`) to avoid permissions problems when Ansible writes temporary
files inside the containers:

```ini
[defaults]
remote_tmp = /tmp/.ansible/tmp
retry_files_enabled = False
```

Running Tests
-------------

### Quick Start

For Molecule tests with Docker:
```bash
# Run the default Docker scenario
molecule test

# Or run only converge and verify on existing instances
molecule converge && molecule verify
```

For Podman-based tests:
```bash
# Run the podman scenario
molecule test -s podman
```

### Using Tox for Complete Test Coverage

For comprehensive testing across multiple Python and Ansible versions:
```bash
# Run all configured test environments
tox

# Run a specific environment
tox -e py39-ansible210
```

All tests should complete with exit code 0 and without unexpected errors.
