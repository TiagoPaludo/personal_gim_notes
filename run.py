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
SHEET = GSPREAD_CLIENT.open("personal gim notes")

def get_user_data():
    """
    get user data inseted by imput metod
    """
    print("Please enter detais required to create a new user. if You are user log in please")
    print("insert data as in order example")
    print("name,surname,age(00),gender(male,female),weight(in kg),height(in cm)\n")

    data_str = input("enter your details here:")
    print(f"the data provided is",{data_str})

get_user_data()