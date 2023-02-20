# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.body import Body  # noqa: E501
from swagger_server.models.inline_response2007 import InlineResponse2007  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCartController(BaseTestCase):
    """CartController integration test stubs"""

    def test_cart_add_post(self):
        """Test case for cart_add_post

        Add item to shopping cart
        """
        body = Body()
        response = self.client.open(
            '/api/v1/cart/add',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cart_remove_delete(self):
        """Test case for cart_remove_delete

        Remove item from shopping cart
        """
        query_string = [('item_id', 789),
                        ('quantity', 56),
                        ('buyer_id', 789)]
        response = self.client.open(
            '/api/v1/cart/remove',
            method='DELETE',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_clear_cart_post(self):
        """Test case for clear_cart_post

        Clear the shopping cart for a given buyer
        """
        query_string = [('buyer_id', 56)]
        response = self.client.open(
            '/api/v1/clear-cart',
            method='POST',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_display_cart_get(self):
        """Test case for display_cart_get

        Get the contents of the shopping cart for a given buyer
        """
        query_string = [('buyer_id', 56)]
        response = self.client.open(
            '/api/v1/display-cart',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
