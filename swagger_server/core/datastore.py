from lxml import etree
from redis import Redis


def _ckey(neid, source):
    return "controller:{}:{}".format(neid, source)


class Datastore(object):
    def __init__(self, **kwargs):
        self._redis = Redis(**kwargs)
        self._parser = etree.XMLParser(remove_blank_text=True)

    def from_xml(self, xml):
        return etree.fromstring(xml, self.parser)

    def to_xml(self, ele):
        return etree.tostring(ele, encoding="utf-8")

    def get_controller_config(self, xpath, ns_map, neid, source):
        key = _ckey(neid, source)
        data = self._redis.get(key)
        config = self.from_xml(data)
        return config.xpath(xpath, namespaces=ns_map)
