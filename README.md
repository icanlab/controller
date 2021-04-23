# Developer Tutorial

## Prerequisites

- Python >= 3.6
- Ansible
- HUAWEI NE Plugin for Ansible
- HUAWEI NE Router
- Redis

## Ansible configuration

Edit `/etc/ansible/hosts`, and add device information:

```
netopeer2 ansible_ssh_host=127.0.0.1  ansible_ssh_port=830  ansible_user=*** ansible_ssh_pass=*** ansible_network_os=ne mediator_device_vendor=HUAWEI mediator_device_type=ROUTER6500 mediator_device_product=HUAWEIOS mediator_device_version=1.0.1111.2
```

## Redis configuration

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
