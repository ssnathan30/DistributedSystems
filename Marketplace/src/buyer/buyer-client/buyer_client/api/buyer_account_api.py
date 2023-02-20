# coding: utf-8

"""
    Buyer Account API

    API for creating and managing buyer accounts  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from buyer_client.api_client import ApiClient


class BuyerAccountApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def account_post(self, account, **kwargs):  # noqa: E501
        """Create a new buyer account  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.account_post(account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param Account account: (required)
        :return: InlineResponse201
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.account_post_with_http_info(account, **kwargs)  # noqa: E501
        else:
            (data) = self.account_post_with_http_info(account, **kwargs)  # noqa: E501
            return data

    def account_post_with_http_info(self, account, **kwargs):  # noqa: E501
        """Create a new buyer account  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.account_post_with_http_info(account, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param Account account: (required)
        :return: InlineResponse201
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method account_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'account' is set
        if self.api_client.client_side_validation and ('account' not in params or
                                                       params['account'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `account` when calling `account_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'account' in params:
            body_params = params['account']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/account', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse201',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def login_post(self, credentials, **kwargs):  # noqa: E501
        """Log in to an existing account  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.login_post(credentials, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param Credentials credentials: (required)
        :return: InlineResponse2005
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.login_post_with_http_info(credentials, **kwargs)  # noqa: E501
        else:
            (data) = self.login_post_with_http_info(credentials, **kwargs)  # noqa: E501
            return data

    def login_post_with_http_info(self, credentials, **kwargs):  # noqa: E501
        """Log in to an existing account  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.login_post_with_http_info(credentials, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param Credentials credentials: (required)
        :return: InlineResponse2005
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['credentials']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method login_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'credentials' is set
        if self.api_client.client_side_validation and ('credentials' not in params or
                                                       params['credentials'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `credentials` when calling `login_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'credentials' in params:
            body_params = params['credentials']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/login', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse2005',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def logout_buyer_id_get(self, buyer_id, **kwargs):  # noqa: E501
        """Log out of an existing account  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.logout_buyer_id_get(buyer_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int buyer_id: (required)
        :return: InlineResponse2006
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.logout_buyer_id_get_with_http_info(buyer_id, **kwargs)  # noqa: E501
        else:
            (data) = self.logout_buyer_id_get_with_http_info(buyer_id, **kwargs)  # noqa: E501
            return data

    def logout_buyer_id_get_with_http_info(self, buyer_id, **kwargs):  # noqa: E501
        """Log out of an existing account  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.logout_buyer_id_get_with_http_info(buyer_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int buyer_id: (required)
        :return: InlineResponse2006
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['buyer_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method logout_buyer_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'buyer_id' is set
        if self.api_client.client_side_validation and ('buyer_id' not in params or
                                                       params['buyer_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `buyer_id` when calling `logout_buyer_id_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'buyer_id' in params:
            path_params['buyer_id'] = params['buyer_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/logout/{buyer_id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse2006',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
