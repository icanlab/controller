import json
import logging
import subprocess

from lxml import etree
from ncclient import manager

logger = logging.getLogger(__name__)


class MediatorServiceError(Exception):
    """Base class for Mediator Service exceptions."""


class AnsibleCommandError(MediatorServiceError):
    """Ansible command error occurred."""


class QueryError(MediatorServiceError):
    """Query error occurred."""


def _ansible_inventory_host(host):
    # Execute Ansible command to fetch host information in the inventory.
    args = ["ansible-inventory", "--host", host]
    try:
        p = subprocess.run(args, capture_output=True, check=True)
        inventory = json.loads(p.stdout)
    except subprocess.CalledProcessError as e:
        msg = "Ansible command error: %s" % e.stderr.decode("utf-8", "ignore")
        logger.error(msg)
        raise AnsibleCommandError(msg)
    except Exception as e:
        msg = "System error"
        logger.error(msg + ": " + str(e))
        raise AnsibleCommandError(msg)
    return inventory


def query_device_info(neid):
    """Query device information.

    Parameters
    ----------
    neid : str
        Device name.

    Returns
    -------
    device_info : dict
        Device information containing 'vendor', 'type', 'product' and 'version'
        as dict keys.
    """

    inventory = _ansible_inventory_host(neid)

    vendor = inventory.get("mediator_device_vendor")
    type = inventory.get("mediator_device_type")
    product = inventory.get("mediator_device_product")
    version = inventory.get("mediator_device_version")

    # Check for missing device information.
    if vendor is None:
        msg = "Cannot find vendor for neid '%s'" % neid
        logger.error(msg)
        raise QueryError(msg)
    if type is None:
        msg = "Cannot find type for neid '%s'" % neid
        logger.error(msg)
        raise QueryError(msg)
    if product is None:
        msg = "Cannot find product for neid '%s'" % neid
        logger.error(msg)
        raise QueryError(msg)
    if version is None:
        msg = "Cannot find version for neid '%s'" % neid
        logger.error(msg)
        raise QueryError(msg)

    device_info = {
        "vendor": vendor,
        "type": type,
        "product": product,
        "version": version,
    }
    return device_info


def query_controller_config(neid, xpath, namespaces=None):
    """Query controller configuration.

    Parameters
    ----------
    neid : str
        Device name.
    xpath : str
        XPath of controller configuration.
    namespaces : dict, optional
        Namespaces used by XPath.

    Returns
    -------
    controller_config : lxml.etree._Element
        Controller configuration.
    """


def query_device_config(neid, xpath, namespaces=None):
    """Query device configuration.

    Parameters
    ----------
    neid : str
        Device name.
    xpath : str
        XPath of device configuration.
    namespaces : dict, optional
        Namespaces used by XPath.

    Returns
    -------
    device_config : lxml.etree._Element
        Device configuration.
    """

    inventory = _ansible_inventory_host(neid)

    # Since Ansible 2.0, variables like ansible_ssh_* are deprecated. However,
    # they are used by HUAWEI NE Plugin.
    host = inventory.get("ansible_ssh_host")
    if host is None:
        host = inventory.get("ansible_host")
    port = inventory.get("ansible_ssh_port")
    if port is None:
        port = inventory.get("ansible_port")
    username = inventory.get("ansible_ssh_user")
    if username is None:
        username = inventory.get("ansible_user")
    password = inventory.get("ansible_ssh_pass")
    if password is None:
        password = inventory.get("ansible_pass")

    if host is None:
        msg = "Cannot find host for neid '{}'" % host
        logger.error(msg)
        raise QueryError(msg)
    if port is None:
        msg = "Cannot find port for neid '{}'" % port
        logger.error(msg)
        raise QueryError(msg)
    if username is None:
        msg = "Cannot find username for neid '{}'" % username
        logger.error(msg)
        raise QueryError(msg)
    if password is None:
        msg = "Cannot find password for neid '{}'" % password
        logger.error(msg)
        raise QueryError(msg)

    conn = manager.connect(
        host=host, port=port, username=username, password=password, hostkey_verify=False
    )
    reply = conn.get_config(source="running", filter=("xpath", (namespaces, xpath)))
    return reply.data_ele[0]
