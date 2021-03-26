from lxml import etree
from ncclient.xml_ import to_ele, to_xml
from redis import Redis


def trim_element(ele, top):
    if ele is top:
        return
    parent = ele.getparent()
    if parent is None:
        return
    for e in parent.getchildren():
        if e is not ele:
            parent.remove(e)
    trim_element(parent, top)


def _ckey(neid, source, module):
    return "controller:{}:{}:{}".format(neid, source, module)


def _dkey(neid, source, module):
    return "device:{}:{}:{}".format(neid, source, module)


class Datastore(object):
    def __init__(self, **kwargs):
        self._redis = Redis(**kwargs)

    # ==========
    # GET
    # ==========

    def _get_config(self, key):
        xml = self._redis.get(key)
        if xml is None:
            raise ValueError
        return to_ele(xml)

    def get_controller_config(self, neid, source, module):
        key = _ckey(neid, source, module)
        return self._get_config(key)

    def get_device_config(self, neid, source, module):
        key = _dkey(neid, source, module)
        return self._get_config(key)

    # ==========
    # SET
    # ==========

    def _set_config(self, key, ele):
        xml = to_xml(ele)
        return self._redis.set(key, xml)

    def set_controller_config(self, neid, source, module, ele):
        key = _ckey(neid, source, module)
        return self._set_config(key, ele)

    def set_device_config(self, neid, source, module, ele):
        key = _dkey(neid, source, module)
        return self._set_config(key, ele)

    # ==========
    # QUERY
    # ==========

    def _query_config(self, config, xpath, namespaces):
        target = config.xpath(xpath, namespaces=namespaces)
        trim_element(target, config)
        return config

    def query_controller_config(self, neid, source, module, xpath, namespaces):
        config = self.get_controller_config(neid, source, module)
        return self._query_config(config, xpath, namespaces)

    def query_device_config(self, neid, source, module, xpath, namespaces):
        config = self.get_device_config(neid, source, module)
        return self._query_config(config, xpath, namespaces)

    # ==========
    # UPDATE
    # ==========

    def _update_config(self, config):
        raise NotImplementedError

    def update_controller_config(self, neid, source, module, config):
        raise NotImplementedError

    def update_device_config(self, neid, source, module, config):
        raise NotImplementedError
