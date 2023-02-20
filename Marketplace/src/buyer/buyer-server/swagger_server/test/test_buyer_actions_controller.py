# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from swagger_server.models.inline_response2004 import InlineResponse2004  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.models.search import Search  # noqa: E501
from swagger_server.models.search1 import Search1  # noqa: E501
from swagger_server.test import BaseTestCase


class TestBuyerActionsController(BaseTestCase):
    """BuyerActionsController integration test stubs"""

    def test_purchase_history_get(self):
        """Test case for purchase_history_get

        Get purchase history
        """
        query_string = [('buyer_id', 56)]
        response = self.client.open(
            '/api/v1/purchase_history',
            method='GET',
            content_type='multipart/form-data',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_purchase_post(self):
        """Test case for purchase_post

        Purchase items added in the cart
        """
        search = Search1()
        response = self.client.open(
            '/api/v1/purchase',
            method='POST',
            data=json.dumps(search),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_items_get(self):
        """Test case for search_items_get

        Search for items
        """
        search = Search()
        response = self.client.open(
            '/api/v1/search-items',
            method='GET',
            data=json.dumps(search),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_seller_feedback_post(self):
        """Test case for seller_feedback_post

        Provide seller Feedback
        """
        query_string = [('seller_id', 56),
                        ('buyer_id', 56)]
        response = self.client.open(
            '/api/v1/seller_feedback',
            method='POST',
            content_type='multipart/form-data',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_seller_rating_get(self):
        """Test case for seller_rating_get

        Get seller rating
        """
        query_string = [('seller_id', 56),
                        ('buyer_id', 56)]
        response = self.client.open(
            '/api/v1/seller_rating',
            method='GET',
            content_type='multipart/form-data',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
