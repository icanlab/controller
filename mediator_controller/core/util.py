import copy
import json
import logging
import re

from flask import current_app
from lxml import etree

logger = logging.getLogger(__name__)
_PARSER = etree.XMLParser(remove_blank_text=True)


def make_response_json(obj, status=200, headers=None):
    if not isinstance(obj, (str, bytes, bytearray)):
        response = json.dumps(obj)
    else:
        response = obj  # type: ignore [assignment]
    return current_app.response_class(
        response, status, headers, mimetype="application/json"
    )


def make_response_xml(element_or_tree, status=200, headers=None):
    if not isinstance(element_or_tree, (str, bytes, bytearray)):
        response = etree.tostring(
            element_or_tree, encoding="utf-8", xml_declaration=True, pretty_print=True
        )
    else:
        response = element_or_tree
    logger.info(response if isinstance(response, str) else response.decode())
    return current_app.response_class(
        response, status, headers, mimetype="application/xml"
    )


def encapsulate_data(ele):
    data = etree.Element("data")
    data.append(copy.copy(ele))
    return data


def _log_ele(ele):
    temp = to_xml(ele)
    if not isinstance(temp, str):
        temp = temp.decode()
    return temp


def real_query_data(data_ele, xpath, namespaces):
    results = data_ele.xpath("/data" + xpath, namespaces=namespaces)
    if len(results) == 0:
        return None
    temp = _log_ele(results[0])
    logger.info(f"real_query_data {temp}")
    return results[0]


def query_data(data_ele, xpath, namespaces):
    # data_ele: <data>...</data>
    n = len(data_ele)
    if n > 1:
        raise ValueError("data should have at most one subelement")
    if n == 1:
        results = real_query_data(data_ele, xpath, namespaces)
        # 查不到时返回空配置。
        if results is None:
            return etree.Element("data")
        result = encapsulate_data(results[0])
        temp = _log_ele(result)
        logger.info(f"query_data {result}")
        return result
    if n == 0:
        return data_ele  # empty config


def replace_element(src, dst):
    src_map = {e.tag: e for e in src}
    dst_map = {e.tag: e for e in dst}
    for tag, ele in dst_map.items():
        src_ele = src_map.get(tag)
        if src_ele is None:
            src.append(copy.copy(ele))
        if src_ele is not None and len(ele) > 0:  # 在 src 中，在 dst 中
            replace_element(src_map[tag], ele)
        else:
            src_ele.getparent().replace(src_ele, copy.copy(ele))


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


def extract_module_from_xpath(xpath):
    m = re.match(r"/(?:[^/]+?:)?([^/]+)", xpath)
    if m is None or len(m.groups()) < 1:
        raise ValueError("error xpath: '{}'".format(xpath))
    return m[1]


def to_ele(xml):
    if etree.iselement(xml):
        return xml
    if isinstance(xml, str):
        xml = xml.encode()
    ele = etree.fromstring(xml, parser=_PARSER)
    return ele


def to_xml(ele, pretty_print=False):
    if not etree.iselement(ele):
        return ele
    xml = etree.tostring(
        ele, encoding="utf-8", xml_declaration=True, pretty_print=pretty_print
    )
    return xml
