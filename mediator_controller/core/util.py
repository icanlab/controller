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


def real_query_data(data_ele, xpath, namespaces):
    result = data_ele.xpath("/data" + xpath, namespaces=namespaces)
    if len(result) == 0:
        return None
    return result[0]


def query_data(data_ele, xpath, namespaces):
    n = len(data_ele)
    if n > 1:
        raise ValueError("data should have at most one subelement")
    if n == 1:
        result = real_query_data(data_ele, xpath, namespaces)
        # 查不到时返回空配置。
        if not result:
            return etree.Element("data")
        return encapsulate_data(result[0])
    if n == 0:
        return data_ele  # empty config


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
