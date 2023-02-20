# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from seller_server.models.inline_response2004 import InlineResponse2004  # noqa: E501
from seller_server.models.inline_response2005 import InlineResponse2005  # noqa: E501
from seller_server.models.inline_response2006 import InlineResponse2006  # noqa: E501
from seller_server.models.inline_response201 import InlineResponse201  # noqa: E501
from seller_server.models.inline_response4002 import InlineResponse4002  # noqa: E501
from seller_server.models.inline_response401 import InlineResponse401  # noqa: E501
from seller_server.models.inline_response404 import InlineResponse404  # noqa: E501
from seller_server.models.inline_response4041 import InlineResponse4041  # noqa: E501
from seller_server.test import BaseTestCase


class TestItemsController(BaseTestCase):
    """ItemsController integration test stubs"""

    def test_display_get(self):
        """Test case for display_get

        Display items
        """
        query_string = [('seller_id', 'seller_id_example')]
        response = self.client.open(
            '/api/v1/display',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_items_item_id_delete(self):
        """Test case for items_item_id_delete

        Remove an item from sale
        """
        data = dict(quantity=56,
                    seller_id='seller_id_example')
        response = self.client.open(
            '/api/v1/items/{item_id}'.format(item_id='item_id_example'),
            method='DELETE',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_items_item_id_sale_price_put(self):
        """Test case for items_item_id_sale_price_put

        Change the sale price of an item
        """
        data = dict(new_sale_price=3.4,
                    seller_id='seller_id_example')
        response = self.client.open(
            '/api/v1/items/{item_id}/sale_price'.format(item_id='item_id_example'),
            method='PUT',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_items_post(self):
        """Test case for items_post

        Put an item for sale
        """
        data = dict(item_id='item_id_example',
                    item_name='item_name_example',
                    item_category='item_category_example',
                    keywords='keywords_example',
                    condition='condition_example',
                    sale_price=3.4,
                    quantity=56,
                    seller_id='seller_id_example')
        response = self.client.open(
            '/api/v1/items',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
