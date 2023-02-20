# seller_client.AccountsApi

All URIs are relative to *https://localhost/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**accounts_post**](AccountsApi.md#accounts_post) | **POST** /accounts | Create an account


# **accounts_post**
> InlineResponse200 accounts_post(username, password, seller_id, name=name)

Create an account

### Example
```python
from __future__ import print_function
import time
import seller_client
from seller_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = seller_client.AccountsApi()
username = 'username_example' # str | 
password = 'password_example' # str | 
seller_id = 'seller_id_example' # str | 
name = 'name_example' # str |  (optional)

try:
    # Create an account
    api_response = api_instance.accounts_post(username, password, seller_id, name=name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountsApi->accounts_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **str**|  | 
 **password** | **str**|  | 
 **seller_id** | **str**|  | 
 **name** | **str**|  | [optional] 

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

