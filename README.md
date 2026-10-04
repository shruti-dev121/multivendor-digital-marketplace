# Multi-Vendor Digital Marketplace

A web-based digital marketplace built with Django where users can register, create and manage digital products, purchase products securely, and track their orders. The platform also provides seller-side sales and earnings information.

## Features

* User registration and authentication
* Login and logout functionality
* Product creation, editing, and deletion
* Product details and product listing
* Seller dashboard
* Customer purchase history
* Order management
* Razorpay payment integration
* Payment verification
* Sales tracking
* Total orders and earnings calculation for sellers
* Product sales statistics
* Responsive user interface
* PostgreSQL/MySQL/SQLite database support depending on configuration

## Technology Stack

### Backend

* Python
* Django

### Frontend

* Django Templates
* HTML
* Tailwind CSS
* JavaScript

### Database

* SQLite for development
* PostgreSQL/MySQL can be configured for deployment

### Payment Gateway

* Razorpay

### Tools

* Git
* GitHub
* VS Code

## Project Workflow

### Customer

1. Register or log in.
2. Browse available digital products.
3. Open a product and view its details.
4. Purchase the product using Razorpay.
5. After successful payment, the order is recorded.
6. View previously purchased products in Purchase History.

### Seller

1. Log in to the platform.
2. Create and manage digital products.
3. View products created by the seller.
4. Track customer orders for their products.
5. View total orders and total earnings.
6. Monitor product sales.

## Payment Flow

The project uses Razorpay for online payments.

1. Customer selects a product.
2. Django creates a Razorpay order.
3. Customer completes the payment.
4. Razorpay returns the payment information.
5. Django verifies the payment signature.
6. The order is marked as paid.
7. Product sales information is updated.
8. The purchase appears in the customer's purchase history.
9. The seller's order and earnings statistics are updated.

## Project Structure

multivendor_digital/
│
├── mysite/
│   ├── manage.py
│   │
│   ├── mysite/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── myapp/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   └── templates/
│
├── requirements.txt
├── .gitignore
└── README.md


## Installation and Setup

### 1. Clone the repository

git clone https://github.com/shruti-dev121/multivendor-digital-marketplace.git

### 2. Navigate to the project

cd multivendor-digital-marketplace

### 3. Create a virtual environment

python -m venv env

### 4. Activate the virtual environment

#### Windows

env\Scripts\activate


### 5. Install dependencies

pip install -r requirements.txt

### 6. Configure environment variables

Create a `.env` file and add your payment gateway credentials:


RAZORPAY_KEY_ID=your_razorpay_key
RAZORPAY_KEY_SECRET=your_razorpay_secret


Do not commit the `.env` file to GitHub.

### 7. Run migrations


python manage.py migrate

### 8. Start the development server


python manage.py runserver


Open the application at:


http://127.0.0.1:8000/


## Security

Sensitive credentials such as Razorpay API keys are stored using environment variables and are not included in the GitHub repository.

The `.env` file is included in `.gitignore` to prevent accidental exposure of secret credentials.

## Future Improvements

* Multiple seller/user roles with improved permissions
* Digital product download management
* Email notifications for orders
* Product reviews and ratings
* Search and filtering
* Wishlist functionality
* Admin analytics dashboard
* Cloud storage for digital products
* Production deployment

## Author

Shruti0
<img width="1891" height="855" alt="image" src="https://github.com/user-attachments/assets/c8176484-4453-4d78-8ff8-915a257e2f40" />

<img width="1859" height="851" alt="image" src="https://github.com/user-attachments/assets/e8732dc9-888a-42db-bf85-f0ab3e0f1f66" />

<img width="1874" height="857" alt="image" src="https://github.com/user-attachments/assets/0c4172c7-ff13-40cb-bd89-c4ed82b43996" />

<img width="1789" height="880" alt="image" src="https://github.com/user-attachments/assets/880cc3b2-ee4f-4837-a59d-15e46b3dc1a5" />

<img width="1860" height="823" alt="image" src="https://github.com/user-attachments/assets/b756ff4d-584b-41e7-b85b-a77339633841" />

<img width="1878" height="849" alt="image" src="https://github.com/user-attachments/assets/3e76419d-d612-465c-bdb1-a067ef9e9ce4" />

<img width="1850" height="936" alt="image" src="https://github.com/user-attachments/assets/94063e1f-2f4e-4003-81f9-54f03527829b" />





GitHub: [shruti-dev121](https://github.com/shruti-dev121)
