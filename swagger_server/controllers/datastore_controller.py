from swagger_server.core.datastore import datastore


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
    return 'do some magic!'


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
    return 'do some magic!'


def datastore_query_controller_config_get(neid, source, module, xpath, ns_map):  # noqa: E501
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
    return 'do some magic!'


def datastore_query_device_config_get(neid, source, module, xpath, ns_map):  # noqa: E501
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
    return 'do some magic!'


def datastore_set_controller_config_post(body=None):  # noqa: E501
    """set controller configuration

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = InputMsg.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def datastore_set_device_config_post(body=None):  # noqa: E501
    """set device configuration

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = InputMsg.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def datastore_update_controller_config_post(body=None):  # noqa: E501
    """update controller configuration

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = InputMsg.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def datastore_update_device_config_post(body=None):  # noqa: E501
    """update device configuration

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = InputMsg.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
