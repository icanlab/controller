import copy

from lxml import etree
from redis import Redis

from .util import query_data, to_ele, to_xml, real_query_data


def _resolve_module(module_ele):
    return etree.QName(module_ele.tag).localname


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
        xml = self._redis.get(key)  # type: ignore [union-attr]
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
        xml = to_xml(ele, pretty_print=True)
        self._redis.set(key, xml)  # type: ignore [union-attr]

    def set_controller_config(self, neid, source, module, ele):
        # 由于报文中可能存在多个 module，现在 module 参数会被忽略，datastore 始终从报文中推断 module。
        # 由于无法推断空配置的 module，故不存储空配置。
        if len(ele) == 0:
            return
        # <data> 中可能有多个 module，分别存储。
        for m in ele:
            data = etree.Element("data")
            data.append(copy.copy(m))
            module = _resolve_module(m)
            key = _ckey(neid, source, module)
            self._set_config(key, data)

    def set_device_config(self, neid, source, module, ele):
        # 由于报文中可能存在多个 module，现在 module 参数会被忽略，datastore 始终从报文中推断 module。
        # 由于无法推断空配置的 module，故不存储空配置。
        if len(ele) == 0:
            return
        # <data> 中可能有多个 module，分别存储。
        for m in ele:
            data = etree.Element("data")
            data.append(copy.copy(m))
            module = _resolve_module(m)
            key = _dkey(neid, source, module)
            self._set_config(key, data)

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

    def update_controller_config(self, neid, source, module, xpath, namespaces, ele):
        old = self.query_controller_config(neid, source, module, xpath, namespaces)
        parent = old.getparent()
        parent.replace(old, ele)

    def update_device_config(self, neid, source, module, xpath, namespaces, ele):
        old = self.query_device_config(neid, source, module, xpath, namespaces)
        parent = old.getparent()
        parent.replace(old, ele)

    # ======== #
    #  DELETE  #
    # ======== #

    def _delete_config(self, key, xpath, namespaces):
        config = self._get_config(key)
        old = real_query_data(config, xpath, namespaces)
        parent = old.getparent()
        parent.remove(old)
        self._set_config(key, config)


    def delete_controller_config(self, neid, source, module, xpath, namespaces):
        key = _ckey(neid, source, module)
        self._delete_config(key, xpath, namespaces)

    def delete_device_config(self, neid, source, module, xpath, namespaces):
        key = _ckey(neid, source, module)
        self._delete_config(key, xpath, namespaces)


datastore = Datastore()
