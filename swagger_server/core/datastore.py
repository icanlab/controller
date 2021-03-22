from lxml import etree
from ncclient.xml_ import to_ele, to_xml
from redis import Redis


def _ckey(neid, source):
    return "controller:{}:{}".format(neid, source)


def _dkey(neid, source):
    return "device:{}:{}".format(neid, source)


class Datastore(object):
    def __init__(self, **kwargs):
        self._redis = Redis(**kwargs)

    # ==========
    # GET
    # ==========

    def _get_config(self, key):
        xml = self._redis.get(key)
        return to_ele(xml)

    def get_controller_config(self, neid, source):
        key = _ckey(neid, source)
        return self._get_config(key)

    def get_device_config(self, neid, source):
        key = _dkey(neid, source)
        return self._get_config(key)

    # ==========
    # SET
    # ==========

    def _set_config(self, key, ele):
        xml = to_xml(ele)
        return self._redis.set(key, xml)

    def set_controller_config(self, neid, source, ele):
        key = _ckey(neid, source)
        return self._set_config(key, ele)

    def set_device_config(self, neid, source, ele):
        key = _dkey(neid, source)
        return self._set_config(key, ele)

    # ==========
    # QUERY
    # ==========

    def _query_config(self, key, xpath, ns_map):
        xml = self._redis.get(key)
        ele = to_ele(xml)
        return ele.xpath(xpath, namespaces=ns_map)

    def query_controller_config(self, neid, source, xpath, ns_map):
        key = _ckey(neid, source)
        return self._query_config(key, xpath, ns_map)

    def query_device_config(self, neid, source, xpath, ns_map):
        key = _dkey(neid, source)
        return self._query_config(key, xpath, ns_map)
