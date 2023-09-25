from datetime import datetime
import random
import sys
import pyfiglet
from colorama import Fore, init, Style
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

try:
    CREDS = Credentials.from_service_account_file("creds.json")
    SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    SHEET = GSPREAD_CLIENT.open("products")
    productsheet = SHEET.worksheet("productsheet")
    all_products = productsheet.get_all_values()
except Exception as e:
    print("Error: Unable to access Google Sheets:", str(e))
    sys.exit(1)

class InventorySystem:
    def __init__(self, all_products):
        self.all_products = all_products

    def display_all(self):
        if not self.all_products:
            print("No products available.")
        else:
            max_widths = [max(len(str(item[i])) for item in self.all_products) for i in range(4)]
            headers = ["Product ID", "Product Name", "In Stock", "Price"]
            format_string = "{:<{width[0]}} {:<{width[1]}} {:<{width[2]}} {:<{width[3]}}"
            print(format_string.format(*headers, width=max_widths))
            print("------------------------------------------------------------")
            for index, item in enumerate(self.all_products, start=1):
                if index == 1:
                    continue
                print(format_string.format(index - 1, item[1], item[2], item[3], width=max_widths))

    def banner(self):
        print("*************************")
        print(pyfiglet.figlet_format("WELCOME TO ELECTRONICS WORLD", justify="center", width=80))
        print("*************************")
        print("\t1.Show All Products")
        print("\t2.Buy Product")
        print("\t3.Add Products")
        print("\t4.Exit")
        print("*************************")

    def order_summary(self, prod_id, name):
        for item in self.all_products[1:]:
            if item[0] == prod_id:
                print("********************************")
                print("\t\tElectronics World")
                print("********************************")
                print("Order Summary\tDate:{}".format(str(datetime.now())))
                print("Customer Name: {}".format(name))
                print("Product Name: {}".format(item[1]))
                print("Price: {}".format(item[3]))
                print("*****************")
                print("\t\tTotal Bill Amount: {}".format(item[3]))
                break

    def generate_bill(self, prod_id, name):
        item = None
        for product in self.all_products[1:]:
            if product[0] == prod_id:
                item = product
                break
        if item:
            price_str = item[3].replace("$", "").replace(",", "")
            price = float(price_str)
            quantity = 1
            total_cost = price * quantity
            print("*****************")
            print("\t\tElectronics World")
            print("*****************")
            print("Bill:{} \tDate:{}".format(int(random.random() * 100000), str(datetime.now())))
            print("Customer Name: {}".format(name))
            print("Product Name: {}".format(item[1]))
            print("Price per Unit: ${}".format(price))
            print("Quantity: {}".format(quantity))
            print("Total Cost: ${}".format(total_cost))
            print("*****************")
            print("\t\tTotal Bill Amount: ${}".format(total_cost))
        else:
            print("Product not found with the given ID")

# Main code
inventory_system = InventorySystem(all_products)

choice = 0  # Initialize choice to 0 before the loop
while choice != 4:
    inventory_system.banner()
    choice_input = input("Enter your choice: ")
    try:
        choice = int(choice_input)
        if choice == 1:
            inventory_system.display_all()
            input("\n\nPress Enter to continue...\n")
        elif choice == 2:
            prod_id = input("Enter the Product ID:\n")
            name = input("Customer Name:\n")
            if prod_id.isdigit() and 1 <= int(prod_id) < len(inventory_system.all_products):
                prod_id = int(prod_id)
                inventory_system.order_summary(prod_id, name)
                cnf = input("Confirm the Order (Y/N)\n")
                if cnf == "Y":
                    inventory_system.generate_bill(prod_id, name)
                    print("Thanks For shopping with Us\n")
            else:
                print("Product not found with the given ID\n")
        elif choice == 3:
            inventory_system.admin_login()
        elif choice == 4:
            welcome_text = pyfiglet.figlet_format(" GOOD BYE!!! ")
            print(welcome_text)
        else:
            print("Invalid choice. Please select a valid option.\n")
    except ValueError:
        print("Invalid input. Please enter a valid integer choice.\n")
    except KeyboardInterrupt:
        print("Program terminated by the user.\n")
        sys.exit(0)
    except Exception as e:
        print("An error occurred:\n", str(e))
