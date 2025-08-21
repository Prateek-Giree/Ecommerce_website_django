# Ecommerce_website_django

An Ecommerce website built with Django that allows customers to browse products, add them to the cart, and place orders securely. The project includes features like user authentication, admin/vendor management, and payment integration. This project demonstrates building a fully functional ecommerce platform with Django,

## Features

1. **User Management**

    * Registration, login, and profile management

    * Multiple roles: Admin and Customer

2. Product Management

    * Add, update, and delete products

    *   Products organized by categories

    *   Product images and multiple price options (original & discounted)

3. **Shopping Cart & Wishlist**

    * Add/remove products from the cart

    * Quantity updates with dynamic subtotal/total calculation

    * Wishlist feature to save favorite products

4. **Checkout & Orders**

    * Delivery address management

    * Order creation and order status tracking (Pending → Packed → Delivered)

5. **Payments**

    * Integrated with eSewa (Nepali payment gateways)

    * Extendable to Stripe/PayPal

6. **Admin Panel**

    * Full control to manage users, vendors, products, and orders

    * Vendor approval workflow

7. **Search & Filtering**

    * Search by product name/category

    * Filtering options for better product discovery

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Installation

Follow these steps to install and set up the project:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Prateek-Giree/Ecommerce_website_django.git
    ```
2. Create and activate a virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate  # On Linux/macOS
    env\Scripts\activate  # On Windows
3. Install Dependencies
    ``` bash
    pip install -r requirements.txt
    ```

4.  **Set up the database:**

    Update settings.py with your database configuration.
    
    Run migrations:
    ``` bash
    python manage.py makemigrations
    python manage.py migrate
    ```
5. **Create a superuser:**
    ```bash 
    python manage.py createsuperuser
    ```
6. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

## Usage

1.  **Accessing the Admin Panel:**

    *   Navigate to `http://127.0.0.1:8000/admin-dashboard/` in your browser.
    *   Log in with the superuser credentials created during installation.

2.  **User Registration and Login:**

    * New users can sign up using the registration page.

    * Existing users can log in to manage their profile, orders, and wishlist.

3.  **Browsing Products:**

    * Products are organized by categories.

    *  Users can search for products and view product details before adding them to the cart.

4.  **Adding Products to Cart and Checkout:**
    * Users can add multiple products to their cart.

    * Cart items are updated dynamically with quantity and subtotal.

    * At checkout, users provide delivery address and complete payment (supports eSewa).

## Configuration

1.  **Settings File (`settings.py`):**

    Update DATABASES for your local database (e.g., PostgreSQL, MySQL, SQLite).

2.  **Environment Variables:**

    Use python-dotenv or OS environment variables for sensitive data.

    ```bash 
        Install python-dotenv:
    ```
    * Example usage:
    ```bash
    SECRET_KEY=your-secret-key
    DATABASE_URL=postgres://user:password@localhost:5432/ecommerce
    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER=example@gmail.com
    EMAIL_HOST_PASSWORD= <your app password for gmail>
    ```
    
## Contributing

> Guidelines for developers who want to contribute to the project.

1.  **Branching Strategy:**

    Use feature branches for new changes:

    * feature/add-cart-functionality

    * bugfix/fix-checkout-issue


3.  **Pull Request Procedure:**

    * Write clear commit messages.

    * Add documentation and tests for new features.

    * Submit pull requests to the main branch.


4.  **Setting up a development environment**
    
    * Follow steps in Installation
    * Run tests with:
        ``` bash
        python manage.py test
        ```
## License

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.


