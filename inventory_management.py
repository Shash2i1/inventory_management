import sqlite3
from tkinter import Tk, Label, Entry, Button, ttk, messagebox

# Database setup
def init_db():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Add product to database
def add_product(name, quantity, price):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
    conn.commit()
    conn.close()

# Update product in database
def update_product(product_id, name, quantity, price):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE products 
    SET name = ?, quantity = ?, price = ? 
    WHERE id = ?
    """, (name, quantity, price, product_id))
    conn.commit()
    conn.close()

# Delete product from database
def delete_product(product_id):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

# Get all products from database
def get_products():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

# GUI functions
def display_products():
    for i in tree.get_children():
        tree.delete(i)
    products = get_products()
    for product in products:
        tree.insert("", "end", values=product)

def add_product_ui():
    name = name_entry.get()
    quantity = quantity_entry.get()
    price = price_entry.get()
    if not name or not quantity or not price:
        messagebox.showerror("Error", "All fields are required!")
        return
    add_product(name, int(quantity), float(price))
    display_products()
    clear_entries()

def delete_product_ui():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a product to delete!")
        return
    item = tree.item(selected_item)
    product_id = item["values"][0]
    delete_product(product_id)
    display_products()

def edit_product_ui():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a product to edit!")
        return
    item = tree.item(selected_item)
    product_id = item["values"][0]
    name = name_entry.get()
    quantity = quantity_entry.get()
    price = price_entry.get()
    if not name or not quantity or not price:
        messagebox.showerror("Error", "All fields are required!")
        return
    update_product(product_id, name, int(quantity), float(price))
    display_products()
    clear_entries()

def load_selected_product():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a product to load!")
        return
    item = tree.item(selected_item)
    product_id, name, quantity, price = item["values"]
    name_entry.delete(0, "end")
    name_entry.insert(0, name)
    quantity_entry.delete(0, "end")
    quantity_entry.insert(0, quantity)
    price_entry.delete(0, "end")
    price_entry.insert(0, price)

def clear_entries():
    name_entry.delete(0, "end")
    quantity_entry.delete(0, "end")
    price_entry.delete(0, "end")

# Main window
root = Tk()
root.title("Inventory Management System")
root.geometry("650x450")
root.resizable(False, False)

# Frame for input fields and buttons
input_frame = ttk.Frame(root, padding="10")
input_frame.pack(side="top", fill="x")

Label(input_frame, text="Product Name:", anchor="w", width=15).grid(row=0, column=0, pady=5, padx=5)
name_entry = Entry(input_frame)
name_entry.grid(row=0, column=1, pady=5, padx=5)

Label(input_frame, text="Quantity:", anchor="w", width=15).grid(row=1, column=0, pady=5, padx=5)
quantity_entry = Entry(input_frame)
quantity_entry.grid(row=1, column=1, pady=5, padx=5)

Label(input_frame, text="Price:", anchor="w", width=15).grid(row=2, column=0, pady=5, padx=5)
price_entry = Entry(input_frame)
price_entry.grid(row=2, column=1, pady=5, padx=5)

# Buttons
button_frame = ttk.Frame(root, padding="10")
button_frame.pack(side="top", fill="x")

Button(button_frame, text="Add Product", command=add_product_ui, width=15).grid(row=0, column=0, pady=5, padx=5)
Button(button_frame, text="Edit Product", command=edit_product_ui, width=15).grid(row=0, column=1, pady=5, padx=5)
Button(button_frame, text="Delete Product", command=delete_product_ui, width=15).grid(row=0, column=2, pady=5, padx=5)
Button(button_frame, text="Load Selected", command=load_selected_product, width=15).grid(row=0, column=3, pady=5, padx=5)

# Treeview for displaying products
tree_frame = ttk.Frame(root, padding="10")
tree_frame.pack(side="top", fill="both", expand=True)

columns = ("ID", "Name", "Quantity", "Price")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
tree.column("ID", width=50, anchor="center")
tree.column("Name", width=200, anchor="center")
tree.column("Quantity", width=100, anchor="center")
tree.column("Price", width=100, anchor="center")
for col in columns:
    tree.heading(col, text=col)
tree.pack(fill="both", expand=True)

# Initialize database and load data
init_db()
display_products()

root.mainloop()
