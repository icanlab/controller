import json

from flask import current_app
from lxml import etree


def make_response_json(obj, status=200, headers=None):
    response = json.dumps(obj)
    return current_app.response_class(
        response, status, headers, mimetype="application/json"
    )


def make_response_xml(element_or_tree, status=200, headers=None):
    response = etree.tostring(element_or_tree, encoding="utf-8", pretty_print=True)
    return current_app.response_class(
        response, status, headers, mimetype="application/xml"
    )
