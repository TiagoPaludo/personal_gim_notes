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

        data_str = input("Enter your details here (comma-separated):\n ")
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
    user_worksheet.append_row(data)
    print("User created/ updated successfully.\n")


def gim_menu(options):
    """
    Display a menu for gym exercises and return the user's choice.
    """
    print("Select the exercise:")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    choice = int(input("Enter the number of your choice:\n "))
    return options[choice - 1]


def select_option(prompt, options):
    """
    Display a menu for the given options and return the user's choice.
    """
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    choice = int(input("Enter the number of your choice:\n "))
    return options[choice - 1]


def additional_info():
    """
    Get additional info from the user
    """
    weights = ["10kg", "20kg", "30kg", "40kg", "50kg"]
    reps_options = ["5", "10", "15", "20", "25"]
    rest_times = ["30s", "60s", "90s", "120s"]
    periods = ["1 week", "2 weeks", "3 weeks", "1 month"]

    weight = select_option("Select the weight used:", weights)
    reps = select_option("Select the number of reps:", reps_options)
    rest_time = select_option("Select the rest time:", rest_times)
    period_of_use = select_option("Select the period of use:", periods)

    return [weight, reps, rest_time, period_of_use]


def load_workout():
    """
    Load the defined parameters of exercises to workout.
    
    """
features_worksheet = SHEET.worksheet("features")
workout = features_worksheet.get_all_values()[2:]  

# Skip first two rows

if workout:

    print("Your workout features:")

    for workout_row in workout:

        print(workout_row)

else:

    print("No existing workout features found.")

    


def update_features_worksheet(data):
    """
    Update features worksheet, add new row with the list data provided
    """
    print("Updating features details...\n")
    features_worksheet = SHEET.worksheet("features")
    features_worksheet.append_row(data)
    print("Workout features updated successfully.\n")


def read_user_data():
    """
    Read the user data from the worksheet.
    """
    print("Reading user data...\n")
    user_worksheet = SHEET.worksheet("user")
    user = user_worksheet.get_all_records()
    if user:

        print(user[0])

    else:

        print("No user data found.")


def read_workout_data():
    """
    Read all workout data from the worksheet starting from the third row.
    """
    print("Reading workout data...\n")
    features_worksheet = SHEET.worksheet("features")
    workouts = features_worksheet.get_all_values()[2:]  
    
    # Skip first two rows
    
    if workouts:

        for workout in workouts:

            print(workout)

    else:

        print("No workout data found.")


def update_user():
    """
    Update the existing user's data.
    """
    read_user_data()
    new_data = get_user_data()
    update_user_worksheet(new_data)
    print("User data updated successfully.")


def delete_user():
    """
    Delete the user data.
    """
    
    user_worksheet = SHEET.worksheet("user")
    user_worksheet.clear()
    print("User data deleted successfully.")


def delete_workout():
    """
    Delete all workout data.
    """
    
    features_worksheet = SHEET.worksheet("features")
    features_worksheet.clear()
    print("Workout data deleted successfully.")


def user_menu():
    """
    Display the user menu to choose between creating a new user or logging in.
    """
    print("Welcome to personal gym notes")
    print("1. Create a new user")
    print("2. Log in as an existing user")
    choice = int(input("Enter the number of your choice:\n "))

    if choice == 1:
        data = get_user_data()
        update_user_worksheet(data)
        return True

    # New user

    elif choice == 2:
        print("Logging in...")
        return False

    # Existing User

    else:
        print("Invalid choice, please try again.")

        return user_menu()


def manage_data():
    """
    Display a menu for managing user and workout data.
    """
    print("Manage Data")
    print("1. Read user data")
    print("2. Update user data")
    print("3. Delete user")
    print("4. Read workout data")
    print("5. Delete workout")
    choice = int(input("Enter the number of your choice:\n "))

    if choice == 1:
        read_user_data()
    elif choice == 2:
        update_user()
    elif choice == 3:
        delete_user()
    elif choice == 4:
        read_workout_data()
    elif choice == 5:
        delete_workout()
    else:
        print("Invalid choice, please try again.")
        manage_data()


def main():
    """
    Call all the functions
    """
    
    user_menu()
    load_workout()
    workout_details = additional_info()
    update_features_worksheet(workout_details)
    manage_data()


if __name__ == "__main__":
    main()
