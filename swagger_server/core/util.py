import json

from flask import current_app
from lxml import etree


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
    return current_app.response_class(
        response, status, headers, mimetype="application/xml"
    )


def trim_element(ele, top):
    parent = ele.getparent()
    if parent is None:
        return
    for e in parent.getchildren():
        if e is not ele:
            parent.remove(e)
    trim_element(parent, top)
