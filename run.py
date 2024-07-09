import gspread
from google.oauth2.service_account import Credentials
import re

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
    Get user data inserted by input method
    """
    while True:
        print("Please enter details required to create a new user. if You are user log in please")
        print("insert data as in order example")
        print(" name:\n surname:\n age(00):\n gender(male,female):\n weight(in kg):\n height(in cm):\n e-mail:\n")

        data_str = input("Enter your details here (comma-separated): ")
        
        user_data = data_str.split(",")
        #validate_data(user_data)

        if validate_data(user_data):
            print("Data is valid!")
            break

    return user_data

def validate_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def validate_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def validate_email(value):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, value) is not None

def validate_str(value):
    return isinstance(value, str) and len(value) > 0

def validate_data(values):
    """
    Verify the values for specified types at specified indices.
    """

    expected_types = ['str', 'str', 'int', 'str', 'float', 'int', 'email']

    if len(values) != len(expected_types):
        print(f"Exactly {len(expected_types)} values required, you provided {len(values)}\n")
        return False

    validators = {
        'int': validate_int,
        'float': validate_float,
        'str': validate_str,
        'email': validate_email,
    }

    try:
        for index, (value, expected_types) in enumerate(zip(values, expected_types)):
            if not validators[expected_types](value.strip()):
                raise ValueError(f"invalid {expected_types} value at index {index}: {value}")
    except ValueError as e:
        print(f"invalid data: {e}, try again.\n")
        return False

    return True

def update_user_worksheet(data):
    """
    Update user worksheet, add new row with the list data provided
    """
    print("Updating user worksheet...\n")
    user_worksheet = SHEET.worksheet("user")
    user_worksheet.append_row(data)
    print("User worksheet updated successfully.\n")


data = get_user_data()
update_user_worksheet(data)