# coding: utf-8

"""
    Seller API

    API for managing seller accounts and items for sale  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from seller_client.api_client import ApiClient


class AccountsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def accounts_post(self, username, password, seller_id, **kwargs):  # noqa: E501
        """Create an account  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.accounts_post(username, password, seller_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str username: (required)
        :param str password: (required)
        :param str seller_id: (required)
        :param str name:
        :return: InlineResponse200
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.accounts_post_with_http_info(username, password, seller_id, **kwargs)  # noqa: E501
        else:
            (data) = self.accounts_post_with_http_info(username, password, seller_id, **kwargs)  # noqa: E501
            return data

    def accounts_post_with_http_info(self, username, password, seller_id, **kwargs):  # noqa: E501
        """Create an account  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.accounts_post_with_http_info(username, password, seller_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str username: (required)
        :param str password: (required)
        :param str seller_id: (required)
        :param str name:
        :return: InlineResponse200
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['username', 'password', 'seller_id', 'name']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method accounts_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'username' is set
        if self.api_client.client_side_validation and ('username' not in params or
                                                       params['username'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `username` when calling `accounts_post`")  # noqa: E501
        # verify the required parameter 'password' is set
        if self.api_client.client_side_validation and ('password' not in params or
                                                       params['password'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `password` when calling `accounts_post`")  # noqa: E501
        # verify the required parameter 'seller_id' is set
        if self.api_client.client_side_validation and ('seller_id' not in params or
                                                       params['seller_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `seller_id` when calling `accounts_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'username' in params:
            form_params.append(('username', params['username']))  # noqa: E501
        if 'password' in params:
            form_params.append(('password', params['password']))  # noqa: E501
        if 'name' in params:
            form_params.append(('name', params['name']))  # noqa: E501
        if 'seller_id' in params:
            form_params.append(('seller_id', params['seller_id']))  # noqa: E501

        body_params = None
        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/accounts', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse200',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
