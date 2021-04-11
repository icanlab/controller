import json

import connexion

from swagger_server.core.datastore import datastore
from swagger_server.core.util import make_response_json, make_response_xml, to_ele
from swagger_server.models.input_msg import InputMsg


def datastore_get_controller_config_get(neid, source, module):  # noqa: E501
    """get controller configuration

     # noqa: E501

    :param neid:
    :type neid: str
    :param source:
    :type source: str
    :param module:
    :type module: str

    :rtype: str
    """
    try:
        ele = datastore.get_controller_config(neid, source, module)
    except Exception as e:
        res = {"errinfo": str(e)}
        return make_response_json(res, 400)
    return make_response_xml(ele)


def datastore_get_device_config_get(neid, source, module):  # noqa: E501
    """get device configuration

     # noqa: E501

    :param neid:
    :type neid: str
    :param source:
    :type source: str
    :param module:
    :type module: str

    :rtype: str
    """
    try:
        ele = datastore.get_device_config(neid, source, module)
    except Exception as e:
        res = {"errinfo": str(e)}
        return make_response_json(res, 400)
    return make_response_xml(ele)


def datastore_query_controller_config_get(
    neid, source, module, xpath, ns_map
):  # noqa: E501
    """query controller configuration

     # noqa: E501

    :param neid:
    :type neid: str
    :param source:
    :type source: str
    :param module:
    :type module: str
    :param xpath:
    :type xpath: str
    :param ns_map:
    :type ns_map: str

    :rtype: str
    """
    try:
        ns_map = json.loads(ns_map)
        ele = datastore.query_controller_config(neid, source, module, xpath, ns_map)
    except Exception as e:
        res = {"errinfo": str(e)}
        return make_response_json(res, 400)
    return make_response_xml(ele)


def datastore_query_device_config_get(
    neid, source, module, xpath, ns_map
):  # noqa: E501
    """query device configuration

     # noqa: E501

    :param neid:
    :type neid: str
    :param source:
    :type source: str
    :param module:
    :type module: str
    :param xpath:
    :type xpath: str
    :param ns_map:
    :type ns_map: str

    :rtype: str
    """
    try:
        ns_map = json.loads(ns_map)
        ele = datastore.query_device_config(neid, source, module, xpath, ns_map)
    except Exception as e:
        res = {"errinfo": str(e)}
        return make_response_json(res, 400)
    return make_response_xml(ele)


def datastore_set_controller_config_post(body=None):  # noqa: E501
    """set controller configuration

     # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        try:
            body = InputMsg.from_dict(connexion.request.get_json())  # noqa: E501
            neid = body.neid
            source = body.source
            module = body.module
            ele = to_ele(body.data)
            datastore.set_controller_config(neid, source, module, ele)
        except Exception as e:
            res = {"errinfo": str(e)}
            return make_response_json(res, 400)
        return make_response_json({"ok": 200})
    return "do some magic!"


def datastore_set_device_config_post(body=None):  # noqa: E501
    """set device configuration

     # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        try:
            body = InputMsg.from_dict(connexion.request.get_json())  # noqa: E501
            neid = body.neid
            source = body.source
            module = body.module
            ele = to_ele(body.data)
            datastore.set_device_config(neid, source, module, ele)
        except Exception as e:
            res = {"errinfo": str(e)}
            return make_response_json(res, 400)
        return make_response_json({"ok": 200})
    return "do some magic!"


def datastore_update_controller_config_post(body=None):  # noqa: E501
    """update controller configuration

     # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = InputMsg.from_dict(connexion.request.get_json())  # noqa: E501
        neid = body.neid
        source = body.source
        module = body.module
        data = body.data
        try:
            datastore.update_controller_config(neid, source, module, data)
        except Exception as e:
            res = {"errinfo": str(e)}
            return make_response_json(res, 400)
        return make_response_json({"ok": 200})
    return "do some magic!"


def datastore_update_device_config_post(body=None):  # noqa: E501
    """update device configuration

     # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = InputMsg.from_dict(connexion.request.get_json())  # noqa: E501
        neid = body.neid
        source = body.source
        module = body.module
        data = body.data
        try:
            datastore.update_device_config(neid, source, module, data)
        except Exception as e:
            res = {"errinfo": str(e)}
            return make_response_json(res, 400)
        return make_response_json({"ok": 200})
    return "do some magic!"
