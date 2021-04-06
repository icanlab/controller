from lxml import etree
from ncclient.xml_ import to_ele, to_xml
from redis import Redis

from .util import query_data


def _resolve_module(ele):
    return etree.QName(ele[0].tag).localname


def _ckey(neid, source, module):
    return "controller:{}:{}:{}".format(neid, source, module)


def _dkey(neid, source, module):
    return "device:{}:{}:{}".format(neid, source, module)


class Datastore(object):
    def __init__(self, app=None):
        self._redis = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        url = app.config.get("MEDIATOR_DATASTORE_URL", "redis://localhost:6379/0")
        self._redis = Redis.from_url(url)

    # ===== #
    #  GET  #
    # ===== #

    def _get_config(self, key):
        xml = self._redis.get(key)
        if xml is None:
            return etree.Element("data")
        return to_ele(xml)

    def get_controller_config(self, neid, source, module):
        key = _ckey(neid, source, module)
        return self._get_config(key)

    def get_device_config(self, neid, source, module):
        key = _dkey(neid, source, module)
        return self._get_config(key)

    # ===== #
    #  SET  #
    # ===== #

    def _set_config(self, key, ele):
        xml = to_xml(ele)
        return self._redis.set(key, xml)

    def set_controller_config(self, neid, source, module, ele):
        # NE 插件难以获取 module，因此 module 为空串时，datastore 从报文中推断 module。
        # 由于无法推断空配置的 module，故不存储空配置。
        if len(ele) == 0:
            return
        if not module:
            module = _resolve_module(ele)
        key = _ckey(neid, source, module)
        return self._set_config(key, ele)

    def set_device_config(self, neid, source, module, ele):
        # NE 插件难以获取 module，因此 module 为空串时，datastore 从报文中推断 module。
        # 由于无法推断空配置的 module，故不存储空配置。
        if len(ele) == 0:
            return
        if not module:
            module = _resolve_module(ele)
        key = _dkey(neid, source, module)
        return self._set_config(key, ele)

    # ======= #
    #  QUERY  #
    # ======= #

    def query_controller_config(self, neid, source, module, xpath, namespaces):
        config = self.get_controller_config(neid, source, module)
        return query_data(config, xpath, namespaces)

    def query_device_config(self, neid, source, module, xpath, namespaces):
        config = self.get_device_config(neid, source, module)
        return query_data(config, xpath, namespaces)

    # ======== #
    #  UPDATE  #
    # ======== #

    def _update_config(self, config):
        raise NotImplementedError

    def update_controller_config(self, neid, source, module, config):
        raise NotImplementedError

    def update_device_config(self, neid, source, module, config):
        raise NotImplementedError


datastore = Datastore()
