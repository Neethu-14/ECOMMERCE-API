from fastapi import FastAPI, Query

app = FastAPI()

# ─────────────── Temporary Data (Acts like a database) ───────────────
products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True},
    {'id': 2, 'name': 'Notebook', 'price': 99, 'category': 'Stationery', 'in_stock': True},
    {'id': 3, 'name': 'USB Hub', 'price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set', 'price': 49, 'category': 'Stationery', 'in_stock': True},

    # Added products (Task 1)
    {'id': 5, 'name': 'Laptop Stand', 'price': 999, 'category': 'Electronics', 'in_stock': True},
    {'id': 6, 'name': 'Mechanical Keyboard', 'price': 2499, 'category': 'Electronics', 'in_stock': True},
    {'id': 7, 'name': 'Webcam', 'price': 1499, 'category': 'Electronics', 'in_stock': False}
]

# ─────────────── Home Endpoint ───────────────
@app.get('/')
def home():
    return {"message": "Welcome to our E-commerce API"}

# ─────────────── Get All Products ───────────────
@app.get('/products')
def get_all_products():
    return {"products": products, "total": len(products)}

# ─────────────── Get Product By ID ───────────────
@app.get('/products/{product_id}')
def get_product(product_id: int):

    for product in products:
        if product['id'] == product_id:
            return {"product": product}

    return {"error": "Product not found"}

# ─────────────── Existing Filter Endpoint (Day 1) ───────────────
@app.get('/products/filter')
def filter_products(
    category: str = Query(None, description="Electronics or Stationery"),
    max_price: int = Query(None, description="Maximum price"),
    in_stock: bool = Query(None, description="True = only available products")
):

    result = products

    if category:
        result = [p for p in result if p['category'] == category]

    if max_price:
        result = [p for p in result if p['price'] <= max_price]

    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]

    return {"filtered_products": result, "count": len(result)}

# ─────────────── Task 2: Category Filter ───────────────
@app.get('/products/category/{category_name}')
def category_products(category_name: str):

    result = []

    for product in products:
        if product['category'].lower() == category_name.lower():
            result.append(product)

    if not result:
        return {"error": "No products found in this category"}

    return {"products": result, "count": len(result)}

# ─────────────── Task 3: Only In-Stock Products ───────────────
@app.get('/products/instock')
def instock_products():

    instock = []

    for product in products:
        if product['in_stock']:
            instock.append(product)

    return {
        "in_stock_products": instock,
        "count": len(instock)
    }

# ─────────────── Task 4: Store Summary ───────────────
@app.get('/store/summary')
def store_summary():

    total_products = len(products)
    instock_count = 0
    outstock_count = 0
    categories = set()

    for product in products:

        categories.add(product['category'])

        if product['in_stock']:
            instock_count += 1
        else:
            outstock_count += 1

    return {
        "store_name": "My E-commerce Store",
        "total_products": total_products,
        "in_stock": instock_count,
        "out_of_stock": outstock_count,
        "categories": list(categories)
    }

# ─────────────── Task 5: Search Products ───────────────
@app.get('/products/search/{keyword}')
def search_products(keyword: str):

    result = []

    for product in products:
        if keyword.lower() in product['name'].lower():
            result.append(product)

    if not result:
        return {"message": "No products matched your search"}

    return {
        "matched_products": result,
        "count": len(result)
    }

# ─────────────── BONUS: Best Deal & Premium Pick ───────────────
@app.get('/products/deals')
def product_deals():

    cheapest_product = min(products, key=lambda x: x['price'])
    expensive_product = max(products, key=lambda x: x['price'])

    return {
        "best_deal": cheapest_product,
        "premium_pick": expensive_product
    }