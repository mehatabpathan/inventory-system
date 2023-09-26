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

    def admin_login(self, case):
        username = input("Enter Admin UserID:\n")
        password = input("Enter the Password:\n")
        if username == "Admin" and password == "password":
            if case == 'add':
                prod = []
                added = self.add_product(prod)
                if added:
                    productsheet = SHEET.worksheet("productsheet")
                    # Append the new product data
                    productsheet.append_row(prod)
                    print("Product Data added to the Database")
                else:
                    print('Product exists already in the Database')
            elif case == 'remove':
                prod = input('Enter Product Id: ')
                remove = self.remove_product(prod)
                if not remove:
                    print('Product Id not found in the Database')
        else:
            print("Incorrect username and password")

    def add_product(self, prod):
        product_name = input("Enter the Product Name:\n")
        product_exists = False
        for pro in self.all_products:
            if product_name == pro[1].strip():
                product_exists = True
                break
        if not product_exists:
            quantity = input("Available Items:\n")
            price = input("Price per Unit:\n")
            total_price = int(quantity)*int(price)
            if len(self.all_products) > 1:
                prod.append(int(len(self.all_products)))
            prod.append(product_name)
            prod.append(int(quantity))
            prod.append(int(price))
            prod.append(total_price)
            self.all_products.append(prod)
            return True
        else:
            return False

    def remove_product(self, prod_id):
        for index, item in enumerate(self.all_products[1:], start=1):
            if str(item[0]) == str(prod_id):
                self.all_products.pop(index)

                # Remove the product from the Google Sheet
                productsheet = SHEET.worksheet("productsheet")
                # Add 1 because the worksheet index starts from 1
                productsheet.delete_rows(index+1)

                print("Product with ID {}, Name ( {} ) removed successfully.".format(
                    int(prod_id), item[1]))
                break
        else:
            return False

        # Update the IDs in a serial manner after a product is removed
        for i, item in enumerate(self.all_products[1:], start=1):
            item[0] = str(i)
            # Update the product ID in the Google Sheet
            # +1 because worksheet index starts from 1 (to skip header)
            productsheet.update_cell(i + 1, 1, i)

        return True

    def display_all(self):
        # Fetching the latest data from the spreadsheet
        try:
            productsheet = SHEET.worksheet("productsheet")
            self.all_products = productsheet.get_all_values()
        except Exception as e:
            print("Error fetching updated data from Google Sheets:", str(e))

        if not self.all_products:
            print("No products available.")
        else:
            max_widths = [max(len(str(item[i]))
                              for item in self.all_products) for i in range(4)]
            headers = ["Product ID", "Product Name", "In Stock", "Price"]
            format_string = "{:<{width[0]}} {:<{width[1]}} {:<{width[2]}} {:<{width[3]}}"
            print(format_string.format(*headers, width=max_widths))
            print("------------------------------------------------------------")
            for index, item in enumerate(self.all_products, start=1):
                if index == 1:
                    continue
                print(format_string.format(
                    index - 1, item[1], item[2], item[3], width=max_widths))

    def banner(self):
        print("***************************************************************************")
        print(pyfiglet.figlet_format(
            "WELCOME TO ELECTRONICS WORLD", justify="center", width=80))
        print("***************************************************************************")
        print("\t1.Show All Products")
        print("\t2.Buy a Product")
        print("\t3.Add Products")
        print("\t4.Remove Products")
        print("\t5.Exit")
        print("***************************************************************************")

    def order_summary(self, prod_id, name):
        for item in self.all_products[1:]:
            if item[0] == prod_id:
                print(
                    "***************************************************************************")
                print("\t\t\tElectronics World")
                print(
                    "***************************************************************************")
                print("Order Summary\tDate:{}".format(str(datetime.now())))
                print("Customer Name: {}".format(name))
                print("Product Name: {}".format(item[1]))
                print("Price: {}".format(item[3]))
                print(
                    "***************************************************************************")
                print("\t\t\tTotal Bill Amount: {}".format(item[3]))
                print(
                    "***************************************************************************")
                break

    def generate_bill(self, prod_id, name):
        item = None
        for product in self.all_products[1:]:
            if int(product[0]) == prod_id:
                item = product
                product[2] = int(product[2]) - 1
                break
        if item:
            # Update the quantity in the spreadsheet
            productsheet.update_cell(int(prod_id) + 1, 3, item[2])

            price_str = str(item[3]).replace("$", "").replace(",", "")
            price = float(price_str)
            quantity = 1
            total_cost = price * quantity
            print(
                "***************************************************************************")
            print("\t\t\tElectronics World")
            print(
                "***************************************************************************")
            print("Bill:{} \tDate:{}".format(
                int(random.random() * 100000), str(datetime.now())))
            print("Customer Name: {}".format(name))
            print("Product Name: {}".format(item[1]))
            print("Price per Unit: ${}".format(price))
            print("Quantity: {}".format(quantity))
            print("Total Cost: ${}".format(total_cost))
            print(
                "***************************************************************************")
            print("\t\t\tTotal Bill Amount: ${}\n".format(total_cost))
        else:
            print("Product not found with the given ID")


# Main code
inventory_system = InventorySystem(all_products)

choice = 0  # Initialize choice to 0 before the loop
while choice != 5:
    inventory_system.banner()
    choice_input = input("Enter your choice: ")
    try:
        choice = int(choice_input)
        if choice == 1:
            print("\n")
            inventory_system.display_all()
            input("\n\nPress Any key to continue...\n")
        elif choice == 2:
            prod_id = input("Enter the Product ID:\n")

            if prod_id.isdigit() and 1 <= int(prod_id) < len(inventory_system.all_products):
                name = input("Customer Name:\n")
                prod_id = int(prod_id)
                selected_product = inventory_system.all_products[prod_id]
                if int(selected_product[2]) <= 0:  # Check for product quantity
                    print('\n')
                    print("Sorry, the item is sold out. Please come back later!")
                    continue
                inventory_system.order_summary(prod_id, name)
                cnf = input("Confirm the Order (Y/N)\n")
                if cnf.lower() == "y":
                    inventory_system.generate_bill(prod_id, name)
                    print("\t\t\tThanks For shopping with Us\n")
                    print(
                        "***************************************************************************")
                    input("\n\nPress Any key to continue...\n")
                else:
                    print('Order cancelled..')
            else:
                print("Product not found with the given ID\n")
                input("\n\nPress Any key to continue...\n")
        elif choice == 3:
            inventory_system.admin_login('add')
            input("\n\nPress Any key to continue...\n")
        elif choice == 4:
            inventory_system.admin_login('remove')
            input("\n\nPress Any key to continue...\n")
        elif choice == 5:
            welcome_text = pyfiglet.figlet_format(" GOOD BYE!!! ")
            print(welcome_text)
            break
        else:
            print("Invalid choice. Please select a valid option.\n")
    except ValueError:
        print("Invalid input. Please enter a valid integer choice.\n")
    except KeyboardInterrupt:
        print("Program terminated by the user.\n")
        sys.exit(0)
    except Exception as e:
        print("An error occurred:\n", str(e))
