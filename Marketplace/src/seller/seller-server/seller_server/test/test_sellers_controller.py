# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from seller_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from seller_server.models.inline_response4001 import InlineResponse4001  # noqa: E501
from seller_server.models.inline_response404 import InlineResponse404  # noqa: E501
from seller_server.models.inline_response5002 import InlineResponse5002  # noqa: E501
from seller_server.test import BaseTestCase


class TestSellersController(BaseTestCase):
    """SellersController integration test stubs"""

    def test_seller_rating_get(self):
        """Test case for seller_rating_get

        Get seller rating
        """
        query_string = [('seller_id', 'seller_id_example')]
        response = self.client.open(
            '/api/v1/seller/rating',
            method='GET',
            content_type='multipart/form-data',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
