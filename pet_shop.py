'''This program want to simulate a Pet shop where the user can buy
different pet's products and adding/deleted/edit in a card shop.
The program will use SQL to create a database that store all the products
and allow the user to navigate in the shop'''

import sqlite3

print("====== Welcome to Cat&Dog and Co. online shop ======")

# Create a dictionary to populate the database
products = [
{"id": 1, "name": "Whiskers Cat Food", "price": 3.5, "quantity": 30, "category": "food"},
{"id": 2, "name": "kong", "price": 2.5, "quantity": 20, "category": "food"},
{"id": 3, "name": "Lucerne Hay", "price": 5.5, "quantity": 50, "category": "food"},
{"id": 4, "name": "Fish food", "price": 0.5, "quantity": 85, "category": "food"},
{"id": 5, "name": "Cat Ball", "price": 10.5, "quantity": 70, "category": "toys"},
{"id": 6, "name": "Dog Ball", "price": 10.5, "quantity": 40, "category": "toys"},
{"id": 7, "name": "Dental Chew", "price": 4.99, "quantity": 100, "category": "toys"},
{"id": 8, "name": "Feather", "price": 2.5, "quantity": 60, "category": "toys"}
]

# Create a database
database = sqlite3.connect("pet_product_db")
cursor = database.cursor()

# Check if the table already exists
cursor.execute('''SELECT count(name)
               FROM sqlite_master WHERE type='table' 
               AND name='pet_product_db' ''')
table_exists = cursor.fetchone()[0]

