import json
import logging
import os

import connexion
import six
import swagger_server
from lxml import etree
from swagger_server import util
from swagger_server.core.service import (
    query_controller_config,
    query_device_config,
    query_device_info,
)
from swagger_server.core.util import make_response_json, make_response_xml, trim_element

swagger_root = os.path.dirname(swagger_server.__file__)
swagger_test = os.path.join(swagger_root, 'test')

logger = logging.getLogger(__name__)


def _temp_query(filepath, neid, xpath, ns_map):
    with open(filepath, 'rb') as f:
        data = f.read()
    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.fromstring(data, parser)
    assert len(root) <= 1, 'should have at most one module, got {}'.format(len(root))
    if len(root) == 1:
        e = root.xpath('/data' + xpath, namespaces=ns_map)[0]
        trim_element(e, root)
    return root


def temp_query_controller_config(neid, xpath, ns_map):
    if 'interfaces' in xpath:
        filepath = os.path.join(swagger_test, 'controller_current_configuration/ietf_interfaces_cc.xml')
    elif 'routing' in xpath:
        filepath = os.path.join(swagger_test, 'controller_current_configuration/ietf_routing_cc.xml')
    elif 'l3vpn-ntw' in xpath:
        filepath = os.path.join(swagger_test, 'controller_current_configuration/ietf_l3vpn_ntw_cc.xml')
    else:
        filepath = os.path.join(swagger_test, 'controller_current_configuration/ietf_interfaces_cc.xml')
    return _temp_query(filepath, neid, xpath, ns_map)


def temp_query_device_config(neid, xpath, ns_map):
    if 'ifm' in xpath:
        filepath = os.path.join(swagger_test, 'device_current_configuration/huawei_ifm_cc.xml')
    elif 'bgp' in xpath:
        filepath = os.path.join(swagger_test, 'device_current_configuration/huawei_bgp_cc.xml')
    elif 'network-instance' in xpath:
        filepath = os.path.join(swagger_test, 'device_current_configuration/huawei_network_instance_cc.xml')
    else:
        filepath = os.path.join(swagger_test, 'device_current_configuration/huawei_ifm_cc.xml')
    return _temp_query(filepath, neid, xpath, ns_map)


def temp_query_device_info(neid):
    device_info = dict(
        mediator_device_vendor='HUAWEI',
        mediator_device_type='ROUTER6500',
        mediator_device_product='HUAWEIOS',
        mediator_device_version='1.0.1111.2',
    )
    return device_info


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
    try:
        ns_map = json.loads(ns_map)
        controller_config = temp_query_controller_config(neid, xpath, ns_map)
    except Exception as e:
        res = {'errinfo': str(e)}
        return make_response_json(res, 400)
    return make_response_xml(controller_config)


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
    try:
        ns_map = json.loads(ns_map)
        device_config = temp_query_device_config(neid, xpath, ns_map)
        # device_config = query_device_config(neid, xpath, ns_map)
    except Exception as e:
        res = {'errinfo': str(e)}
        return make_response_json(res, 400)
    return make_response_xml(device_config)


def get_device_info(neid):  # noqa: E501
    """get device information

     # noqa: E501

    :param neid: 
    :type neid: str

    :rtype: str
    """
    try:
        # device_info = temp_query_device_info(neid)
        device_info = query_device_info(neid)
    except Exception as e:
        res = {'errinfo': str(e)}
        return make_response_json(res, 400)
    return make_response_json(device_info)
