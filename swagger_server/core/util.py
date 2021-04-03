import json
import logging
import re

from flask import current_app
from lxml import etree

logger = logging.getLogger(__name__)


def make_response_json(obj, status=200, headers=None):
    if not isinstance(obj, (str, bytes, bytearray)):
        response = json.dumps(obj)
    else:
        response = obj
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
    logger.info(response)
    return current_app.response_class(
        response, status, headers, mimetype="application/xml"
    )


def query_data(data_ele, xpath, namespaces):
    n = len(data_ele)
    if n > 1:
        raise ValueError("data should have at most one subelement")
    if n == 1:
        result = data_ele.xpath("/data" + xpath, namespaces=namespaces)
        # 查不到时返回空配置。
        if len(result) == 0:
            return etree.Element("data")
        ele = result[0]
        trim_element(ele, data_ele)
    return data_ele


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
    m = re.match(r"/(?:[^/]+?:)?([^/]+)")
    if m is None or len(m.groups()) < 1:
        raise QueryError("error xpath: '{}'".format(xpath))
    return m[1]
