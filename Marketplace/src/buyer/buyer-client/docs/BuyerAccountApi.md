# buyer_client.BuyerAccountApi

All URIs are relative to *http://localhost/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**account_post**](BuyerAccountApi.md#account_post) | **POST** /account | Create a new buyer account
[**login_post**](BuyerAccountApi.md#login_post) | **POST** /login | Log in to an existing account
[**logout_buyer_id_get**](BuyerAccountApi.md#logout_buyer_id_get) | **GET** /logout/{buyer_id} | Log out of an existing account


# **account_post**
> InlineResponse201 account_post(account)

Create a new buyer account

### Example
```python
from __future__ import print_function
import time
import buyer_client
from buyer_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = buyer_client.BuyerAccountApi()
account = buyer_client.Account() # Account | 

try:
    # Create a new buyer account
    api_response = api_instance.account_post(account)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuyerAccountApi->account_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **account** | [**Account**](Account.md)|  | 

### Return type

[**InlineResponse201**](InlineResponse201.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **login_post**
> InlineResponse2005 login_post(credentials)

Log in to an existing account

### Example
```python
from __future__ import print_function
import time
import buyer_client
from buyer_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = buyer_client.BuyerAccountApi()
credentials = buyer_client.Credentials() # Credentials | 

try:
    # Log in to an existing account
    api_response = api_instance.login_post(credentials)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuyerAccountApi->login_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **credentials** | [**Credentials**](Credentials.md)|  | 

### Return type

[**InlineResponse2005**](InlineResponse2005.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **logout_buyer_id_get**
> InlineResponse2006 logout_buyer_id_get(buyer_id)

Log out of an existing account

### Example
```python
from __future__ import print_function
import time
import buyer_client
from buyer_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = buyer_client.BuyerAccountApi()
buyer_id = 56 # int | 

try:
    # Log out of an existing account
    api_response = api_instance.logout_buyer_id_get(buyer_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuyerAccountApi->logout_buyer_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **buyer_id** | **int**|  | 

### Return type

[**InlineResponse2006**](InlineResponse2006.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

