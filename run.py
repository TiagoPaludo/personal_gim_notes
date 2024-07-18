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
    Display a menu for the given options and return the user's choice.
    """
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    choice = int(input("Enter the number of your choice: "))
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


def load_workout(is_new_user):
    """
    Load the defined parameters of exercises to workout.

    If existing user, ask if they want to load features or create new.
    """
    if is_new_user:

        print("Welcome, new user! Start creating your workout plan.")

    else:

        choice = select_option("Load existing workout or create a new one?", ["Load existing", "Create new"])

        if choice == "Load existing":

            print("Loading your existing workout features...")

            workout = SHEET.worksheet("features").get_all_values()[2:]  # Skip first two rows

            for workout_row in workout:

                print("Your workout features:", workout_row)

            return workout

        else:

            print("Creating new workout plan.")

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

    Read all user data from the worksheet.

    """

    print("Reading user data...\n")

    user_worksheet = SHEET.worksheet("user")

    users = user_worksheet.get_all_records()

    for user in users:

        print(user)



def read_workout_data():

    """

    Read all workout data from the worksheet starting from the third row.

    """

    print("Reading workout data...\n")

    features_worksheet = SHEET.worksheet("features")

    workouts = features_worksheet.get_all_values()[2:]  # Skip first two rows

    for workout in workouts:

        print(workout)



def update_user():

    """

    Update an existing user's data.

    """

    read_user_data()

    email = input("Enter the email of the user you want to update: ")

    user_worksheet = SHEET.worksheet("user")

    user_list = user_worksheet.get_all_records()

    for index, user in enumerate(user_list):

        # Print user details to debug

        print(user)

        if user['email'] == email:

            new_data = get_user_data()

            for i, value in enumerate(new_data):

                user_worksheet.update_cell(index + 2, i + 1, value)

            print("User data updated successfully.")

            return

    print("User not found.")



def delete_user():

    """

    Delete a user by email.

    """

    read_user_data()

    email = input("Enter the email of the user you want to delete: ")

    user_worksheet = SHEET.worksheet("user")

    user_list = user_worksheet.get_all_records()

    for index, user in enumerate(user_list):

        if user['email'] == email:

            user_worksheet.delete_row(index + 2)

            print("User deleted successfully.")

            return

    print("User not found.")



def delete_workout():

    """

    Delete a workout by selecting it from the list starting from the third row.

    """

    read_workout_data()

    workout_worksheet = SHEET.worksheet("features")

    workout_list = workout_worksheet.get_all_values()[2:]  # Skip first two rows

    choice = int(input("Enter the number of the workout you want to delete: "))

    if 1 <= choice <= len(workout_list):

        workout_worksheet.delete_row(choice + 2)  # Adjust for zero-index and skipped rows

        print("Workout deleted successfully.")

    else:

        print("Invalid choice.")

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
        return True # New user

    elif choice == 2:

        print("Logging in...")
        # Implement login functionality here

        return False # Existing User

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

    choice = int(input("Enter the number of your choice: "))



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
    is_new_user = user_menu()
    

    if not is_new_user:

        manage_data()

    workout_data = load_workout(is_new_user)

    if workout_data is None:  # If creating new workout

    

        options = ["leg press", "chest press", "pull down"]

        selected_option = gim_menu(options)

        print(f"You selected: {selected_option}")

        additional_details = additional_info()

        update_features_worksheet([selected_option] + additional_details)

    
if __name__ == "__main__":

    main()