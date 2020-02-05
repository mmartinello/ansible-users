mmartinello.users - Ansible Users Manager Role
==============================================

Ansible role which let to easily manage users and their access to Linux servers.

The role has some default groups which are used to manage default user permissions:
- Super administrator: user which has complete root access (using sudo) on every hosts.
- Administrator: user which has complete root access (using sudo) on a specified host or group of hosts.
- Deployer: user which has access to deployer group on a specified host or group of hosts.

Only Linux hosts are supported at the moment.

Requirements
------------

None.

Role Variables
--------------

```yaml
# Superadmin group name (default: admin)
superadmin_group: admin

# Ask sudo password for superadmin users (default: true)
superadmin_ask_pass: true

# Admin group name (default: sudo)
admin_group: sudo

# Ask sudo password for admin users (default: true)
admin_ask_pass: true

# Deployer group name (default: deployer)
deployer_group: deployer

# Ask sudo password to become deployer (default: true)
deployer_become_ask_pass: true

# Users' default group
users_default_group: users

# User list
users: []
```

Users list examples
-------------------

Admin user: has root access on every server

```yaml
users:
  - username: jdoe
    comment: "John Doe"
    group: admin
    password: "$6..."
    keys:
      active:
        - "ssh-rsa ... jdoe@host.local"
    admin: yes

```

Dependencies
------------

None.

Example Playbook
----------------

TODO

License
-------

BSD

Author Information
------------------

Mattia Martinello
mattia@mattiamartinello.com
https://github.com/mmartinello
