# KK39 Candles - Handmade Eco-Friendly E-commerce Store

## Table of Contents
1.  [Project Description](#project-description)
2.  [Live Demo](#live-demo)
3.  [Features](#features)
4.  [User Walkthrough](#user-walkthrough)
4.  [User Stories](#user-stories)
4.  [UX/UI Design](#uxui-design) 
    *   [Responsive Design](#responsive-design)
    *   [Color Scheme](#color-scheme)
    *   [Typography](#typography) 
5.  [Wireframes](#wireframes)
5.  [Tech Stack](#tech-stack)
6.  [Prerequisites](#prerequisites)
7.  [Installation & Setup](#installation--setup)
    *   [Cloning the Repository](#cloning-the-repository)
    *   [Setting up the Virtual Environment](#setting-up-the-virtual-environment)
    *   [Installing Dependencies](#installing-dependencies)
    *   [Environment Variables (`env.py`)](#environment-variables-envpy)
    *   [Database Setup](#database-setup)
    *   [Database Schema & Data Management](#database-schema--data-management)
    *   [Running Migrations](#running-migrations)
    *   [Creating a Superuser](#creating-a-superuser)
    *   [Compiling Static Files](#compiling-static-files)
8.  [Running the Project Locally](#running-the-project-locally)
9.  [Deployment](#deployment)
10. [Key Functionality Overview](#key-functionality-overview)
    *   [User Facing](#user-facing)
    *   [Admin Facing](#admin-facing)
    *   [Authentication & User Management](#authentication--user-management)
15. [Testing](#testing)
    *   [Manual Testing](#manual-testing)
    *   [HTML & CSS Validation](#html--css-validation)
    *   [Automated Testing (Django's Test Framework)](#automated-testing-djangos-test-framework)
11. [Known Issues](#known-issues)
12. [Future Development](#future-development)
13. [Credits & Acknowledgements](#credits--acknowledgements)
14. [License](#license)

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
*   **Wishlist:** Users can add products to wishlist, what they can see in their profile.
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

## User Walkthrough (Key User Flows)

This section visually demonstrates common user journeys through the KK39 Candles website, from browsing products to completing a purchase and viewing order history.

### 1. Browsing and Adding to Bag (Guest or Logged-in User)

**Step 1: Landing on the Homepage**
A visitor arrives at the homepage, greeted by the hero section and calls to action.
![Homepage Screenshot](./static/images/readme/walkthrough/main_page1.png/)

Can read a section/teaser about KK39 Candles
![Homepage Screenshot](./static/images/readme/walkthrough/main_page2.jpeg/)

Visitor is introduced with our Bestseller section
![Homepage Screenshot](./static/images/readme/walkthrough/main_page3.png/)

A small review section is visible, to build a trust 
![Homepage Screenshot](./static/images/readme/walkthrough/main_page4.png/)

Social link section. Visitor can click on any picture what will take to official KK39 Candles Instagram page
![Homepage Screenshot](./static/images/readme/walkthrough/main_page5.png/)

Contact Section
![Homepage Screenshot](./static/images/readme/walkthrough/main_page6.png/)

Footer section 
![Homepage Screenshot](./static/images/readme/walkthrough/main_page7.png/)

**Step 2: Navigating to All Products**
The user clicks on "SHOP ALL" in the main navigation.
![Navigation to Products Screenshot](./static/images/readme/walkthrough/dropdown.png/)

**Step 3: Viewing the Product Listing Page**
The user sees a grid of available products.
![Product Listing Page Screenshot](./static/images/readme/walkthrough/product_page.png/)

**Step 4: Clicking on an Individual Product**
The user selects a product Small Eco Gift Set from the list to view its details.The user sees the product's image, description,
![Clicking Product Screenshot](./static/images/readme/walkthrough/product_detail1.png/)

 price, and other options. The user selects a quantity (if applicable) and clicks the "ADD TO CART" button. A success message appears.
 If user is admin, then see Edit Button as well, if not button is not visible
![Product Listing Page Screenshot](./static/images/readme/walkthrough/product_detail2.png)

**Step 5: Viewing the Shopping Bag**
The user navigates to their shopping bag, often by clicking the bag icon in the header. They can see the item(s) added, update quantities, or remove items.
![Product Listing Page Screenshot](./static/images/readme/walkthrough/shopping_bag.png)

### 2. Checkout Process

**Step 6: Proceeding to Checkout**
From the shopping bag, the user clicks "SECURE CHECKOUT".The user fills in their shipping address, contact information. If logged in, this information might be pre-filled.
![Product Listing Page Screenshot](./static/images/readme/walkthrough/checkout.png)

**Step 7: Selecting Payment Method and Paying**
The user selects a payment method (e.g., Stripe card entry, PayPal) and completes the payment.
![Product Listing Page Screenshot](./static/images/readme/walkthrough/payment_option.png)
![Product Listing Page Screenshot](./static/images/readme/walkthrough/payment_buttons.png)

**Step 8: Order Confirmation / Success Page**
After successful payment, the user is redirected to an order confirmation page summarizing their order.
![Product Listing Page Screenshot](./static/images/readme/walkthrough/success.png)

### 3. Logged-in User: Viewing Order History

**Step 9: Navigating to Profile/Orders**
A logged-in user clicks on their profile icon and selects "MY PROFILE / ORDERS" from the dropdown. If is admin, can see add products button as well. 
![Product Listing Page Screenshot](./static/images/readme/walkthrough/profile_dropdown.png)

**Step 10: Viewing Order History in Profile**
The user's profile page displays a list of their past orders.
![Product Listing Page Screenshot](./static/images/readme/walkthrough/order_history.png)

**Step 11: Viewing Details of a Specific Past Order**
The user can click on a specific order from their history to see its full details.
![Product Listing Page Screenshot](./static/images/readme/walkthrough/old_purchase.png)

---

## User Stories

This project was developed with a user-centric approach, focusing on delivering key functionalities that meet the needs of different user roles. Our user stories outline these requirements from the perspective of visitors, registered customers, and site administrators.

Below are a couple of examples illustrating the format and typical goals:

**Example 1: Browsing Products (Visitor)**
*   **User Story:** As a **visitor**, I want to **view all available candles and home fragrance products** so that I can **see the full range offered by KK39 Candles.**
*   **Acceptance Criteria (Key points):**
    *   A dedicated page (e.g., /products/) exists and is accessible from the main navigation.
    *   All currently active/published products are displayed on this page.
    *   Each product is displayed in a consistent "product card" format, showing at least its image, name, and price.
    *   Users can click on a product card to navigate to its individual product detail page.
    *   If there are many products, pagination is implemented to improve load times and usability.
    *   If no products are available, a user-friendly message like "Sorry, there are currently no products available" is displayed.

**Example 2: Adding to Wishlist (Registered Customer)**
*   **User Story:** As a **registered customer**, I want to **add a product to my personal wishlist** so that I can **save items I'm interested in for later purchase or reference.**
*   **Acceptance Criteria (Key points):**
    *   An "Add to Wishlist" button/icon is visible on the product detail page for logged-in users.
    *   An "Add to Wishlist" button/icon is visible on product cards (e.g., on the all products page, search results) for logged-in users.
    *   Clicking the "Add to Wishlist" button adds the specific product to the currently logged-in user's wishlist.
    *   A success message (e.g., "[Product Name] added to your wishlist!") is displayed to the user.
    *   If a product is already in the wishlist, the "Add to Wishlist" button should ideally change to indicate this (e.g., "Added to Wishlist" or a filled heart icon) or be replaced by a "Remove from Wishlist" option.
    *   Attempting to add a product that is already in the wishlist does not create a duplicate entry.
    *   Unauthenticated users do not see the "Add to Wishlist" button

A comprehensive list of all user stories and their current status (e.g., To Do, In Progress, Done) is managed on our GitHub Project board.

**➡️ [View Full List of User Stories & Project Board](https://github.com/users/kristine-kiki/projects/4)**

---

## UX/UI Design

The KK39 Candles project was designed with a focus on a clean, elegant, and user-friendly experience, emphasizing the artisanal and eco-friendly nature of the products.

### Responsive Design
The website is fully responsive and designed to provide an optimal viewing and interaction experience across a wide range of devices, from mobile phones and tablets to desktops. Bootstrap 4.6.2 is utilized as the primary framework for the responsive grid system and components. Custom CSS media queries are employed to fine-tune layouts, typography, and navigation for different screen sizes, ensuring usability and aesthetic consistency. ![KK39 Candles on Multiple Devices](./static/images/readme/amiresponsive.png)
### Color Scheme
The color palette is designed to be warm, natural, and inviting, reflecting the qualities of handmade eco-candles.

| Color Swatch & Hex Code             | Variable Name          | Description                                       | Usage Example              |
|---------------------------------------|------------------------|---------------------------------------------------|----------------------------|
| <span style="background-color:#FBF9F6; color:#000000; padding: 2px 8px; border-radius: 4px; font-family: monospace; border: 1px solid #ccc;">#FBF9F6</span> | `--bg-light` | Off-white/Cream | Main page background |
| <span style="background-color:#F6F2EC; color:#000000; padding: 2px 8px; border-radius: 4px; font-family: monospace; border: 1px solid #ccc;">#F6F2EC</span> | `--bg-accent` | Slightly darker cream | Contrast areas, subtle BGs |
| <span style="background-color:#4F4A45; color:#FFFFFF; padding: 2px 8px; border-radius: 4px; font-family: monospace; border: 1px solid #ccc;">#4F4A45</span> | `--text-color` | Dark Brown/Charcoal (slightly warm) | Main body text, default links |
| <span style="background-color:#33312e; color:#FFFFFF; padding: 2px 8px; border-radius: 4px; font-family: monospace; border: 1px solid #ccc;">#33312e</span> | `--text-heading` | Very Dark Brown/Near Black | Primary headings (H1, H2) |
| <span style="background-color:#FFFFFF; color:#000000; padding: 2px 8px; border-radius: 4px; font-family: monospace; border: 1px solid #ccc;">#FFFFFF</span> | `--text-light` | White | Text on dark backgrounds |
| <span style="background-color:#9D9C75; color:#FFFFFF; padding: 2px 8px; border-radius: 4px; font-family: monospace; border: 1px solid #ccc;">#9D9C75</span> | `--primary-color` | Muted Olive/Sage Green | Accents, top banner BG |
| <span style="background-color:#D3C4B1; color:#000000; padding: 2px 8px; border-radius: 4px; font-family: monospace; border: 1px solid #ccc;">#D3C4B1</span> | `--secondary-color` | Tan/Light Beige | Buttons (`btn-tertiary`), Hero overlay |
| <span style="background-color:#E7A385; color:#000000; padding: 2px 8px; border-radius: 4px; font-family: monospace; border: 1px solid #ccc;">#E7A385</span> | `--accent-color` | Muted Pink/Coral | Price text |
| <span style="background-color:#CCA86F; color:#000000; padding: 2px 8px; border-radius: 4px; font-family: monospace; border: 1px solid #ccc;">#CCA86F</span> | `--gold-color` | Warm Gold | Newsletter subscribe button |
| <span style="background-color:#D1C9BF; color:#000000; padding: 2px 8px; border-radius: 4px; font-family: monospace; border: 1px solid #ccc;">#D1C9BF</span> | `--border-color` | Light Beige/Grey border | General borders |
| <span style="background-color:#33312e; color:#FFFFFF; padding: 2px 8px; border-radius: 4px; font-family: monospace; border: 1px solid #ccc;">#33312e</span> | `--footer-bg` | Dark Brown/Near Black (same as `--text-heading`) | Footer background |
| <span style="background-color:#d3cec7; color:#000000; padding: 2px 8px; border-radius: 4px; font-family: monospace; border: 1px solid #ccc;">#d3cec7</span> | `--footer-text` | Light Grey/Beige text | Text in the dark footer |

*Note: `--hero-overlay-bg` uses the same color as `var(--secondary-color)`.*

### Typography
*   **Headings:** Playfair Display (serif, elegant)
*   **Body Text:** Lato (sans-serif, clean and readable)

---

## Wireframes
The following images present the initial wireframe concepts and reflecting an agile approach for the KK39 Candles website. These hand-drawn sketches are a product of early brainstorming sessions, allowing for quick iteration and exploration of ideas. Although not digitally rendered at this stage due to time considerations, they effectively outline the intended user interface, content hierarchy, and navigation flow for key pages.

Below are descriptions of the wireframes for the primary pages. The actual sketches can be found in the [KK39 Candles Wireframes folder on GitHub](https://github.com/kristine-kiki/KK39_Candles/tree/main/static/images/wireframes) directory or linked below 

### 1. Homepage

*   **Purpose:** Introduce the KK39 Candles brand, showcase featured or bestseller products, guide users to key sections of the site, and provide clear calls to action.
*   **Key Sections & Elements:**
    *   **Header:** Consistent site header with Logo, Main Navigation (Shop All, Candles, For Home, About, Contact), and Utility Navigation (Search, User/Account, Bag, Wishlist). Includes Top Banner for promotions.
    *   **Hero Section:** Prominent full-width or large section with a compelling background image, an overlay text block containing a primary headline (e.g., "Handmade Eco-Friendly Soy Candles"), a tagline, and a "Shop Now" call-to-action button.
    *   **Bestsellers/Featured Products:** A grid display (e.g., 3-4 items) of product cards, each showing an image, product name, price, and a "View Product" button. A section title like "Our Bestsellers" precedes this grid.
    *   **"Our Story" Teaser:** A section with an image on one side and text on the other. The text includes a short, engaging introduction to the brand's story and values, with a "Learn More" button linking to the full "About Us" page.
    *   **(Optional) Featured Categories:** Visually distinct blocks or cards highlighting 2-3 main product categories with links.
    *   **(Optional) Testimonials/Reviews:** A small section to display customer testimonials or star ratings.
    *   **Social Media Call to Action:** A section encouraging users to "Follow Us" with links/icons to social media platforms.
    *   **Footer:** Consistent site footer with navigation links, newsletter signup, social links, and copyright information.
![KK39 Candles Wireframes](./static/images/readme/wireframes/main_page_wireframe.jpg)

### 2. All Products / Category Page

*   **Purpose:** Allow users to browse the full product catalog or products within a specific category, with options for sorting and (future) filtering.
*   **Key Sections & Elements:**
    *   **Header & Footer:** Consistent with the rest of the site.
    *   **Page Title:** Clear heading, e.g., "All Products," "Eco Soy Candles."
    *   **(Optional) Sorting/Filtering Controls:** Area for dropdowns or links to sort by (e.g., price, popularity, newness) and filter by sub-categories or attributes.
    *   **Product Grid:** The main content area displaying products in a responsive grid format.
        *   **Product Card (Repeated):** Image, Name (link), Price, Category tags (links), "View Product" button, (Optional) Add to Wishlist icon.
    *   **Pagination:** Controls (Previous, Next, Page Numbers) if the number of products exceeds a single page view.
    *   **(Optional) "No Products Found" Message:** Displayed if the category is empty or filters result in no matches.
![KK39 Candles Wireframes](./static/images/readme/wireframes/all_products_wireframe.jpg)

### 3. Product Detail Page

*   **Purpose:** Provide comprehensive information about a single product, display reviews, and allow users to add the product to their bag or wishlist.
*   **Key Sections & Elements (Often a two-column layout on desktop):**
    *   **Header & Footer:** Consistent.
    *   **Product Images:** Main image display with (optional) smaller thumbnail images for different views.
    *   **Product Information:**
        *   Product Name (Prominent Heading)
        *   Price
        *   Average Star Rating
        *   (Optional for logged-in users) Add to Wishlist button/icon.
        *   Short Description / Key Highlights.
    *   **Call to Action Area:**
        *   Quantity Selector (Decrement button, Input field, Increment button).
        *   "Add to Cart" button.
        *   Stock availability message (e.g., "In Stock," "Out of Stock").
    *   **Detailed Information Tabs/Sections:**
        *   Full Product Description.
        *   Materials/Ingredients List.
        *   Specifications (Dimensions, Burn Time, etc.).
    *   **Customer Reviews Section:**
        *   Form to submit a new review (for logged-in users).
        *   List of existing reviews (rating, comment, user, date).
![KK39 Candles Wireframes](./static/images/readme/wireframes/product_wireframe.jpg)

### 4. Shopping Bag Page

*   **Purpose:** Allow users to review their selected items, adjust quantities, remove items, and proceed to checkout.
*   **Key Sections & Elements:**
    *   **Header & Footer:** Consistent.
    *   **Page Title:** "Your Shopping Bag" or similar.
    *   **List of Bag Items:** For each item:
        *   Product Image Thumbnail.
        *   Product Name (link to product page).
        *   Unit Price.
        *   Quantity Selector (with update/remove options).
        *   Line Item Total.
    *   **(If bag is empty) Empty Bag Message:** With a "Continue Shopping" link.
    *   **Order Summary:**
        *   Subtotal.
        *   Estimated Delivery Cost (with info/options if applicable).
        *   Grand Total.
    *   **Action Buttons:**
        *   "Continue Shopping" button.
        *   "Proceed to Checkout" button.
![KK39 Candles Wireframes](./static/images/readme/wireframes/bag_wireframe.jpg)

### 5. Checkout Page

*   **Purpose:** Securely collect shipping details, contact information, and payment information to complete an order.
*   **Key Sections & Elements (can be multi-step or single page):**
    *   **Header & Footer:** Consistent (possibly a simplified "secure checkout" header).
    *   **Page Title:** "Secure Checkout."
    *   **Shipping & Contact Information Form:** Fields for Full Name, Email, Phone, Street Address 1 & 2, Town/City, County/State, Postal Code, Country (select dropdown). "Save information" checkbox for logged-in users.
    *   **Order Summary (Brief):** A collapsed or concise view of the order total, possibly item count.
    *   **Payment Method Selection:**
        *   Stripe Card Element (for direct card input).
        *   PayPal Button.
        *   (If enabled) Stripe Payment Request Button (Apple Pay / Google Pay).
    *   **Error Display Area:** For payment or form validation errors.
    *   **Place Order Button:** Clearly labeled submit button with the total amount.
    *   **Security/Trust Badges (Optional):** Small icons indicating secure payment.
![KK39 Candles Wireframes](./static/images/readme/wireframes/checkout_wireframe.jpg)

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

## Database Schema & Data Management

The KK39 Candles application utilizes a relational database to store and manage its data. Django's Object-Relational Mapper (ORM) is used for all database interactions, providing an abstraction layer over SQL.

**Database Systems:**
*   **Production (Heroku):** PostgreSQL is used for its robustness, scalability, and advanced features. The `dj_database_url` package is used to parse the `DATABASE_URL` environment variable provided by Heroku.
*   **Local Development:** SQLite3 is the default for ease of setup, though developers can configure a local PostgreSQL instance to mirror the production environment.

### Key Models & Relationships:

The core data is structured around the following Django models:

1.  **`Product` Model (`products` app):**
    *   Stores all details about individual candle products, diffusers, wax melts, and room sprays.
    *   **Fields:** `name`, `description` (rich text via Summernote in admin), `price`, `sku`, `image` (ImageField for uploads to S3), `image_url` (optional for external images), `is_bestseller` (boolean).
    *   **Relationships:**
        *   ManyToMany with `Category`: A product can belong to multiple categories.
        *   OneToMany with `Rating` (reverse): A product can have multiple ratings.
        *   OneToMany with `WishlistItem` (reverse): A product can be in multiple users' wishlists.
        *   OneToMany with `OrderLineItem` (reverse): A product can be part of multiple order line items.
    *   **Calculated Fields:** `rating` (average rating, updated via signals or model save methods from the `Rating` model).

2.  **`Category` Model (`products` app):**
    *   Defines product categories.
    *   **Fields:** `name` (e.g., "candles", "for_home"), `friendly_name` (e.g., "Candles", "For Home").
    *   **Relationships:**
        *   ManyToMany with `Product`.

3.  **`Rating` Model (`products` app):**
    *   Stores user-submitted ratings and comments for products.
    *   **Fields:** `score` (1-5), `comment` (optional text).
    *   **Relationships:**
        *   ForeignKey to `Product`: Each rating belongs to one product.
        *   ForeignKey to `User`: Each rating is submitted by one user.
    *   **Constraints:** `unique_together = ('product', 'user')` ensures a user can rate a product only once.

4.  **`User` Model (Django's built-in `django.contrib.auth.models.User`):**
    *   Managed by `django-allauth` for authentication.
    *   Stores standard user information: `username`, `password`, `email`, `first_name`, `last_name`, `is_active`, `is_staff`, `is_superuser`.
    *   **Relationships:**
        *   OneToOne with `UserProfile`.
        *   OneToMany with `Order`.
        *   OneToMany with `Rating`.
        *   OneToMany with `WishlistItem`.

5.  **`UserProfile` Model (`profiles` app):**
    *   Extends the built-in `User` model to store additional user-specific information.
    *   **Fields:** `default_phone_number`, `default_street_address1`, `default_street_address2`, `default_town_or_city`, `default_county`, `default_postcode`, `default_country` (using `django-countries`).
    *   **Relationships:**
        *   OneToOne with `User`.

6.  **`WishlistItem` Model (`profiles` app - as per our discussion):**
    *   Connects a `User` to a `Product` they have wishlisted.
    *   **Fields:** `added_on` (timestamp).
    *   **Relationships:**
        *   ForeignKey to `User`.
        *   ForeignKey to `Product`.
    *   **Constraints:** `unique_together = ('user', 'product')`.

7.  **`Order` Model (`checkout` app):**
    *   Represents a customer's order.
    *   **Fields:** `order_number` (unique), `full_name`, `email`, `phone_number`, shipping address fields, `date`, `delivery_cost`, `order_total`, `grand_total`, `original_bag` (for Stripe), `stripe_pid`.
    *   **Relationships:**
        *   ForeignKey to `UserProfile` (optional, for registered users).
        *   OneToMany with `OrderLineItem` (reverse).

8.  **`OrderLineItem` Model (`checkout` app):**
    *   Represents an individual item within an `Order`.
    *   **Fields:** `quantity`, `lineitem_total`.
    *   **Relationships:**
        *   ForeignKey to `Order`.
        *   ForeignKey to `Product`.

9.  **`Post` Model (`about` app - for the blog):**
    *   Stores blog post content.
    *   **Fields:** `title`, `slug`, `content` (rich text via `SummernoteTextField`), `publish_date`, `status`, `featured_image`.
    *   **Relationships:**
        *   ForeignKey to `User` (author).

### Data Management & Administration:

*   **Django Admin Interface:** The primary tool for managing most data.
    *   Products, Categories, Orders, Users, User Profiles, Blog Posts, and Wishlist Items are registered with the admin site, allowing administrators to perform CRUD (Create, Read, Update, Delete) operations.
    *   Customizations like `list_display`, `list_filter`, `search_fields`, and `SummernoteModelAdmin` enhance the admin experience.
*   **Database Migrations:** Django's migration system (`makemigrations` and `migrate`) is used to manage schema changes and keep the database synchronized with the model definitions.
*   **Data Integrity:** Model field validators, `unique_together` constraints, and foreign key relationships help maintain data integrity.
*   **Backups (Production):** For the production PostgreSQL database on Heroku, regular backups are managed through Heroku Postgres tools or add-ons.

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
<ul>(e.g., Heroku Postgres).</ul>
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

### Authentication & User Management (Powered by `django-allauth`)
The KK39 Candles application provides a robust and secure authentication system for users, primarily managed by the `django-allauth` package. This allows for a comprehensive set of account management features:

**For Users:**
*   **User Registration (Sign Up):** New users can create an account by providing necessary details (typically email, username, password). `django-allauth` handles email confirmation if configured.
    ![User Signup Form Screenshot](./static/images/readme/signup.png/)
*   **User Login (Sign In):** Registered users can securely log in using their credentials (username/email and password).
    ![User Login Form Screenshot](./static/images/readme/signin.png)
*   **User Logout:** Authenticated users can securely log out of their accounts.
*   **Password Management:**
    *   **Password Reset:** Users who have forgotten their password can request a password reset via email.
    *   **Password Change:** Logged-in users can change their current password.
*   **Email Management:** Logged-in users can manage their email addresses associated with their account (e.g., add secondary emails, change primary, verify emails).
*   **Social Logins (Optional - if configured):** `django-allauth` supports easy integration of social media logins (e.g., Google, Facebook), though this may not be implemented in the current version of KK39 Candles. *(Adjust this sentence based on your implementation)*
*   **Persistent Sessions:** "Remember Me" functionality allows users to stay logged in across browser sessions.

**User Profile (`profiles` app):**
*   Each authenticated user has an associated `UserProfile` which stores default delivery information and order history.
*   Users can view and update their profile information after logging in.
    ![User Profile Page Screenshot](./static/images/readme/walkthrough/order_history.png)

**For Administrators (via Django Admin):**
*   **User Overview:** Administrators can view a list of all registered users, search, and filter them.
    ![Admin User List Screenshot](./static/images/readme/admin_panel.png)
*   **Detailed User Management:**
    *   View and edit individual user details (username, email, first/last name).
    *   Manually set or change user passwords (with appropriate security considerations).
    *   Control user status:
        *   Activate or deactivate user accounts (`is_active` flag).
        *   Grant or revoke staff status (`is_staff` flag for admin access).
        *   Grant or revoke superuser status (`is_superuser` flag).
    *   Manage user group memberships and specific permissions.
    ![Admin User Detail/Edit Screenshot](./static/images/readme/admin1.png)

`django-allauth` provides templates for all authentication views, which have been customized to match the KK39 Candles brand aesthetic.

---

## Testing

A comprehensive testing strategy was employed throughout the development of KK39 Candles to ensure functionality, reliability, and a positive user experience. Testing was conducted at multiple levels, including manual testing of user flows and automated testing for core application logic.

### Manual Testing

Extensive manual testing was performed to cover key user stories and critical paths within the application. This involved:

*   **User Authentication Flow:**
    *   Testing user registration, email confirmation (if enabled), login with valid and invalid credentials, password reset functionality, and logout.
    *   Verifying access restrictions for authenticated vs. unauthenticated users.
*   **Product Browsing & Discovery:**
    *   Navigating to the "All Products" page and individual category pages.
    *   Testing product search functionality with various terms (including those expected to yield results and those expected not to).
    *   Verifying product detail page display (images, description, price, reviews).
*   **Shopping Bag & Checkout Process:**
    *   Adding various products to the bag.
    *   Updating quantities in the bag.
    *   Removing items from the bag.
    *   Proceeding to checkout and testing the form with valid and invalid data (e.g., incorrect card details, missing required address fields).
    *   Simulating successful and failed payments with Stripe (using test card numbers) and PayPal (using sandbox accounts).
    *   Verifying order confirmation and data storage.
*   **User Profile Management:**
    *   Updating saved delivery information.
    *   Viewing order history and details of past orders.
*   **Wishlist Functionality:**
    *   Adding products to the wishlist.
    *   Viewing the wishlist.
    *   Removing products from the wishlist.
    *   Verifying that "Add to Wishlist" buttons correctly reflect the product's wishlist status.
*   **Product Reviews & Ratings:**
    *   Submitting new product ratings and reviews as a logged-in user.
    *   Verifying that reviews are displayed correctly on product detail pages.
    *   Checking that a user cannot review the same product multiple times.
*   **Blog Functionality:**
    *   Viewing the blog list and individual blog posts.
    *   Verifying content rendering from the Summernote editor.
*   **Newsletter Subscription:**
    *   Subscribing with a valid email and checking for redirection to the Mailchimp/custom thank-you page.
*   **Admin Interface:**
    *   CRUD (Create, Read, Update, Delete) operations for Products, Categories, and Blog Posts.
    *   Viewing and managing Orders.
    *   Basic User account management (activating/deactivating, staff status).
*   **Responsiveness:**
    *   Testing the website layout and functionality across various screen sizes (desktop, tablet, mobile) using browser developer tools and, if possible, physical devices.
    *   Ensuring navigation, forms, and content are accessible and usable on all supported devices.
*   **Cross-Browser Compatibility (Basic):**
    *   Testing key functionalities on modern versions of major browsers (e.g., Chrome, Firefox, Edge, Safari).
*   **Accessibility (Basic Checks):**
    *   Ensuring semantic HTML, appropriate ARIA labels (where implemented), and keyboard navigability for core features.

### HTML & CSS Validation

### Automated Testing (Django's Test Framework)

Automated tests were written using Django's built-in testing framework to cover critical backend logic and ensure stability during development and refactoring.

*   **Models:**
    *   Tests for model creation, string representations (`__str__`), and any custom model methods (e.g., `Product.update_average_rating()`).
*   **Views:**
    *   Testing that views render the correct templates.
    *   Verifying GET requests to key pages return a 200 OK status.
    *   Testing POST requests for form submissions (e.g., adding products, submitting reviews, checkout logic if feasible without extensive mocking of payment gateways).
    *   Testing access restrictions (e.g., `@login_required` decorators).
*   **Forms:**
    *   Testing form validation with valid and invalid data for key forms (e.g., `ProductForm`, `RatingForm`, `OrderForm`).
*   **URLs:**
    *   Ensuring URL patterns correctly resolve to their respective views.

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
My mentor Spencer Barriball
Code Institute for walkthrough project Boutique Ado, SheCode 
