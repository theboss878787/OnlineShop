# 🛍️ Online Shop API

A Django-based RESTful API for an online shopping platform. It supports product browsing, category filtering, authentication, cart operations, and order submission.

---

## 🚀 Getting Started

### 🧰 Requirements

- Python 3.9+
- pip
- Virtualenv (recommended)
- Django & Django REST framework

### ⚙️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/mohamadrezabjr/Online_Shop.git
cd Online_Shop

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your database in settings.py or use a .env file

# 5. Apply migrations
python manage.py migrate

# 6. Create superuser (for admin access)
python manage.py createsuperuser

# 7. Run development server
python manage.py runserver
```

---

## 🔌 API Endpoints

### 📦 Get All Products
- **URL**: `/products/`
- **Method**: `GET`
- **Authentication**: None

#### ✅ Response:
```json
{
  "name": "Asus",
  "price": 2000,
  "category": {"name": "Laptop"},
  "condition": true,
  "image": "/media/<image_name>",
  "description": "...",
  "extra_details": "...",
  "token": "P-2645591"
  
}
```

---

### 🔍 Get Product Details
- **URL**: `/products/<product_token>/`
- **Method**: `GET`
- **Authentication**: None

#### ✅ Response:
```json
{
  "name": "Asus",
  "price": 2000,
  "category": {"name": "Laptop"},
  "condition": true,
  "image": "/media/<image_name>",
  "description": "...",
  "extra_details": "...",
  "token": "P-2645591"
}
```

---

### 🗂️ Get All Categories
- **URL**: `/categories/`
- **Method**: `GET`
- **Authentication**: None

#### ✅ Response:
```json
[
  {"name": "Laptop"},
  {"name": "Phone"}
]
```

---

### 🧾 Get Products by Category
- **URL**: `/categories/<category_name>/`
- **Method**: `GET`
- **Authentication**: None

---

### 🔐 Register
- **URL**: `/register/`
- **Method**: `POST`
- **Authentication**: None

#### 📨 Request Body:
```json
{
  "username": "your_username",
  "password": "your_password",
  "email": "your_email"
}
```
### 🔐 Get Auth Token
- **URL**: `/token/`
- **Method**: `POST`
- **Authentication**: None

#### 📨 Request Body:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

#### ✅ Response:
```json
{
  "token": "12c31f12e83d06ac750182adf3f57481423f93e8"
}
```

---

### ➕ Add Product to Cart
- **URL**: `/add_to_cart/`
- **Method**: `POST`
- **Authentication**: Token / Session

#### 📨 Request Body:
```json
{
  "product_token": "P-2645591"
}
```

#### 🧾 Headers:
```http
Authorization: Token <user_token>
```

---

### 🧾 View and Submit Orders
- **URL**: `/order/`
- **Methods**: `GET`, `POST`
- **Authentication**: Token / Session

#### 📨 POST Body:
```json
{
  "city": "Tehran",
  "address": "Example Street",
  "number": "09121234567"
}
```

#### ✅ GET Response:
```json
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
```

---
### ➕ Make review
- **URL**: `/review/`
- **Method**: `POST`
- **Authentication**: Token / Session

#### 📨 Request Body:
```json
{
  "product_token" : "P-2645591",
  "review" : "some text",
  "star" : "1 to 5"
}
```

#### 🧾 Headers:
```http
Authorization: Token <user_token>
```

---


> ⚠️ Make sure to send the `Authorization` header when required.