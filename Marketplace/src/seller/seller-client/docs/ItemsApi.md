# seller_client.ItemsApi

All URIs are relative to *https://localhost/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**display_get**](ItemsApi.md#display_get) | **GET** /display | Display items
[**items_item_id_delete**](ItemsApi.md#items_item_id_delete) | **DELETE** /items/{item_id}/delete | Remove an item from sale
[**items_item_id_sale_price_put**](ItemsApi.md#items_item_id_sale_price_put) | **PUT** /items/{item_id}/sale_price | Change the sale price of an item
[**items_post**](ItemsApi.md#items_post) | **POST** /items | Put an item for sale


# **display_get**
> InlineResponse2007 display_get(seller_id)

Display items

### Example
```python
from __future__ import print_function
import time
import seller_client
from seller_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = seller_client.ItemsApi()
seller_id = 'seller_id_example' # str | 

try:
    # Display items
    api_response = api_instance.display_get(seller_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ItemsApi->display_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **seller_id** | **str**|  | 

### Return type

[**InlineResponse2007**](InlineResponse2007.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **items_item_id_delete**
> InlineResponse2005 items_item_id_delete(item_id, quantity, seller_id)

Remove an item from sale

### Example
```python
from __future__ import print_function
import time
import seller_client
from seller_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = seller_client.ItemsApi()
item_id = 56 # int | 
quantity = 56 # int | 
seller_id = 'seller_id_example' # str | 

try:
    # Remove an item from sale
    api_response = api_instance.items_item_id_delete(item_id, quantity, seller_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ItemsApi->items_item_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **item_id** | **int**|  | 
 **quantity** | **int**|  | 
 **seller_id** | **str**|  | 

### Return type

[**InlineResponse2005**](InlineResponse2005.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **items_item_id_sale_price_put**
> InlineResponse2004 items_item_id_sale_price_put(item_id, new_sale_price, seller_id)

Change the sale price of an item

### Example
```python
from __future__ import print_function
import time
import seller_client
from seller_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = seller_client.ItemsApi()
item_id = 'item_id_example' # str | 
new_sale_price = 3.4 # float | 
seller_id = 'seller_id_example' # str | 

try:
    # Change the sale price of an item
    api_response = api_instance.items_item_id_sale_price_put(item_id, new_sale_price, seller_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ItemsApi->items_item_id_sale_price_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **item_id** | **str**|  | 
 **new_sale_price** | **float**|  | 
 **seller_id** | **str**|  | 

### Return type

[**InlineResponse2004**](InlineResponse2004.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **items_post**
> InlineResponse201 items_post(item_id, item_name, item_category, keywords, condition, sale_price, quantity, seller_id)

Put an item for sale

### Example
```python
from __future__ import print_function
import time
import seller_client
from seller_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = seller_client.ItemsApi()
item_id = 'item_id_example' # str | 
item_name = 'item_name_example' # str | 
item_category = 'item_category_example' # str | 
keywords = ['keywords_example'] # list[str] | 
condition = 'condition_example' # str | 
sale_price = 3.4 # float | 
quantity = 56 # int | 
seller_id = 'seller_id_example' # str | 

try:
    # Put an item for sale
    api_response = api_instance.items_post(item_id, item_name, item_category, keywords, condition, sale_price, quantity, seller_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ItemsApi->items_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **item_id** | **str**|  | 
 **item_name** | **str**|  | 
 **item_category** | **str**|  | 
 **keywords** | [**list[str]**](str.md)|  | 
 **condition** | **str**|  | 
 **sale_price** | **float**|  | 
 **quantity** | **int**|  | 
 **seller_id** | **str**|  | 

### Return type

[**InlineResponse201**](InlineResponse201.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

