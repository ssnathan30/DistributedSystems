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


class ItemsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def display_get(self, seller_id, **kwargs):  # noqa: E501
        """Display items  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.display_get(seller_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str seller_id: (required)
        :return: InlineResponse2007
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.display_get_with_http_info(seller_id, **kwargs)  # noqa: E501
        else:
            (data) = self.display_get_with_http_info(seller_id, **kwargs)  # noqa: E501
            return data

    def display_get_with_http_info(self, seller_id, **kwargs):  # noqa: E501
        """Display items  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.display_get_with_http_info(seller_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str seller_id: (required)
        :return: InlineResponse2007
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['seller_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method display_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'seller_id' is set
        if self.api_client.client_side_validation and ('seller_id' not in params or
                                                       params['seller_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `seller_id` when calling `display_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'seller_id' in params:
            query_params.append(('seller_id', params['seller_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/display', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse2007',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def items_item_id_delete(self, item_id, quantity, seller_id, **kwargs):  # noqa: E501
        """Remove an item from sale  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.items_item_id_delete(item_id, quantity, seller_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int item_id: (required)
        :param int quantity: (required)
        :param str seller_id: (required)
        :return: InlineResponse2005
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.items_item_id_delete_with_http_info(item_id, quantity, seller_id, **kwargs)  # noqa: E501
        else:
            (data) = self.items_item_id_delete_with_http_info(item_id, quantity, seller_id, **kwargs)  # noqa: E501
            return data

    def items_item_id_delete_with_http_info(self, item_id, quantity, seller_id, **kwargs):  # noqa: E501
        """Remove an item from sale  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.items_item_id_delete_with_http_info(item_id, quantity, seller_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int item_id: (required)
        :param int quantity: (required)
        :param str seller_id: (required)
        :return: InlineResponse2005
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['item_id', 'quantity', 'seller_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method items_item_id_delete" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'item_id' is set
        if self.api_client.client_side_validation and ('item_id' not in params or
                                                       params['item_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `item_id` when calling `items_item_id_delete`")  # noqa: E501
        # verify the required parameter 'quantity' is set
        if self.api_client.client_side_validation and ('quantity' not in params or
                                                       params['quantity'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `quantity` when calling `items_item_id_delete`")  # noqa: E501
        # verify the required parameter 'seller_id' is set
        if self.api_client.client_side_validation and ('seller_id' not in params or
                                                       params['seller_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `seller_id` when calling `items_item_id_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'item_id' in params:
            path_params['item_id'] = params['item_id']  # noqa: E501

        query_params = []
        if 'quantity' in params:
            query_params.append(('quantity', params['quantity']))  # noqa: E501
        if 'seller_id' in params:
            query_params.append(('seller_id', params['seller_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/items/{item_id}/delete', 'DELETE',
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

    def items_item_id_sale_price_put(self, item_id, new_sale_price, seller_id, **kwargs):  # noqa: E501
        """Change the sale price of an item  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.items_item_id_sale_price_put(item_id, new_sale_price, seller_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str item_id: (required)
        :param float new_sale_price: (required)
        :param str seller_id: (required)
        :return: InlineResponse2004
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.items_item_id_sale_price_put_with_http_info(item_id, new_sale_price, seller_id, **kwargs)  # noqa: E501
        else:
            (data) = self.items_item_id_sale_price_put_with_http_info(item_id, new_sale_price, seller_id, **kwargs)  # noqa: E501
            return data

    def items_item_id_sale_price_put_with_http_info(self, item_id, new_sale_price, seller_id, **kwargs):  # noqa: E501
        """Change the sale price of an item  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.items_item_id_sale_price_put_with_http_info(item_id, new_sale_price, seller_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str item_id: (required)
        :param float new_sale_price: (required)
        :param str seller_id: (required)
        :return: InlineResponse2004
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['item_id', 'new_sale_price', 'seller_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method items_item_id_sale_price_put" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'item_id' is set
        if self.api_client.client_side_validation and ('item_id' not in params or
                                                       params['item_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `item_id` when calling `items_item_id_sale_price_put`")  # noqa: E501
        # verify the required parameter 'new_sale_price' is set
        if self.api_client.client_side_validation and ('new_sale_price' not in params or
                                                       params['new_sale_price'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `new_sale_price` when calling `items_item_id_sale_price_put`")  # noqa: E501
        # verify the required parameter 'seller_id' is set
        if self.api_client.client_side_validation and ('seller_id' not in params or
                                                       params['seller_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `seller_id` when calling `items_item_id_sale_price_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'item_id' in params:
            path_params['item_id'] = params['item_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'new_sale_price' in params:
            form_params.append(('new_sale_price', params['new_sale_price']))  # noqa: E501
        if 'seller_id' in params:
            form_params.append(('seller_id', params['seller_id']))  # noqa: E501

        body_params = None
        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/items/{item_id}/sale_price', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse2004',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def items_post(self, item_id, item_name, item_category, keywords, condition, sale_price, quantity, seller_id, **kwargs):  # noqa: E501
        """Put an item for sale  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.items_post(item_id, item_name, item_category, keywords, condition, sale_price, quantity, seller_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str item_id: (required)
        :param str item_name: (required)
        :param str item_category: (required)
        :param list[str] keywords: (required)
        :param str condition: (required)
        :param float sale_price: (required)
        :param int quantity: (required)
        :param str seller_id: (required)
        :return: InlineResponse201
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.items_post_with_http_info(item_id, item_name, item_category, keywords, condition, sale_price, quantity, seller_id, **kwargs)  # noqa: E501
        else:
            (data) = self.items_post_with_http_info(item_id, item_name, item_category, keywords, condition, sale_price, quantity, seller_id, **kwargs)  # noqa: E501
            return data

    def items_post_with_http_info(self, item_id, item_name, item_category, keywords, condition, sale_price, quantity, seller_id, **kwargs):  # noqa: E501
        """Put an item for sale  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.items_post_with_http_info(item_id, item_name, item_category, keywords, condition, sale_price, quantity, seller_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str item_id: (required)
        :param str item_name: (required)
        :param str item_category: (required)
        :param list[str] keywords: (required)
        :param str condition: (required)
        :param float sale_price: (required)
        :param int quantity: (required)
        :param str seller_id: (required)
        :return: InlineResponse201
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['item_id', 'item_name', 'item_category', 'keywords', 'condition', 'sale_price', 'quantity', 'seller_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method items_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'item_id' is set
        if self.api_client.client_side_validation and ('item_id' not in params or
                                                       params['item_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `item_id` when calling `items_post`")  # noqa: E501
        # verify the required parameter 'item_name' is set
        if self.api_client.client_side_validation and ('item_name' not in params or
                                                       params['item_name'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `item_name` when calling `items_post`")  # noqa: E501
        # verify the required parameter 'item_category' is set
        if self.api_client.client_side_validation and ('item_category' not in params or
                                                       params['item_category'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `item_category` when calling `items_post`")  # noqa: E501
        # verify the required parameter 'keywords' is set
        if self.api_client.client_side_validation and ('keywords' not in params or
                                                       params['keywords'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `keywords` when calling `items_post`")  # noqa: E501
        # verify the required parameter 'condition' is set
        if self.api_client.client_side_validation and ('condition' not in params or
                                                       params['condition'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `condition` when calling `items_post`")  # noqa: E501
        # verify the required parameter 'sale_price' is set
        if self.api_client.client_side_validation and ('sale_price' not in params or
                                                       params['sale_price'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `sale_price` when calling `items_post`")  # noqa: E501
        # verify the required parameter 'quantity' is set
        if self.api_client.client_side_validation and ('quantity' not in params or
                                                       params['quantity'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `quantity` when calling `items_post`")  # noqa: E501
        # verify the required parameter 'seller_id' is set
        if self.api_client.client_side_validation and ('seller_id' not in params or
                                                       params['seller_id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `seller_id` when calling `items_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'item_id' in params:
            form_params.append(('item_id', params['item_id']))  # noqa: E501
        if 'item_name' in params:
            form_params.append(('item_name', params['item_name']))  # noqa: E501
        if 'item_category' in params:
            form_params.append(('item_category', params['item_category']))  # noqa: E501
        if 'keywords' in params:
            form_params.append(('keywords', params['keywords']))  # noqa: E501
            collection_formats['keywords'] = 'multi'  # noqa: E501
        if 'condition' in params:
            form_params.append(('condition', params['condition']))  # noqa: E501
        if 'sale_price' in params:
            form_params.append(('sale_price', params['sale_price']))  # noqa: E501
        if 'quantity' in params:
            form_params.append(('quantity', params['quantity']))  # noqa: E501
        if 'seller_id' in params:
            form_params.append(('seller_id', params['seller_id']))  # noqa: E501

        body_params = None
        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/items', 'POST',
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
