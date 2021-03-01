import json
import os

import connexion
import six
import swagger_server
from flask import current_app
from lxml import etree
from swagger_server import util

swagger_root = os.path.dirname(swagger_server.__file__)
swagger_test = os.path.join(swagger_root, 'test')


def get_controller_config(neid, xpath, ns_map):  # noqa: E501
    """get controller configuration

     # noqa: E501

    :param neid: 
    :type neid: str
    :param xpath: 
    :type xpath: str
    :param ns_map: 
    :type ns_map: str

    :rtype: str
    """
    ns_map = json.loads(ns_map)

    name = xpath[xpath.rfind(':')+1:]
    if 'interfaces' == name:
        filepath = os.path.join(swagger_test, 'controller_current_configuration/ietf_interfaces_cc.xml')
    elif 'routing' == name:
        filepath = os.path.join(swagger_test, 'controller_current_configuration/ietf_routing_cc.xml')
    elif 'l3vpn-ntw' == name:
        filepath = os.path.join(swagger_test, 'controller_current_configuration/ietf_l3vpn_ntw_cc.xml')
    else:
        filepath = os.path.join(swagger_test, 'controller_current_configuration/ietf_interfaces_cc.xml')

    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.parse(filepath, parser)
    controller_config = root.xpath(xpath, namespaces=ns_map)[0]
    result = etree.tostring(controller_config, encoding='utf-8', pretty_print=True).decode()
    return current_app.response_class(result, mimetype="application/xml")


def get_device_config(neid, xpath, ns_map):  # noqa: E501
    """get device configuration

     # noqa: E501

    :param neid: 
    :type neid: str
    :param xpath: 
    :type xpath: str
    :param ns_map: 
    :type ns_map: str

    :rtype: str
    """
    ns_map = json.loads(ns_map)

    name = xpath[xpath.rfind(':') + 1:]
    if 'ifm' == name:
        filepath = os.path.join(swagger_test, 'device_current_configuration/huawei_ifm_cc.xml')
    elif 'bgp' == name:
        filepath = os.path.join(swagger_test, 'device_current_configuration/huawei_bgp_cc.xml')
    elif 'network-instance' == name:
        filepath = os.path.join(swagger_test, 'device_current_configuration/huawei_network_instance_cc.xml')
    else:
        filepath = os.path.join(swagger_test, 'device_current_configuration/huawei_ifm_cc.xml')

    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.parse(filepath, parser)
    device_config = root.xpath(xpath, namespaces=ns_map)[0]
    result = etree.tostring(device_config, encoding='utf-8', pretty_print=True).decode()
    return current_app.response_class(result, mimetype="application/xml")


def get_device_info(neid):  # noqa: E501
    """get device information

     # noqa: E501

    :param neid: 
    :type neid: str

    :rtype: str
    """
    device_info = dict(
        mediator_device_vendor='HUAWEI',
        mediator_device_type='ROUTER6500',
        mediator_device_product='HUAWEIOS',
        mediator_device_version='1.0.1111.2',
    )
    return device_info
