"""
Defines the main() function which starts the game, along with the Game class
which is responsible for controlling the flow of the game.
"""

from datetime import date
import os
import random
import gspread
from google.oauth2.service_account import Credentials
import pyfiglet
import pandas as pd
import colorama
from colorama import Fore, Style
from modules.word_checker import WordChecker

colorama.init(autoreset=True)

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('word-Py-Leaderboard')
