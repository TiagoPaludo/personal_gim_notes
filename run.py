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
        print(" name:\n surname:\n age(00):\n gender(male,female):\n \
        weight(in kg):\n height(in cm):\n e-mail:\n")

        data_str = input("Enter your details here (comma-separated):\n ")
        user_data = [data.strip() for data in data_str.split(",")]

        if validate_data(user_data):
            print("Data is valid!")
            break

    return user_data


def validate_int(value, min_value=None, max_value=None):

    try:

        int_value = int(value)
        if (min_value is not None and int_value < min_value) or (max_value is not None and int_value > max_value):
            return False
        return True
    except ValueError:
        return False


def validate_float(value, min_value=None, max_value=None):

    try:

        float_value = float(value)

        if (min_value is not None and float_value < min_value) or (max_value is not None and float_value > max_value):
            return False
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
        print(f"Exactly {len(expected_types)} values required, \
    you provided {len(values)}\n")
        return False

    validators = {
        'int': lambda v: validate_int(v, min_value=0),
        'float': lambda v: validate_float(v, min_value=0.0),
        'str': validate_str,
        'email': validate_email,
    }

    try:
        for index, (value, expected_types) in \
                enumerate(zip(values, expected_types)):
            if not validators[expected_types](value.strip()):
                raise ValueError
                (f"invalid {expected_types} value at index {index}: {value}")
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

    # Check if the worksheet is empty and set the header row if it is

    if user_worksheet.row_count == 1 and not user_worksheet.get_all_values():

        header = ["name", "surname", "age", "gender", "weight", "height", "e-mail"]

        user_worksheet.append_row(header)

    user_worksheet.append_row(data)

    print("User created/updated successfully.\n")


def select_option(prompt, options):
    """
    Display a menu for the given options and return the user's choice.
    """
    while True:
        print(prompt)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        try:
            choice = int(input("Enter the number of your choice:\n "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Invalid choice, please select a valid option.")
        except ValueError:
            print("Invalid input, please enter a number.")


def additional_info():
    """
    Get additional info from the user
    """
    exercises = ["Bench Press", "Squat", "Deadlift", "Overhead Press", "Pull-Up"]
    weights = ["10kg", "20kg", "30kg", "40kg", "50kg"]
    reps_options = ["5", "10", "15", "20", "25"]
    rest_times = ["30s", "60s", "90s", "120s"]
    periods = ["1 week", "2 weeks", "3 weeks", "1 month"]

    exercise_type = select_option("Select the type of exercise or machine:", exercises)
    weight = select_option("Select the weight used:", weights)
    reps = select_option("Select the number of reps:", reps_options)
    rest_time = select_option("Select the rest time:", rest_times)
    period_of_use = select_option("Select the period of use:", periods)

    return [exercise_type, weight, reps, rest_time, period_of_use]


def load_workout(new_user):
    """
    Load the defined parameters of exercises to workout.
    """
    features_worksheet = SHEET.worksheet("features")
    workout = features_worksheet.get_all_values()[2:]  # Skip first two rows

    if new_user:
        print("Welcome new user! Please set up your workout features.")
    else:
        if workout:
            print("Your workout features:")
            for workout_row in workout:
                print(workout_row)
            choice = input("Do you want to load these features (yes/no)? ").strip().lower()
            if choice != 'yes':
                return True  # Indicate that the user wants to create new features
        else:
            print("No existing workout features found.")
            return True  # Indicate that the user needs to create new features

    return False  # Indicate that the user doesn't need to create new features


def update_features_worksheet(data):
    """
    Update features worksheet, add new row with the list data provided
    """
    print("Updating features details...\n")
    features_worksheet = SHEET.worksheet("features")
    features_worksheet.append_row(data)
    print("Workout features updated successfully.\n")


def user_menu():

    """
    Display the user menu to choose between creating a new user or logging in.
    """

    while True:
        print("Welcome to personal gym notes")
        print("1. Create a new user")
        print("2. Log in as an existing user")
        try:
            choice = int(input("Enter the number of your choice:\n "))
            if choice == 1:
                data = get_user_data()
                update_user_worksheet(data)
                return True
                  # New user who wants to set workout features
                
            elif choice == 2:
                print("Logging in...")
                get_user_data()
                return False  # Existing user
            else:
                print("Invalid choice, please try again.")
        except ValueError:
            print("Invalid input, please enter a number.")



def main():

    """
    Call all the functions
    """
    new_user = user_menu()
    if new_user:
        workout_details = additional_info()
        update_features_worksheet(workout_details)
    else:
        need_new_features = load_workout(new_user)
        if need_new_features:
            workout_details = additional_info()
            update_features_worksheet(workout_details)
    

if __name__ == "__main__":
    main()
