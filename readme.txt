-Get all products :
URL : products/  
Authentication : None  
Options : GET  
Response example : {  
{
"name":"Asus",  
"price":2000,  
"category":{"name":"Laptop"},  
"condition":true,  
"image":"/media/<image_name>",  
"description":"...",  
"extra_details":"...",  
"token":"P-2645591"  
} }

-Detail of one product :
URL : products/<product_token>/  
Authentication : None  
Options : GET  
Response example :
{  
"name":"Asus",  
"price":2000,  
"category":{"name":"Laptop"},  
"condition":true,  
"image":"/media/<image_name>",  
"description":"...",  
"extra_details":"...",  
"token":"P-2645591"  
}

-List of all categories :
URL : categories/  
Authentication : None  
Options : Get  
Response example :  
[ {"name":"Laptop"}, {"name" : "Phone"} ]


-Get products of one category:
URL : categories/<category_name>/  
Authentication : None  
Options : GET  

-Get authentication token:
URL : token/  
Authentication : None  
Options : POST  
Body : {"username" : username , "password" : <password>}  
Response example :   
{"token":"12c31f12e83d06ac750182adf3f57481423f93e8"}  

-Add a product to cart:
Authentication : TokenAuthentication, SessionAuthentication    
URL : add_to_cart/  
Options : POST  
Body : {"product_token" : "token of the product"}  
Headers : {"Authorization" : "Token <user token>"}


-View and make orders :
Authentication : TokenAuthentication, SessionAuthentication  
URL : order/
Options : POST, GET  
Body :   
{  
"city" : "city",   
"address" : "address",  
"number" : "phone number"  
}  
Headers : {"Authorization" : "Token <user token>"}
Response example :
[
    {
        "user": {
            "username": "example",
            "email": "example@gmail.com"
        },
        "address": "...",
        "number": 9301234567,
        "city": "...",
        "cart": [
            {
                "product": {
                    "name": "Laptop",
                    "token": "P-4512354"
                },
                "quantity": 3
            }
        ],
        "date": "2025-05-20T07:39:39.261056Z"
    },
    {
        "user": {
            "username": "example",
            "email": "example.gmail.com"
        },
        "address": "...",
        "number": 9301234567,
        "city": "...",
        "cart": [
            {
                "product": {
                    "name": "Airbuds",
                    "token": "P-2645591"
                },
                "quantity": 2
            }
        ],
        "date": "2025-05-20T07:40:15.739774Z"
    }
]
