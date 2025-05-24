# KK39 Candles - Handmade Eco-Friendly E-commerce Store

## Table of Contents
1.  [Project Description](#project-description)
2.  [Live Demo](#live-demo)
3.  [Features](#features)
4.  [Tech Stack](#tech-stack)
5.  [Prerequisites](#prerequisites)
6.  [Installation & Setup](#installation--setup)
    *   [Cloning the Repository](#cloning-the-repository)
    *   [Setting up the Virtual Environment](#setting-up-the-virtual-environment)
    *   [Installing Dependencies](#installing-dependencies)
    *   [Environment Variables (`env.py`)](#environment-variables-envpy)
    *   [Database Setup](#database-setup)
    *   [Running Migrations](#running-migrations)
    *   [Creating a Superuser](#creating-a-superuser)
    *   [Compiling Static Files](#compiling-static-files)
7.  [Running the Project Locally](#running-the-project-locally)
8.  [Deployment](#deployment)
9.  [Key Functionality Overview](#key-functionality-overview)
    *   [User Facing](#user-facing)
    *   [Admin Facing](#admin-facing)
10. [Known Issues](#known-issues)
11. [Future Development](#future-development)
12. [Credits & Acknowledgements](#credits--acknowledgements)
13. [License](#license)

---

## Project Description

KK39 Candles is a full-stack e-commerce web application built with Django, designed for a small business selling handmade, **eco-friendly**, and **organic candles**. The platform allows users to browse products, manage a shopping bag, complete secure purchases, review products, and manage their profiles. The site emphasizes high-quality ingredients, sustainability, and pet-friendly options (especially for unscented candles).

The project features a custom-styled frontend, integration with payment gateways like Stripe (including Google Pay and Apple Pay features) and PayPal, user authentication, an admin interface for site management, a blog, and a newsletter subscription feature integrated with Mailchimp.

---

## Live Demo

A live version of this project is deployed on Heroku and can be accessed here:
(https://kk39-candles-24591ccdc142.herokuapp.com/) 

---

## Features

*   **User Authentication:** Full registration, login, logout, password reset functionality (via `django-allauth`).
*   **Product Browsing:** View all products, filter by category, view individual product details.
*   **Product Search:** Users can search for products by name, description, and category.
*   **Shopping Bag:** Add, view, update quantities, and remove items from the shopping bag.
*   **Secure Checkout:** Multi-step checkout process with Stripe and PayPal integration for payments.
*   **User Profiles:** Registered users can view their order history and save delivery information.
*   **Product Reviews:** Users can rate and review products.
*   **Admin Interface:** Comprehensive Django admin panel for managing products, categories, orders, users, blog posts, etc.
*   **Blog:** Section for articles, with content managed via a rich text editor (Summernote).
*   **Newsletter Subscription:** Integration with Mailchimp.
*   **Responsive Design:** Styled to work across various devices (desktop, tablet, mobile).
*   **Eco-Friendly Focus:** Highlights natural ingredients, eco jesmonite jars, organic hemp wicks.
*   **Pet-Friendly Options:** Clearly indicates unscented candles suitable for homes with pets.

---

## Tech Stack

*   **Backend:** Python, Django (v5.2 mentioned, please confirm)
*   **Frontend:** HTML5, CSS3, JavaScript
*   **CSS Framework:** Bootstrap (v4.6.2 confirmed)
*   **Database:** PostgreSQL (for Heroku/production), SQLite3 (for local development)
*   **Key Django Packages:**
    *   `django-allauth`: For user authentication.
    *   `django-crispy-forms`: For rendering Django forms with Bootstrap.
    *   `crispy-bootstrap5`: 
    *   `django-countries`: For country selection fields.
    *   `django-storages` & `boto3`: For AWS S3 static and media file storage.
    *   `Pillow`: For image processing.
    *   `gunicorn`: WSGI HTTP Server for production.
    *   `psycopg2-binary`: PostgreSQL adapter.
    *   `dj_database_url`: For Heroku database configuration.
    *   `django-summernote`: WYSIWYG editor for blog content.
    *   `bleach==4.1.0`: HTML sanitizer (pinned version for `django-summernote` compatibility).
*   **Payment Integration:** Stripe, PayPal
*   **Email Marketing:** Mailchimp
*   **Deployment:** Heroku, AWS S3

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:
*   Python (3.8+ recommended)
*   pip (Python package installer)
*   Git
*   PostgreSQL (Optional for local, but recommended for full setup mirroring production)
*   An AWS account with an S3 bucket configured (for static/media files in production or production-like local testing)
*   A Stripe account (for payment processing)
*   A Mailchimp account (for newsletter functionality)

---

## Installation & Setup

### Cloning the Repository
```bash
git clone https://github.com/kristine-kiki/KK39_Candles 
cd KK39_Candles
```
### Setting up the Virtual Environment
```bash
python -m venv .venv
```
On Windows
```bash
.venv\Scripts\activate
```
On macOS/Linux
```bash
source .venv/bin/activate
```
### Installing Dependencies
```bash
pip install -r requirements.txt
```
### Environment Variables (env.py)
This project uses an env.py file to manage sensitive credentials and settings for local development. This file should not be committed to version control (ensure it's in your .gitignore).
Create an env.py file in the root of your project:
```bash
import os
# Or for local PostgreSQL:
os.environ.setdefault('DATABASE_URL', 'postgres://USER:PASSWORD@HOST:PORT/DB_NAME')

os.environ.setdefault('STRIPE_PUBLIC_KEY', 'YOUR_STRIPE_PUBLIC_KEY')
os.environ.setdefault('STRIPE_SECRET_KEY', 'YOUR_STRIPE_SECRET_KEY')
os.environ.setdefault('STRIPE_WH_SECRET', 'YOUR_STRIPE_WEBHOOK_SECRET')

# Only needed if testing S3 locally (when DEBUG=False or USE_AWS is set)
os.environ.setdefault('USE_AWS', '1') # Set to True to use S3 settings
os.environ.setdefault('AWS_ACCESS_KEY_ID', 'YOUR_AWS_ACCESS_KEY_ID')
os.environ.setdefault('AWS_SECRET_ACCESS_KEY', 'YOUR_AWS_SECRET_ACCESS_KEY')
os.environ.setdefault('AWS_STORAGE_BUCKET_NAME', 'kk39-candles') # Your S3 bucket name
os.environ.setdefault('AWS_S3_REGION_NAME', 'eu-north-1') # Your S3 bucket region
```
### Esnsure your settings.py loads env.py at the top
```bash
import os
if os.path.isfile('env.py'):
    import env
```
### Database setup
<strong>Local SQLite (Default):</strong> If DATABASE_URL in env.py points to sqlite:///db.sqlite3, Django will use SQLite. No further setup is usually needed beyond migrations.<br>

<strong>Local PostgreSQL:</strong>
<li>Ensure PostgreSQL is installed and running.</li>
<li>Create a database and a user for the project.</li>
<li>Update DATABASE_URL in env.py with your PostgreSQL connection string.</li>

### Running Migrations
```bash
python manage.py makemigrations --dry-run
```
With this commanad you are able to see migrations, without migrating them.If you are happy run command
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
### Creating Superuser
Create an admin user to access the Django admin panel
```bash
python manage.py createsuperuser
```
Follow instructions to set up a username, email, password. Note: when setting up password it won`t show you are typing anything in, but it will.

### Compiling Static Files
<li><strong>For local development (DEBUG = True):</strong>Django's development server usually handles static files automatically from your app's static directories and STATICFILES_DIRS.</li>
<li><strong>For testing production settings locally (i.e., DEBUG = False and USE_AWS = 'True' in env.py) or before deploying to production:</strong></li>
```bash
python manage.py collectstatic --noinput
```
This command collects static files from all your applications into STATIC_ROOT or uploads them directly to S3 if your STATICFILES_STORAGE is configured for S3.

## Running the Project Locally
<ol>
<li>Ensure your virtual environment is activated.</li>
<li>Ensure your env.py variables are set (especially SECRET_KEY and DATABASE_URL).</li>
<li>Start the Django development server:</li>

```bash
python manage.py runserver
```

<li>Open your web browser and go to http://127.0.0.1:8000/.</li></ol>

---

## Deployment
This project is configured for deployment to <strong>Heroku</strong> with static and media files served from <strong>AWS S3.</strong>
<ol>
<li><strong>Heroku: </strong></li>
<ul>Ensure a Procfile is present (e.g., web: gunicorn KK39_Candles.wsgi:application).</ul>
<ul>Set up Heroku Add-ons (e.g., Heroku Postgres).</ul>
<ul>Configure all necessary Config Vars on Heroku corresponding to the variables in env.py (DATABASE_URL will be set by Heroku Postgres, Stripe keys, AWS keys, Mailchimp keys, SECRET_KEY, etc.).</ul>
<ul>DEBUG should be False in production (set via Heroku Config Var or ensure it defaults to False if DEVELOPMENT var isn't set).</ul>
<ul>ALLOWED_HOSTS should include your Heroku app domain.</ul>
<li><strong>AWS S3:</strong></li>
<ul>Ensure your S3 bucket is created and configured for public access for static/media files.</ul>
<ul>Ensure the IAM user credentials used have appropriate permissions for S3 (GetObject, PutObject, DeleteObject, ListBucket, PutObjectAcl).</ul>
<ul>Configurate CORS</ul></ol>

---

## Key Funcionality Overview 

### User Facing
*   **Homepage:** Features hero section, bestsellers, "Our Story" teaser, newsletter signup.
*   **Products Page & Search:** Lists all products, allows filtering by category. A dedicated search page (`/search/`) allows users to find products based on keywords in product names, descriptions, and categories. <!-- <<< MODIFIED/ADDED DETAIL -->
*   **Product Detail Page:** Shows product images, description, price, reviews, quantity selector, and "Add to Cart" button. Users can submit reviews here.
*   **Shopping Bag Page:** Displays items in the bag, allows quantity updates and item removal. Shows subtotal, delivery cost, and grand total.
*   **Secure Checkout Page:** Secure form for shipping, contact, and payment details (Stripe card element, PayPal option, Apple/Google Pay via Stripe Payment Request Button).
*   **User Profile Page:** Authenticated users can view past order history and update default delivery information.
*   **Authentication Pages:** Login, Signup, Logout, Password Reset, Email Management (via `django-allauth`).
*   **About Section:** "Our Story", "Ingredients", "Blog List", "Blog Post Detail" pages.
*   **Contact Section:** "Contact Us" form, "FAQ", "Shipping & Returns", "Terms of Service".

### Admin Facing (`/admin/`)

*   **Product Management:** Add, edit, delete products, including details, images, pricing, stock, categories, bestseller status.
*   **Category Management:** Manage product categories.
*   **Order Management:** View and update order details and statuses.
*   **User Management:** View and manage registered users.
*   **Blog Post Management:** Create, edit, and publish blog posts using the Summernote WYSIWYG editor.

---

## Known Issues

---

## Future Development

---

## Credits & Aknowledgments
Django Allauth: For comprehensive authentication.
Crispy Forms: For styling Django forms.
Django Countries: For the country selection field.
Django Storages & Boto3: For AWS S3 integration.
Pillow: For image handling.
Stripe & PayPal: For payment processing.
Summernote & django-summernote: For the rich text editor.
Bootstrap 4.6.2: For frontend styling.
Font Awesome: For icons.
My mentor Spencer
Code Institute for walkthrough project Boutique Ado, SheCode 
