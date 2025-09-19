import streamlit as st
import requests
import pandas as pd

# API Configuration 
API_URL = "http://127.0.0.1:8000"

#functions to talk to the API ---

def get_all_products():
    """Fetches all products from the backend."""
    try:
        response = requests.get(f"{API_URL}/products")
        response.raise_for_status()
        return response.json().get("products", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching products: {e}")
        return []

def search_product_by_id(product_id: int):
    """Fetches a single product by its ID from the backend."""
    try:
        response = requests.get(f"{API_URL}/searchproduct/{product_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error searching for product: {e}")
        return {"error": "Product not found or API is down"}

def add_product(product: dict):
    """Sends a new product to the backend."""
    try:
        response = requests.post(f"{API_URL}/products", json=product)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error adding product: {e}")
        return None

def update_product(product_id: int, product: dict):
    """Updates an existing product on the backend."""
    try:
        response = requests.put(f"{API_URL}/products?id={product_id}", json=product)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error updating product: {e}")
        return None

def delete_product(product_id: int):
    """Deletes a product from the backend."""
    try:
        response = requests.delete(f"{API_URL}/products?id={product_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error deleting product: {e}")
        return None

#Streamlit UI

st.set_page_config(page_title="Product Dashboard", layout="wide")
st.title("Product Management Dashboard")

# --- Section 1: Display All Products ---
st.header("All Products")
products_data = get_all_products()
if products_data:
    df = pd.DataFrame(products_data)
    st.dataframe(df, width='stretch')
else:
    st.info("No products found in the database.")


# --- Section 2: Search for a Product ---
st.header("🔍 Search for a Product by ID")
search_id = st.number_input("Enter Product ID to search", min_value=1, step=1, key="search_id")

if st.button("Search"):
    if search_id:
        result = search_product_by_id(search_id)
        if "Message" in result:
            st.success("Product Found!")
            st.json(result["Message"])
        else:
            st.error(result.get("error", "An unknown error occurred."))


# --- Section 3: Manage Products ---
st.header("Manage Products")
col1, col2 = st.columns(2)

# --- Add New Product Form (in column 1) ---
with col1:
    st.subheader("Add a New Product")
    with st.form("add_product_form", clear_on_submit=True):
        new_id = st.number_input("Product ID", min_value=1, step=1)
        new_name = st.text_input("Name")
        new_description = st.text_area("Description")
        new_price = st.number_input("Price", min_value=0.0) # Using float for consistency
        new_quantity = st.number_input("Quantity", min_value=0, step=1)

        submitted = st.form_submit_button("Add Product")
        if submitted:
            product_payload = {
                "id": new_id, "name": new_name, "description": new_description,
                "price": new_price, "quantity": new_quantity
            }
            result = add_product(product_payload)
            if result:
                st.toast("Product added successfully!", icon="🎉")
                st.rerun()

# --- Update/Delete Product Form (in column 2) ---
with col2:
    st.subheader("Update or Delete a Product")
    if products_data:
        product_options = {f"{p['id']} - {p['name']}": p for p in products_data}
        selected_option = st.selectbox("Select a Product", options=product_options.keys())
        
        if selected_option:
            selected_product = product_options[selected_option]
            
            with st.form("update_product_form"):
                st.write(f"Editing Product ID: {selected_product['id']}")
                update_name = st.text_input("Name", value=selected_product['name'])
                update_description = st.text_area("Description", value=selected_product['description'])
                update_price = st.number_input("Price", min_value=0.0, value=selected_product['price'])
                update_quantity = st.number_input("Quantity", min_value=0, step=1, value=selected_product['quantity'])

                update_submitted = st.form_submit_button("Update Product")
                if update_submitted:
                    product_update_payload = {
                        "id": selected_product['id'], "name": update_name, "description": update_description,
                        "price": float(update_price), "quantity": int(update_quantity)
                    }
                    result = update_product(selected_product['id'], product_update_payload)
                    if result:
                        st.toast("Product updated successfully!")
                        st.rerun()

            if st.button("Delete Selected Product", key=f"delete_{selected_product['id']}", type="primary"):
                result = delete_product(selected_product['id'])
                if result:
                    st.toast("Product deleted successfully!")
                    st.rerun()
    else:
        st.warning("No products available to manage.")