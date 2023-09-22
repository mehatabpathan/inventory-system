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

CREDS = Credentials.from_service_account_file('/Users/mehatab/Downloads/word-Py-main/testing/creds.json')
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
        