if not table_exists:
    # Create the table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS pet_product_db
                   (id_product INTEGER PRIMARY KEY,
                   name STRING,
                   price REAL, 
                   quantity INTEGER,
                   category STRING)''')
    database.commit()

    # Populate the database
    cursor.executemany('''INSERT INTO pet_product_db
                       (id_product, name, price, quantity, category)
                       VALUES (:id, :name, :price, :quantity, :category)''' ,
                       products)
    database.commit()


def view_product():
    """
    This function retrieves and displays all products from a SQLite database
    table.
    """
    cursor.row_factory = sqlite3.Row
    cursor.execute("SELECT * FROM pet_product_db")
    print("\nThese are the products available:")
    for row in cursor.fetchall():
        print(f"\n=======\nProduct number: {row['id_product']}"
              f"\nName Product: {row['name']}"
              f"\nPrice: {row['price']}"
              f"\nCategory: {row['category']}")


def view_category(user_filter):
    """
    This Python function queries a database for pet products based on a
    user-defined category filter and displays the results.
    
    :param user_filter: takes a `user_filter`to filter the products
    from the database based on the category specified by the user
    """
    cursor.execute("SELECT * FROM pet_product_db WHERE category = :category",
                   {'category':user_filter})
    print("\nThese are the products available:")
    for row in cursor.fetchall():
        print(f"\n=======\nProduct number: {row[0]}"
              f"\nName Product: {row[1]}"
              f"\nPrice: {row[2]}")


def search_by_name(name):
    """
    The function `search_by_name` searches for products in a database based on a
    given name using SQL LIKE operator for pattern matching.
    
    :param name: The `search_by_name` function you provided is designed to search
    for products in a database table called `pet_product_db` based on a given name.
    The function converts the search query to lowercase and then uses the SQL LIKE
    operator for pattern matching to find products that contain the search query in
    their names
    """
    # Convert the search query to lowercase
    name = name.lower()
    # Use SQL LIKE operator for pattern matching
    cursor.execute(
    "SELECT * FROM pet_product_db WHERE LOWER(name) LIKE '%' || :name || '%'",
                   {'name': name})
    rows = cursor.fetchall()
    if rows:
        print("\nProducts found:")
        for row in rows:
            print(f"\n=======\nProduct number: {row[0]}"
              f"\nName Product: {row[1]}"
              f"\nPrice: {row[2]}" 
              f"\nCategory: {row[4]}")
    else:
        print("Product not found.")


def add_product_cart(id_product):
    """
    This function adds a product to the user's cart.
    
    :param id_product: The `id_product` parameter is the unique identifier of the
    product that the user wants to add to their cart. This identifier is used to
    retrieve information about the product from the database and manage the
    quantity of the product in the cart
    """
    cursor.execute("SELECT * FROM pet_product_db WHERE id_product = :id",
                   {'id':id_product})
    row = cursor.fetchone()
    if row:
        print(f"\n=======\nProduct number: {row[0]}"
              f"\nName Product: {row[1]}"
              f"\nPrice: {row[2]}"
              f"\nQuantity Available: {row[3]}"
              f"\nCategory: {row[4]}")

    user_quantity = int(input("How many do you need?: "))
    if user_quantity > row[3]:
        print("Quantity not available")
    else:
        # Append product along with its quantity to user_cart list
        user_cart.append((row, user_quantity))
        print("Product added to cart successfully!")


def view_shopping_cart():
    """
    The `view_shopping_cart` function displays the contents of the 
    user's shopping cart along with the total price.
    :return: The `view_shopping_cart` function returns the total price of 
    the items in the shopping cart. 
    If the shopping cart is empty, it prints a message that the cart is empty 
    and then returns without calculating the total price.
    """
    if not user_cart:
        print("Your shopping cart is empty.")

    total_price = 0  # Initialize total price counter

    print("\n===== This is your shopping cart:=====")
    for index, (product, quantity) in enumerate(user_cart, 1):
        print(f"Item {index}:")
        print(f"Product: {product[1]}")
        print(f"Price per unit: {product[2]}")
        print(f"Quantity: {quantity}")

        item_price = product[2] * quantity
        total_price += item_price  # Add item price to total price
        print(f"Total price: {item_price}\n")

    print(f"Total Price of your cart is: {total_price}")


def delete_product_from_cart(user_edit):
    """
    The function `delete_product_from_cart` removes a product 
    from the user's cart.
    
    :param user_edit: The `user_edit` parameter represents the item number 
    that the user wants to delete from the cart. 
    It is used to identify the specific product in the cart that the user
    wants to remove
    """
    # Remove the product from the cart
    if user_edit <= len(user_cart):
        user_cart.pop(user_edit - 1)
        print("Product removed successfully!")
    else:
        print("Invalid item number. Please enter a valid Item number.")


def edit_product_quantity(user_edit):
    """
    This function updates the quantity of a product in the user's cart.
    
    :param user_edit: The `user_edit` parameter in the `edit_product_quantity`
    function represents the index of the product in the user's cart 
    that the user wants to edit the quantity for. 
    """
    # Update the quantity of the product in the cart
    if user_edit <= len(user_cart):
        edited_quantity = int(input("Enter the new quantity you need: \n"))
        product_info, _ = user_cart[user_edit - 1]

        # Check if the edited quantity exceeds the available quantity
        if edited_quantity > products[product_info[0] - 1]["quantity"]:
            print("Quantity not available")
        else:
            # Update the quantity in the user_cart list
            user_cart[user_edit - 1] = (product_info, edited_quantity)
            print(user_cart[user_edit - 1])

        print("Quantity updated successfully!")
    else:
        print("Invalid item number. Please enter a valid Item number.")


def edit_shopping_card():
    """
    The `edit_shopping_card` function allows users to edit the shopping cart 
    by deleting products or editing quantities.
    
    :return: In the `edit_shopping_card` function, if the shopping cart is empty,
    the function prints a message "Your shopping cart is empty."
    If there are products in the cart, the function prints the cart, asks the user
    for input on which product to edit, and then asks for the action to perform
    (delete the product or edit the quantity). Depending on the user
    """
    # Check if the cart has some products inside
    if not user_cart:
        print("Your shopping cart is empty.")
        return

    # If there are products, the program prints the cart and asks how to proceed
    print(view_shopping_cart())
    user_edit = int(input("\nWhich product do you want to edit? "
                          "Enter the Item number: \n"))

    cart_edit = int(input("What do you want to do?\n"
                          "1 - Delete the product\n"
                          "2 - Edit the quantity\n"))

    if cart_edit == 1:
        delete_product_from_cart(user_edit)
    elif cart_edit == 2:
        edit_product_quantity(user_edit)


def update_database():
    """
    The function `update_database` updates the quantity availability of products
    in a database removing the quantity sitting on the user's cart.
    
    We run this function at the checkout menu, to allow the user to do all the
    edit they want before pay without calling constantly the database.
    """
    for product, quantity in user_cart:
        id_product = product[0]  # Get the ID of the product
        cursor.execute("SELECT quantity FROM pet_product_db WHERE id_product = ?",
                       (id_product,))
        current_quantity = cursor.fetchone()[0]  # Get current quantity from the database
        new_quantity = current_quantity - quantity  # Subtract quantity in the cart
        cursor.execute("UPDATE pet_product_db SET quantity = ? WHERE id_product = ?",
                       (new_quantity, id_product))
        database.commit()

# Create an empty list to storage the product that the user will select
user_cart = []

# ==== Main program ===== Menu that allow the user to move through the shop
MENU = True
while MENU is True:
    user_choice = input("\n=== MENU ==="
"=\nPlease select the option by enter a number between 1 to 4:"
"\n1 - Create a shopping cart"
"\n2 - View your shopping cart"
"\n3 - Edit your shopping cart"
"\n4 - Checkout\n")
    if not user_choice.isdigit() or not 1 <= int(user_choice) <= 4:
        print("Please insert a valid number between 1 and 4")
        continue

    user_choice = int(user_choice)  # Convert user input to integer

    if user_choice == 1:
        while True:
            # User can decide how to navigate through the products
            user_browser = input("\nPlease select: \n"
                             "1 - See all the products\n"
                             "2 - Filter by Category. \n"
                             "3 - Search by name \n:")

            # Check if the input is a valid integer
            if user_browser.isdigit():
                user_browser = int(user_browser)  # Convert to integer

                if user_browser == 1:
                    # Select the database and print all the products available
                    view_product()
                    break
                elif user_browser == 2:
                # Let the user choose the category
                    while True:
                        category_choice = input("Enter the category (food/toys): \n")
                        if category_choice.lower() == "food" or \
                            category_choice.lower() == "toys":
                            view_category(category_choice.lower())
                            break
                        else:
                            print("Please enter either 'food' or 'toys'.")
                elif user_browser == 3:
                    # Let the user choose by name
                    name_product = input("Please insert the name of the product: \n")
                    search_by_name(name_product.lower())
                    break
                else:
                    print("Please insert a valid number (1, 2, or 3)")
            else:
                print("Please insert a valid number (1, 2, or 3)")


        while True:
        # Give the chance to select from the product displayed
            choice_product = input("\nWhich product do you want to add to your cart?\n"
                           "Enter the product number or "
                           "EXIT if you want to come back to the main menu\n")
            if choice_product.upper() == "EXIT":
                break
            try:
                product_selected = int(choice_product)
                if 1 <= product_selected <= len(products):
                    add_product_cart(product_selected)
                else:
                    raise ValueError("Please enter a valid product number.")
            except ValueError:
                print("Please enter a valid product number.")

    elif user_choice == 2:
        view_shopping_cart()

    elif user_choice == 3:
        edit_shopping_card()

    elif user_choice == 4:
        update_database()
        view_shopping_cart()
        print("we will direct you to the payment page")
        print("\nThanks for visiting us\n")
        MENU = False
