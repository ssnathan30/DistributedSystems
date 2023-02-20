# seller_client.SellersApi

All URIs are relative to *https://localhost/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**seller_rating_get**](SellersApi.md#seller_rating_get) | **GET** /seller/rating | Get seller rating


# **seller_rating_get**
> InlineResponse2003 seller_rating_get(seller_id)

Get seller rating

### Example
```python
from __future__ import print_function
import time
import seller_client
from seller_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = seller_client.SellersApi()
seller_id = 'seller_id_example' # str | 

try:
    # Get seller rating
    api_response = api_instance.seller_rating_get(seller_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SellersApi->seller_rating_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **seller_id** | **str**|  | 

### Return type

[**InlineResponse2003**](InlineResponse2003.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

