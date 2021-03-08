import json
import logging
import subprocess

from lxml import etree

logger = logging.getLogger(__name__)


class MediatorServiceError(Exception):
    """Base class for Mediator Service exceptions."""


class AnsibleCommandError(MediatorServiceError):
    """Ansible command error occurred."""


class QueryError(MediatorServiceError):
    """Query error occurred."""


def _ansible_inventory_host(host):
    # Execute Ansible command to fetch device information in the inventory.
    args = ["ansible-inventory", "--host", host]
    try:
        p = subprocess.run(args, capture_output=True, check=True)
        data = json.loads(p.stdout)
    except subprocess.CalledProcessError as e:
        msg = "Ansible command error: %s" % e.stderr.decode("utf-8", "ignore")
        logger.error(msg)
        raise AnsibleCommandError(msg)
    except Exception as e:
        msg = "System error"
        logger.error(msg + ": " + str(e))
        raise AnsibleCommandError(msg)
    return data


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

    data = _ansible_inventory_host(neid)

    vendor = data.get("mediator_device_vendor")
    type = data.get("mediator_device_type")
    product = data.get("mediator_device_product")
    version = data.get("mediator_device_version")

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

    # TODO: command incomplete
    args = ["ansible", neid]
    try:
        p = subprocess.run(args, capture_output=True, check=True)
        data = json.loads(p.stdout)
    except subprocess.CalledProcessError as e:
        msg = "Ansible command error: %s" % e.stderr.decode("utf-8", "ignore")
        logger.error(msg)
        raise AnsibleCommandError(msg)
    except Exception as e:
        msg = "System error"
        logger.error(msg + ": " + str(e))
        raise AnsibleCommandError(msg)

    # TODO: parse ansible output
    device_config = etree.fromstring(data["xxx"])
    result = device_config.xpath(xpath, namespaces=namespaces)
    if not result:
        msg = "Device configuration '%s' for neid '%s' not exists" % (xpath, neid)
        logger.error(msg)
        raise QueryError(msg)
    return result[0]
