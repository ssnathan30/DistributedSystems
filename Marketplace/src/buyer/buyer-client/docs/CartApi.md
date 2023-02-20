# buyer_client.CartApi

All URIs are relative to *http://localhost/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cart_add_post**](CartApi.md#cart_add_post) | **POST** /cart/add | Add item to shopping cart
[**cart_remove_delete**](CartApi.md#cart_remove_delete) | **DELETE** /cart/remove | Remove item from shopping cart
[**clear_cart_post**](CartApi.md#clear_cart_post) | **POST** /clear-cart | Clear the shopping cart for a given buyer
[**display_cart_get**](CartApi.md#display_cart_get) | **GET** /display-cart | Get the contents of the shopping cart for a given buyer


# **cart_add_post**
> cart_add_post(body)

Add item to shopping cart

Adds an item to the shopping cart of a buyer

### Example
```python
from __future__ import print_function
import time
import buyer_client
from buyer_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = buyer_client.CartApi()
body = buyer_client.Body() # Body | Item ID and quantity to be added to cart

try:
    # Add item to shopping cart
    api_instance.cart_add_post(body)
except ApiException as e:
    print("Exception when calling CartApi->cart_add_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Body**](Body.md)| Item ID and quantity to be added to cart | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **cart_remove_delete**
> cart_remove_delete(item_id, quantity, buyer_id)

Remove item from shopping cart

Removes an item from the shopping cart of a buyer

### Example
```python
from __future__ import print_function
import time
import buyer_client
from buyer_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = buyer_client.CartApi()
item_id = 789 # int | ID of the item to be removed from the cart
quantity = 56 # int | Quantity of the item to be removed from the cart
buyer_id = 789 # int | ID of the buyer whose cart the item should be removed from

try:
    # Remove item from shopping cart
    api_instance.cart_remove_delete(item_id, quantity, buyer_id)
except ApiException as e:
    print("Exception when calling CartApi->cart_remove_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **item_id** | **int**| ID of the item to be removed from the cart | 
 **quantity** | **int**| Quantity of the item to be removed from the cart | 
 **buyer_id** | **int**| ID of the buyer whose cart the item should be removed from | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clear_cart_post**
> clear_cart_post(buyer_id)

Clear the shopping cart for a given buyer

### Example
```python
from __future__ import print_function
import time
import buyer_client
from buyer_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = buyer_client.CartApi()
buyer_id = 56 # int | ID of the buyer whose shopping cart should be cleared

try:
    # Clear the shopping cart for a given buyer
    api_instance.clear_cart_post(buyer_id)
except ApiException as e:
    print("Exception when calling CartApi->clear_cart_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **buyer_id** | **int**| ID of the buyer whose shopping cart should be cleared | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **display_cart_get**
> InlineResponse2007 display_cart_get(buyer_id)

Get the contents of the shopping cart for a given buyer

### Example
```python
from __future__ import print_function
import time
import buyer_client
from buyer_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = buyer_client.CartApi()
buyer_id = 56 # int | ID of the buyer whose shopping cart should be displayed

try:
    # Get the contents of the shopping cart for a given buyer
    api_response = api_instance.display_cart_get(buyer_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CartApi->display_cart_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **buyer_id** | **int**| ID of the buyer whose shopping cart should be displayed | 

### Return type

[**InlineResponse2007**](InlineResponse2007.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

