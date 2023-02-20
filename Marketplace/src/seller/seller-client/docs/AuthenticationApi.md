# seller_client.AuthenticationApi

All URIs are relative to *https://localhost/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**login_post**](AuthenticationApi.md#login_post) | **POST** /login | Login
[**logout_post**](AuthenticationApi.md#logout_post) | **POST** /logout | Logout


# **login_post**
> InlineResponse2001 login_post(username, password)

Login

### Example
```python
from __future__ import print_function
import time
import seller_client
from seller_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = seller_client.AuthenticationApi()
username = 'username_example' # str | 
password = 'password_example' # str | 

try:
    # Login
    api_response = api_instance.login_post(username, password)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuthenticationApi->login_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **str**|  | 
 **password** | **str**|  | 

### Return type

[**InlineResponse2001**](InlineResponse2001.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **logout_post**
> InlineResponse2002 logout_post(seller_id)

Logout

### Example
```python
from __future__ import print_function
import time
import seller_client
from seller_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = seller_client.AuthenticationApi()
seller_id = 'seller_id_example' # str | 

try:
    # Logout
    api_response = api_instance.logout_post(seller_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuthenticationApi->logout_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **seller_id** | **str**|  | 

### Return type

[**InlineResponse2002**](InlineResponse2002.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

