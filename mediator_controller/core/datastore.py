import copy
import json
import logging
import re

from lxml import etree
from redis import Redis

from .util import query_data, real_query_data, replace_element, to_ele, to_xml


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

    def _update_config(self, key, xpath, namespaces, ele):
        config = self._get_config(key)
        replace_element(config, ele)
        self._set_config(key, config)

    def update_controller_config(self, neid, source, module, xpath, namespaces, ele):
        key = _ckey(neid, source, module)
        self._update_config(key, xpath, namespaces, ele)

    def update_device_config(self, neid, source, module, xpath, namespaces, ele):
        key = _ckey(neid, source, module)
        self._update_config(key, xpath, namespaces, ele)

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

    # ======== #
    #  XXXXXX  #
    # ======== #

    def _update_redis_for_mediator(self, data, key):
        if "key_list" not in data:
            xpath = data["xpath"]
            # Strip namespace prefix
            xpath = re.sub(r"(?:[^[/]+?:)", "", xpath)
            path_list = []
            i = xpath.find("]")
            while i != -1:
                path = xpath[: i + 1]
                path = re.sub(r"\[(.+?)=.+?\]", r"/\1", path)
                path_list.append(path)
                i = xpath.find("]", i + 1)
            data["key_list"] = path_list

        origin = self._get_config(key)

        if data["operation"] == "delete":
            xpath = data["xpath"]
            namespaces = data["namespaces"]
            delete_config(origin, xpath, namespaces)
            self._set_config(key, origin)
        else:
            config = to_ele(data["config"])
            key_list = data["key_list"]
            merge_config(origin, config, key_list)
            self._set_config(key, origin)

    def update_redis_for_mediator(self, neid, source, type):
        if type == "controller":
            data_str = self._redis.get("temp_data_controller")
            data_list = json.loads(data_str)
            for data in data_list:
                module = data["module"]
                key = _ckey(neid, source, module)
                self._update_redis_for_mediator(data, key)
            #self._redis.delete("temp_data_controller")

        elif type == "device":
            data_str = self._redis.get("temp_data_device")
            data = json.loads(data_str)
            module = data["module"]
            key = _dkey(neid, source, module)
            self._update_redis_for_mediator(data, key)
            #self._redis.delete("temp_data_device")

        else:
            raise ValueError(f"unknown type {type!r}")


datastore = Datastore()

logger = logging.getLogger(__name__)


def delete_config(origin, xpath, namespaces):
    ele = origin.xpath(xpath, namespaces=namespaces)[0]
    ele.getparent().remove(ele)
    logger.debug(to_xml(origin, pretty_print=True).decode())


def merge_config(origin, config, key_list):
    currpath = "/data"
    key_prefix_set = set()
    key_name_set = set()
    for key in key_list:
        i = key.rfind("/")
        key_prefix_set.add(key[:i])
        key_name_set.add(key[i + 1 :])
    _merge_config(origin, config, currpath, key_prefix_set, key_name_set)
    logger.debug(to_xml(origin, pretty_print=True).decode())


def _get_tag_map(ele):
    return {etree.QName(child).localname: child for child in ele}


def _get_key_tag_map(ele, key_name_set):
    result = {}
    for child in ele:
        for x in child:
            if etree.QName(x).localname in key_name_set:
                result[x.text] = child
                break
    return result


def _is_key_node(ele, currpath, key_prefix_set):
    for child in ele:
        path = currpath + "/" + etree.QName(child).localname
        if path in key_prefix_set:
            return True
    return False


def _merge_config(src, dst, currpath, key_prefix_set, key_name_set):
    if len(dst) == 0 and dst.text:
        src.text = dst.text
        return

    if _is_key_node(dst, currpath, key_prefix_set):
        src_key_tag_map = _get_key_tag_map(src, key_name_set)
        dst_key_tag_map = _get_key_tag_map(dst, key_name_set)
        if not dst_key_tag_map:
            return
        for key_tag, ele in dst_key_tag_map.items():
            if key_tag in src_key_tag_map:
                _merge_config(
                    src_key_tag_map[key_tag],
                    ele,
                    currpath + "/" + key_tag,
                    key_prefix_set,
                    key_name_set,
                )
            else:
                src.append(copy.copy(ele))
    else:
        src_tag_map = _get_tag_map(src)
        dst_tag_map = _get_tag_map(dst)
        if not dst_tag_map:
            return
        for tag, ele in dst_tag_map.items():
            if tag in src_tag_map:
                _merge_config(
                    src_tag_map[tag],
                    ele,
                    currpath + "/" + tag,
                    key_prefix_set,
                    key_name_set,
                )
            else:
                src.append(copy.copy(ele))
