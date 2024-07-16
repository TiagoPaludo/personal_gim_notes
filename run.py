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
        print("Please enter details required to create a new user.")
        print("Insert data in the following order, example:")
        print(" name:\n surname:\n age(00):\n gender(male,female):\n weight(in kg):\n height(in cm):\n e-mail:\n")

        data_str = input("Enter your details here (comma-separated): ")
        
        user_data = data_str.split(",")



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
        print(f"Invalid data: {e}, try again.\n")
        return False

    return True

def update_user_worksheet(data):
    """
    Update user worksheet, add new row with the list data provided
    """
    print("Updating user details...\n")
    user_worksheet = SHEET.worksheet("user")
    user_worksheet.append_row(data)
    print("User created successfully.\n")

def gim_menu(options):
    """
    Display a menu for gym exercises and return the user's choice.
    """
    print("Select the exercise:")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    choice = int(input("Enter the number of your choice: "))
    return options[choice - 1]

def select_option(prompt, options):
    """
    Display a menu for the given options and retur the user's choice.
    """
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    choice = int(input("Enter the number of your choice: "))
    return options[choice -1]

def additional_info():
    """
    Get additional info from the user
    """
    weights = ["20kg", "30kg", "40kg", "50kg"]

    reps = ["5", "10", "15", "20"]

    rest_times = ["30s", "60s", "90s", "120s"]

    periods_of_use = ["1 week", "2 weeks", "1 month", "2 months"]

    weight = select_option("Select the weight used:", weights)

    rep = select_option("Select the number of reps:", reps)

    rest_time = select_option("Select the rest time:", rest_times)

    period_of_use = select_option("Select the period of use:", periods_of_use)

    return [weight, rep, rest_time, period_of_use]


def load_workout():
    """
    Load the defined parameters of exercises to workout
    """
    print("Start updating your training features...")
    workout = SHEET.worksheet("features").get_all_values()
    workout_row = workout[-1]
    print(workout_row)

def update_features_worksheet(data):
    """
    Update features worksheet, add new row with the list data provided
    """
    print("Updating features details...\n")
    features_worksheet = SHEET.worksheet("features")
    features_worksheet.append_row(data)
    print("Program created successfully.\n")

def user_menu():

    """

    Display the user menu to choose between creating a new user or logging in.

    """

    print("Welcome to personal gym notes")

    print("1. Create a new user")

    print("2. Log in as an existing user")

    choice = int(input("Enter the number of your choice: "))



    if choice == 1:

        data = get_user_data()

        update_user_worksheet(data)

    elif choice == 2:

        print("Logging in...")

        # Implement login functionality here

    else:

        print("Invalid choice, please try again.")

        user_menu()


def main():
    """
    Call all the functions
    """
    user_menu()
    load_workout()
    options = ["leg press", "chest press", "pull down"]
    selected_exercise = gim_menu(options)
    print(f"You selected: {selected_exercise}")
    additional_details = additional_info()
    update_features_worksheet([selected_exercise] + additional_details)
    load_workout()

    
if __name__ == "__main__":

    main()