Get all products:  
url : products/  
Authentication : None  
options : GET  
Response example : {  
{  
"id":1,  
"category":{"name":"Laptop"},  
"name":"Asus",  
"price":2000,  
"condition":true,  
"image":"/media/<image_name>",  
"description":"...",  
"extra_details":"...",  
"token":"P-2645591"  
} }

Detail of one product:  
url : products/<product_token>/  
Authentication : None  
options : GET  
Response example :
{  
"id":1,  
"category":{"name":"Laptop"},  
"name":"Asus",  
"price":2000,  
"condition":true,  
"image":"/media/<image_name>",  
"description":"...",  
"extra_details":"...",  
"token":"P-2645591"  
}

List of all categories :  
url : categories/  
Authentication : None  
Options : Get  

Get products of one category:  
url : categories/<category_name>/  
Authentication : None  
options : GET  

Get authentication token:  
url : token/  
Authentication : None  
options : POST  
body : {"username" : username , "password" : <password>}  

Add a product to cart:  
Authentication : TokenAuthentication  
url : add_to_cart/  
Options: POST  
body : {"product_name" : "name of the product"}  
Headers : {"Authorization" : "Token <user token>"}


