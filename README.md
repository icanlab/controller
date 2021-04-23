# Developer Tutorial

## Prerequisites

- Python >= 3.6
- Ansible
- HUAWEI NE Plugin for Ansible
- HUAWEI NE Router
- Redis

## Configure Ansible

Edit `/etc/ansible/hosts`, and add device information:

```
netopeer2 ansible_ssh_host=127.0.0.1  ansible_ssh_port=830  ansible_user=*** ansible_ssh_pass=*** ansible_network_os=ne mediator_device_vendor=HUAWEI mediator_device_type=ROUTER6500 mediator_device_product=HUAWEIOS mediator_device_version=1.0.1111.2
```

## Configure Redis

Start redis-server.

```
redis-server
```

Edit `~/.mediator/controller.yml`, and add redis url:

The following is an example:

```yaml
---
MEDIATOR_DATASTORE_URL: redis://localhost:6379/0
```

## Install mediator-controller

```
git clone https://github.com/icanlab/mediator-controller.git
cd mediator-controller
pip3 install -r requirements.txt
```

## End-to-End Test

Send `get-config` or `edit-config` via `ansible-playbook`.

### get-config

```yaml
---
- name: ietf-interfaces_config
  hosts: netopeer2
  connection: netconf
  gather_facts: no
  vars:
    netconf:
      host: "{{ inventory_hostname }}"
      port: "{{ ansible_ssh_port }}"
      username: "{{ ansible_user }}"
      password: "{{ ansible_ssh_pass }}"
      transport: netconf

  tasks:
    - name: ietf-interfaces_full
        ietf-interfaces_config:
        operation_type: get-config
        interfaces: []
        provider: "{{ netconf }}"
```

### set-config

```yaml
---
- name: ietf-interfaces_config
  hosts: netopeer2
  connection: netconf
  gather_facts: no
  vars:
    netconf:
      host: "{{ inventory_hostname }}"
      port: "{{ ansible_ssh_port }}"
      username: "{{ ansible_user }}"
      password: "{{ ansible_ssh_pass }}"
      transport: netconf

  tasks:
    - name: ietf-interfaces_full
        ietf-interfaces_config:
        operation_type: config
        operation_specs:
            - path: "/config/interfaces/interface[name=\"GigabitEthernet 3/0/1\"]"
            operation: merge
            - path: "/config/interfaces/interface[name=\"GigabitEthernet 3/0/1\"]/ipv4"
            operation: merge
        interfaces:
            - interface:
                name: "GigabitEthernet 3/0/1"
                type: "ianaift:ethernetCsmacd"
                ipv4:
                - address:
                    ip: "192.0.2.3"
                    prefix-length: 32
        provider: "{{ netconf }}"
```
