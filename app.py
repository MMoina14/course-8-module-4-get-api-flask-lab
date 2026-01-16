from flask import Flask, jsonify, request
from data import products

app = Flask(__name__)

# Homepage route that returns a welcome message
@app.route("/")
def home():
    """
    Homepage endpoint that returns a welcome message.
    Returns:
        JSON response with welcome message and available endpoints
    """
    return jsonify({
        "message": "Welcome to the Product Catalog API",
        "endpoints": {
            "home": "/",
            "all_products": "/products",
            "single_product": "/products/<id>",
            "filter_by_category": "/products?category=<category_name>"
        }
    }), 200

# GET /products route that returns all products or filters by category
@app.route("/products")
def get_products():
    """
    Returns all products or filters by category if query parameter is provided.
    Query Parameters:
        category (optional): Filter products by category
    Returns:
        JSON response with list of products
    """
    # Check if category filter is provided in query string
    category = request.args.get("category")
    
    if category:
        # Filter products by category (case-insensitive)
        filtered_products = [
            product for product in products 
            if product["category"].lower() == category.lower()
        ]
        return jsonify({
            "count": len(filtered_products),
            "category": category,
            "products": filtered_products
        }), 200
    
    # Return all products if no filter is applied
    return jsonify({
        "count": len(products),
        "products": products
    }), 200

# GET /products/<id> route that returns a specific product by ID or 404
@app.route("/products/<int:id>")
def get_product_by_id(id):
    """
    Returns a single product by its ID.
    Path Parameters:
        id: The unique identifier of the product
    Returns:
        JSON response with product details or 404 if not found
    """
    # Search for product with matching ID
    product = next((p for p in products if p["id"] == id), None)
    
    if product:
        return jsonify(product), 200
    else:
        return jsonify({
            "error": "Product not found",
            "message": f"No product exists with ID {id}"
        }), 404

if __name__ == "__main__":
    app.run(debug=True)