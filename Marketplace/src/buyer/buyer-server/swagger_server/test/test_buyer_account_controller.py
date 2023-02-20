# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.account import Account  # noqa: E501
from swagger_server.models.credentials import Credentials  # noqa: E501
from swagger_server.models.inline_response2005 import InlineResponse2005  # noqa: E501
from swagger_server.models.inline_response2006 import InlineResponse2006  # noqa: E501
from swagger_server.models.inline_response201 import InlineResponse201  # noqa: E501
from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.models.inline_response401 import InlineResponse401  # noqa: E501
from swagger_server.test import BaseTestCase


class TestBuyerAccountController(BaseTestCase):
    """BuyerAccountController integration test stubs"""

    def test_account_post(self):
        """Test case for account_post

        Create a new buyer account
        """
        account = Account()
        response = self.client.open(
            '/api/v1/account',
            method='POST',
            data=json.dumps(account),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login_post(self):
        """Test case for login_post

        Log in to an existing account
        """
        credentials = Credentials()
        response = self.client.open(
            '/api/v1/login',
            method='POST',
            data=json.dumps(credentials),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_logout_buyer_id_get(self):
        """Test case for logout_buyer_id_get

        Log out of an existing account
        """
        response = self.client.open(
            '/api/v1/logout/{buyer_id}'.format(buyer_id=56),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
