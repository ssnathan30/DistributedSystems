# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from seller_server.models.inline_response200 import InlineResponse200  # noqa: E501
from seller_server.models.inline_response400 import InlineResponse400  # noqa: E501
from seller_server.models.inline_response500 import InlineResponse500  # noqa: E501
from seller_server.test import BaseTestCase


class TestAccountsController(BaseTestCase):
    """AccountsController integration test stubs"""

    def test_accounts_post(self):
        """Test case for accounts_post

        Create an account
        """
        data = dict(username='username_example',
                    password='password_example',
                    name='name_example',
                    seller_id='seller_id_example')
        response = self.client.open(
            '/api/v1/accounts',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
