from lxml import etree
from ncclient.xml_ import to_ele, to_xml
from redis import Redis


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
