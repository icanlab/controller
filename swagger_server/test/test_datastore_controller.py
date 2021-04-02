# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.input_msg import InputMsg  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_datastore_get_controller_config_get(self):
        """Test case for datastore_get_controller_config_get

        get controller configuration
        """
        query_string = [('neid', 'neid_example'),
                        ('source', 'source_example'),
                        ('module', 'module_example')]
        response = self.client.open(
            '/v1/datastore/get_controller_config',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_datastore_get_device_config_get(self):
        """Test case for datastore_get_device_config_get

        get device configuration
        """
        query_string = [('neid', 'neid_example'),
                        ('source', 'source_example'),
                        ('module', 'module_example')]
        response = self.client.open(
            '/v1/datastore/get_device_config',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_datastore_query_controller_config_get(self):
        """Test case for datastore_query_controller_config_get

        query controller configuration
        """
        query_string = [('neid', 'neid_example'),
                        ('source', 'source_example'),
                        ('module', 'module_example'),
                        ('xpath', 'xpath_example'),
                        ('ns_map', 'ns_map_example')]
        response = self.client.open(
            '/v1/datastore/query_controller_config',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_datastore_query_device_config_get(self):
        """Test case for datastore_query_device_config_get

        query device configuration
        """
        query_string = [('neid', 'neid_example'),
                        ('source', 'source_example'),
                        ('module', 'module_example'),
                        ('xpath', 'xpath_example'),
                        ('ns_map', 'ns_map_example')]
        response = self.client.open(
            '/v1/datastore/query_device_config',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_datastore_set_controller_config_post(self):
        """Test case for datastore_set_controller_config_post

        set controller configuration
        """
        body = InputMsg()
        response = self.client.open(
            '/v1/datastore/set_controller_config',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_datastore_set_device_config_post(self):
        """Test case for datastore_set_device_config_post

        set device configuration
        """
        body = InputMsg()
        response = self.client.open(
            '/v1/datastore/set_device_config',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_datastore_update_controller_config_post(self):
        """Test case for datastore_update_controller_config_post

        update controller configuration
        """
        body = InputMsg()
        response = self.client.open(
            '/v1/datastore/update_controller_config',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_datastore_update_device_config_post(self):
        """Test case for datastore_update_device_config_post

        update device configuration
        """
        body = InputMsg()
        response = self.client.open(
            '/v1/datastore/update_device_config',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
