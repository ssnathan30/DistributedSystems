# buyer_client.BuyerActionsApi

All URIs are relative to *http://localhost/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**purchase_history_get**](BuyerActionsApi.md#purchase_history_get) | **GET** /purchase_history | Get purchase history
[**purchase_post**](BuyerActionsApi.md#purchase_post) | **POST** /purchase | Purchase items added in the cart
[**search_items_get**](BuyerActionsApi.md#search_items_get) | **GET** /search-items | Search for items
[**seller_feedback_post**](BuyerActionsApi.md#seller_feedback_post) | **POST** /seller_feedback | Provide seller Feedback
[**seller_rating_get**](BuyerActionsApi.md#seller_rating_get) | **GET** /seller_rating | Get seller rating


# **purchase_history_get**
> InlineResponse2004 purchase_history_get(buyer_id)

Get purchase history

### Example
```python
from __future__ import print_function
import time
import buyer_client
from buyer_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = buyer_client.BuyerActionsApi()
buyer_id = 56 # int | 

try:
    # Get purchase history
    api_response = api_instance.purchase_history_get(buyer_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuyerActionsApi->purchase_history_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **buyer_id** | **int**|  | 

### Return type

[**InlineResponse2004**](InlineResponse2004.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **purchase_post**
> InlineResponse2001 purchase_post(buyer_id, card_details)

Purchase items added in the cart

### Example
```python
from __future__ import print_function
import time
import buyer_client
from buyer_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = buyer_client.BuyerActionsApi()
buyer_id = 56 # int | 
card_details = buyer_client.CardDetails() # CardDetails | 

try:
    # Purchase items added in the cart
    api_response = api_instance.purchase_post(buyer_id, card_details)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuyerActionsApi->purchase_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **buyer_id** | **int**|  | 
 **card_details** | [**CardDetails**](CardDetails.md)|  | 

### Return type

[**InlineResponse2001**](InlineResponse2001.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_items_get**
> InlineResponse200 search_items_get(item_category, keywords, buyer_id)

Search for items

### Example
```python
from __future__ import print_function
import time
import buyer_client
from buyer_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = buyer_client.BuyerActionsApi()
item_category = 56 # int | 
keywords = 'keywords_example' # str | 
buyer_id = 56 # int | 

try:
    # Search for items
    api_response = api_instance.search_items_get(item_category, keywords, buyer_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuyerActionsApi->search_items_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **item_category** | **int**|  | 
 **keywords** | **str**|  | 
 **buyer_id** | **int**|  | 

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **seller_feedback_post**
> InlineResponse2003 seller_feedback_post(seller_id, buyer_id, transaction_id)

Provide seller Feedback

### Example
```python
from __future__ import print_function
import time
import buyer_client
from buyer_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = buyer_client.BuyerActionsApi()
seller_id = 56 # int | 
buyer_id = 56 # int | 
transaction_id = 'transaction_id_example' # str | 

try:
    # Provide seller Feedback
    api_response = api_instance.seller_feedback_post(seller_id, buyer_id, transaction_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuyerActionsApi->seller_feedback_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **seller_id** | **int**|  | 
 **buyer_id** | **int**|  | 
 **transaction_id** | **str**|  | 

### Return type

[**InlineResponse2003**](InlineResponse2003.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **seller_rating_get**
> InlineResponse2002 seller_rating_get(seller_id, buyer_id)

Get seller rating

### Example
```python
from __future__ import print_function
import time
import buyer_client
from buyer_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = buyer_client.BuyerActionsApi()
seller_id = 56 # int | 
buyer_id = 56 # int | 

try:
    # Get seller rating
    api_response = api_instance.seller_rating_get(seller_id, buyer_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BuyerActionsApi->seller_rating_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **seller_id** | **int**|  | 
 **buyer_id** | **int**|  | 

### Return type

[**InlineResponse2002**](InlineResponse2002.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

