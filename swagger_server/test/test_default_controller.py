# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_get_controller_config(self):
        """Test case for get_controller_config

        get controller configuration
        """
        query_string = [('neid', 'route 0'),
                        ('xpath', '/a:interfaces'),
                        ('ns_map', '{"a": "urn:ietf:params:xml:ns:yang:ietf-interfaces"}')]
        response = self.client.open(
            '/v1/mediatorservice/get_controller_config',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_device_config(self):
        """Test case for get_device_config

        get device configuration
        """
        query_string = [('neid', 'route 0'),
                        ('xpath', '/a:ifm'),
                        ('ns_map', '{"a": "urn:huawei:yang:huawei-ifm"}')]
        response = self.client.open(
            '/v1/mediatorservice/get_device_config',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_device_info(self):
        """Test case for get_device_info

        get device information
        """
        query_string = [('neid', 'route 0')]
        response = self.client.open(
            '/v1/mediatorservice/get_device_info',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
