# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from seller_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from seller_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from seller_server.models.inline_response400 import InlineResponse400  # noqa: E501
from seller_server.models.inline_response401 import InlineResponse401  # noqa: E501
from seller_server.models.inline_response5001 import InlineResponse5001  # noqa: E501
from seller_server.models.inline_response5002 import InlineResponse5002  # noqa: E501
from seller_server.test import BaseTestCase


class TestAuthenticationController(BaseTestCase):
    """AuthenticationController integration test stubs"""

    def test_login_post(self):
        """Test case for login_post

        Login
        """
        data = dict(username='username_example',
                    password='password_example')
        response = self.client.open(
            '/api/v1/login',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_logout_post(self):
        """Test case for logout_post

        Logout
        """
        data = dict(seller_id='seller_id_example')
        response = self.client.open(
            '/api/v1/logout',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
