import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w"):
        pass

# Load task data from tasks.txt
with open("tasks.txt", "r") as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = {}
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT).date()
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT).date()
    curr_t['completed'] = True if task_components[5] == "Yes" else False
    task_list.append(curr_t)


# Login Section
def login():
    """
    Function to authenticate the user and grant admin rights.
    """
    # Read user.txt file and load username-password pairs
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

    with open("user.txt", "r") as user_file:
        user_data = user_file.read().split("\n")

    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    logged_in = False
    while not logged_in:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in username_password:
            print("User does not exist")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            logged_in = True

            # Return True if admin, False otherwise
            return curr_user == "admin"  

admin_access = login()

# Define username_password variable outside of the login() function
username_password = {}


def reg_user():
    """
    Function to register a new user.
    """
    new_username = input("New Username: ")
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    if new_username in username_password:
        print("Username already exists. Please choose a different username.")
    elif new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "a") as out_file:
            out_file.write(f"\n{new_username};{new_password}")
    else:
        print("Passwords do not match")


def generate_reports():
    """
    Function to generate task reports.
    """
    total_tasks = len(task_list)
    completed_tasks = sum(task['completed'] for task in task_list)
    incomplete_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(task['due_date'] < date.today() and not task['completed'] for task in task_list)

    print("Task Overview:")
    print(f"Total tasks: {total_tasks}")
    print(f"Completed tasks: {completed_tasks}")
    print(f"Incomplete tasks: {incomplete_tasks}")
    print(f"Overdue tasks: {overdue_tasks}")

    print("\nUser Overview:")
    user_counts = {}
    for task in task_list:
        username = task['username']
        if username not in user_counts:
            user_counts[username] = {'total': 0, 'completed': 0, 'incomplete': 0, 'overdue': 0}
        user_counts[username]['total'] += 1
        if task['completed']:
            user_counts[username]['completed'] += 1
        else:
            user_counts[username]['incomplete'] += 1
            if task['due_date'] < date.today():
                user_counts[username]['overdue'] += 1

    for username, counts in user_counts.items():
        print(f"Username: {username}")
        print(f"Total tasks: {counts['total']}")
        print(f"Completed tasks: {counts['completed']}")
        print(f"Incomplete tasks: {counts['incomplete']}")
        print(f"Overdue tasks: {counts['overdue']}")
        print("=" * 50)


while True:
    print()
    menu = input('''Welcome To Task Manager
Select one of the following options below:
r - Register a user
a - Add a task
va - View all tasks
vm - View my tasks
ds - Display statistics
vr - Generate reports
e - Exit
: ''').lower()

    if menu == 'r':
        # Register a new user
        if admin_access:
            reg_user()
        else:
            print("Access denied. Only admin users can register new users.")

    elif menu == 'a':
        # Add a new task
        task_username = input("Username of the person the task is assigned to: ")
        task_title = input("Task title: ")
        task_description = input("Task description: ")
        task_due_date = input("Due date (YYYY-MM-DD): ")
        task_assigned_date = date.today().strftime(DATETIME_STRING_FORMAT)

        new_task = {
            'username': task_username,
            'title': task_title,
            'description': task_description,
            'due_date': datetime.strptime(task_due_date, DATETIME_STRING_FORMAT).date(),
            'assigned_date': datetime.strptime(task_assigned_date, DATETIME_STRING_FORMAT).date(),
            'completed': False
        }

        task_list.append(new_task)

        with open("tasks.txt", "a") as task_file:
            task_file.write(f"{task_username};{task_title};{task_description};"
                            f"{task_due_date};{task_assigned_date};No\n")
        print("Task added successfully!")

    elif menu == 'va':
        # View all tasks
        print("All Tasks:")
        print("{:<15} {:<15} {:<30} {:<15} {:<15} {:<10}".format(
            "Username", "Title", "Description", "Due Date", "Assigned Date", "Completed"))
        print("=" * 100)
        for task in task_list:
            print("{:<15} {:<15} {:<30} {:<15} {:<15} {:<10}".format(
                task['username'], task['title'], task['description'], task['due_date'],
                task['assigned_date'], "Yes" if task['completed'] else "No"))

    elif menu == 'vm':
        # View my tasks
        username = input("Username: ")
        print("My Tasks:")
        print("{:<15} {:<15} {:<30} {:<15} {:<15} {:<10}".format(
            "Username", "Title", "Description", "Due Date", "Assigned Date", "Completed"))
        print("=" * 100)
        for idx, task in enumerate(task_list):
            if task['username'] == username:
                print("{:<15} {:<15} {:<30} {:<15} {:<15} {:<10}".format(
                    task['username'], task['title'], task['description'], task['due_date'],
                    task['assigned_date'], "Yes" if task['completed'] else "No"))
                if admin_access:
                    option = input("Edit (E) / Mark as Complete (M) / Skip (S): ").lower()
                    if option == "e":
                        new_title = input("New title: ")
                        new_description = input("New description: ")
                        task_list[idx]['title'] = new_title
                        task_list[idx]['description'] = new_description
                        with open("tasks.txt", "w") as task_file:
                            for task in task_list:
                                completed_str = "Yes" if task['completed'] else "No"
                                task_file.write(f"{task['username']};{task['title']};{task['description']};"
                                                f"{task['due_date'].strftime(DATETIME_STRING_FORMAT)};"
                                                f"{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};"
                                                f"{completed_str}\n")
                    elif option == "m":
                        task_list[idx]['completed'] = True
                        with open("tasks.txt", "w") as task_file:
                            for task in task_list:
                                completed_str = "Yes" if task['completed'] else "No"
                                task_file.write(f"{task['username']};{task['title']};{task['description']};"
                                                f"{task['due_date'].strftime(DATETIME_STRING_FORMAT)};"
                                                f"{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};"
                                                f"{completed_str}\n")
                    elif option == "s":
                        continue
                    else:
                        print("Invalid option. Skipping task.")
                        continue
                else:
                    print("Access denied. You do not have permission to edit tasks.")
                print("Task updated successfully!")


    elif menu == 'ds':
        # Display statistics
        total_tasks = len(task_list)
        completed_tasks = sum(task['completed'] for task in task_list)
        incomplete_tasks = total_tasks - completed_tasks
        overdue_tasks = sum(task['due_date'] < date.today() and not task['completed'] for task in task_list)

        print("Task Statistics:")
        print(f"Total tasks: {total_tasks}")
        print(f"Completed tasks: {completed_tasks}")
        print(f"Incomplete tasks: {incomplete_tasks}")
        print(f"Overdue tasks: {overdue_tasks}")

    elif menu == 'vr':
        # Generate reports
        generate_reports()

    elif menu == 'e':
        # Exit
        break

    else:
        print("Invalid input. Please try again.")

print("Task Manager closed.")
