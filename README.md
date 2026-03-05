# FluxPoint Django Backend

## Setup

1. **Activate virtual environment:**
   ```bash
   cd backend
   source venv/bin/activate  # On Linux/Mac
   # or
   venv\Scripts\activate  # On Windows
   ```

2. **Install dependencies (already installed):**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations (already done):**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication (`/api/auth/`)
- `GET /api/auth/csrf/` - Get CSRF token
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/check/` - Check authentication status
- `GET/PUT /api/auth/profile/` - Get/update user profile
- `POST /api/auth/change-password/` - Change password
- `GET/POST /api/auth/addresses/` - List/create addresses
- `GET/PUT/DELETE /api/auth/addresses/<id>/` - Address detail

### Products (`/api/products/`)
- `GET /api/products/` - List products (with filtering)
- `GET /api/products/featured/` - Featured products
- `GET /api/products/categories/` - List categories
- `GET /api/products/categories/<slug>/` - Category detail
- `GET /api/products/<slug>/` - Product detail
- `GET/POST /api/products/<slug>/reviews/` - Product reviews

### Cart (`/api/cart/`)
- `GET /api/cart/` - Get current cart
- `POST /api/cart/add/` - Add to cart
- `PUT /api/cart/update/<item_id>/` - Update cart item
- `DELETE /api/cart/remove/<item_id>/` - Remove from cart
- `DELETE /api/cart/clear/` - Clear cart

### Orders (`/api/orders/`)
- `GET /api/orders/` - List user orders
- `POST /api/orders/create/` - Create order from cart
- `GET /api/orders/<order_number>/` - Order detail
- `POST /api/orders/<order_number>/cancel/` - Cancel order

### Wishlist (`/api/wishlist/`)
- `GET /api/wishlist/` - Get wishlist
- `POST /api/wishlist/add/` - Add to wishlist
- `DELETE /api/wishlist/remove/<product_id>/` - Remove from wishlist
- `DELETE /api/wishlist/clear/` - Clear wishlist
- `GET /api/wishlist/check/<product_id>/` - Check if in wishlist

### Blog (`/api/blog/`)
- `GET /api/blog/` - List blog posts
- `GET /api/blog/featured/` - Featured posts
- `GET /api/blog/categories/` - Blog categories
- `GET /api/blog/tags/` - Blog tags
- `GET /api/blog/<slug>/` - Post detail
- `GET/POST /api/blog/<slug>/comments/` - Post comments

## Admin Panel

Access the admin panel at: `http://localhost:8000/admin/`

## Query Parameters for Filtering

### Products
- `category` - Filter by category slug
- `min_price` / `max_price` - Price range
- `featured=true` - Featured products only
- `on_sale=true` - Products on sale
- `search` - Search term
- `ordering` - Sort by: price, -price, created_at, -created_at, name

### Blog Posts
- `category` - Filter by category slug
- `tag` - Filter by tag slug
- `type` - Filter by post type (standard, audio, video, gallery, quote)
- `featured=true` - Featured posts only
- `search` - Search term
