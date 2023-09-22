from datetime import datetime
import random
import sys
import pyfiglet
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('products')

productsheet = SHEET.worksheet('productsheet')
all_products = productsheet.get_all_values()
print(all_products)


# Define a class to encapsulate functionality

class InventorySystem:
    def __init__(self, all_products):
        self.all_products = all_products

    def display_all(self):
        print("SNO\tProduct\t\tIn Stock\tPrice")
        for item in self.all_products:
            print("{0}\t{1}\t{2}\t\t{3}".format(item[0], item[1], item[2], item[3]))

    def banner(self):
        print("*************************************")
        welcome_text = pyfiglet.figlet_format("** Mobile Shop **")
        print(welcome_text)
        print("*************************************")
        print("\t1.Show All Products")
        print("\t2.Buy Product")
        print("\t3.Add Products")
        print("\t4.Exit")
        print("**************************************")

    def add_product(self, prod):
        prod.append(len(self.all_products) + 1)
        prod.append(input("Enter the Product Name: "))
        prod.append(int(input("Available: ")))
        prod.append(float(input("Price: ")))  # Use float for price
        self.all_products.append(prod)

    def admin_login(self):
        username = input("Enter Admin UserID: ")
        password = input("Enter the Password: ")
        if username == "Admin" and password == "password":
            prod = []
            self.add_product(prod)
            productsheet = SHEET.worksheet('productsheet')
            productsheet.append_row(prod)  # Append the new product data
            print("Data added to the sheets")
        else:
            print("Incorrect username and password")

    def order_summary(self, prod_id, name):
        for item in self.all_products:
            if item[0] == prod_id:
                print("***********************************************")
                print("\t\tClix Mobiles Shop")
                print("***********************************************")
                print("Order Summary\tDate:{}".format(str(datetime.now())))
                print("Customer Name: {}".format(name))
                print("Product Name: {}".format(item[1]))  # Display the product name (item[1])
                print("Price: {}".format(item[3]))  # Display the product price (item[3])
                print("***********************************************")
                print("\t\tTotal Bill Amount: {}".format(item[3]))  # Use item[3] for price
                break  # Exit the loop once the product is found

    def generate_bill(self, prod_id, name):
        item = None  # Initialize item as NonE
        for product in self.all_products:
            if product[0] == prod_id:
                item = product
                break  # Exit the loop once the product is found

        if item:
            # Remove the '$' and ',' characters from the price string
            price_str = item[3].replace('$', '').replace(',', '')
            price = float(price_str)  # Convert the modified price string to a float
            quantity = 1  # Assuming the quantity is 1 for a single product
            total_cost = price * quantity
            print("***********************************************")
            print("\t\tClix Mobiles Shop")
            print("***********************************************")
            print("Bill:{} \tDate:{}".format(int(random.random() * 100000), str(datetime.now())))
            print("Customer Name: {}".format(name))
            print("Product Name: {}".format(item[1]))
            print("Price per Unit: ${}".format(price))  # Display the price with '$'
            print("Quantity: {}".format(quantity))
            print("Total Cost: ${}".format(total_cost))  # Display the total cost with '$'
            print("***********************************************")
            print("\t\tTotal Bill Amount: ${}".format(total_cost))  # Display the total bill with '$'
        else:
            print("Product not found with the given ID")






# Main code

inventory_system = InventorySystem(all_products)

while True:
    inventory_system.banner()
    choice = int(input())
    if choice == 1:
        inventory_system.display_all()

    elif choice == 2:
        prod_id = int(input("Enter the Product ID: "))
        # Validate prod_id here before proceeding
        name = input("Customer Name: ")  # Get the customer's name
        # Adjust prod_id to match the list index (subtract 1)
        prod_id -= 1
        if 0 <= prod_id < len(inventory_system.all_products):
            inventory_system.order_summary(inventory_system.all_products[prod_id][0], name)  # Pass the product ID as an argument
            cnf = input("Confirm the Order (Y/N)")
            if cnf == 'Y':
                inventory_system.generate_bill(inventory_system.all_products[prod_id][0], name)  # Pass the product ID as an argument
                print("Thanks For shopping with Us")
                sys.exit(0)
            else:
                print("Continue Exploring the shop")
        else:
            print("Product not found with the given ID")
    elif choice == 3:
        inventory_system.admin_login()
    else:
        welcome_text = pyfiglet.figlet_format(" GOOD BYE!! ")
        print(welcome_text)
        break




