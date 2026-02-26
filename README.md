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
