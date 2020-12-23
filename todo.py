import os
import sys
from datetime import datetime

# Import click
try:
    import click
except ImportError:
    # Install click package if it doesn't exist
    from io import StringIO

    from pip._internal import main as pip

    # Redirecting Standard output and error to String Streams
    sys.stderr, sys.stdout = StringIO(), StringIO()
    pip(['install', '--user', 'click'])

    # Redirect standard output and error back to console
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    import click

# Function to get help text
def get_help():
    commands = [
        'Usage :-',
        '$ ./todo add "todo item"  # Add a new todo',
        '$ ./todo ls               # Show remaining todos',
        '$ ./todo del NUMBER       # Delete a todo',
        '$ ./todo done NUMBER      # Complete a todo',
        '$ ./todo help             # Show usage',
        '$ ./todo report           # Statistics',
    ]
    print("\n".join(commands))
    sys.exit(0)


def add_todo_item(todo_item):
    with open('todo.txt', 'a+') as f:
        f.write(todo_item + "\n")
        print(f'Added todo: "{todo_item}"')


def delete_todo(todo_number):
    try:
        with open('todo.txt', 'r+') as f:
            data = f.readlines()
        if todo_number == 0:
            raise IndexError
        item = data.pop(todo_number - 1)
        with open('todo.txt', 'w') as f:
            f.writelines(data)
        return item
    except (IndexError, FileNotFoundError):
        return f'Error: todo #{todo_number} does not exist.'


def show_pending_todos():
    try:
        with open('todo.txt') as f:
            data = f.readlines()
    except FileNotFoundError:
        print('There are no pending todos!')
        sys.exit(0)

    if len(data) == 0:
        print('There are no pending todos!')
    data = data[::-1]

    pending_todos = len(data)
    for i in range(pending_todos):
        print(f'[{pending_todos-i}] {data[i].strip()}')


# Mark a todo as Done
def complete_todo(todo_number):
    # Call delete_todo to remove item from todo list
    todo_item = delete_todo(todo_number)
    # Check if there was an error
    if todo_item.startswith('Error'):
        print(todo_item)
        sys.exit(0)

    # Get current date in UTC format
    today_date = datetime.utcnow().strftime('%Y-%m-%d')
    with open('done.txt', 'a+') as f:
        f.write(f'x {today_date} {todo_item}')


# Get Statistics
def get_report():
    try:
        with open('todo.txt', 'r+') as f:
            pending = len(f.readlines())
    except FileNotFoundError:
        pending = 0
    try:
        with open('done.txt', 'r+') as f:
            completed = len(f.readlines())
    except FileNotFoundError:
        completed = 0
    today_date = datetime.utcnow().strftime('%Y-%m-%d')
    print(f'{today_date} Pending : {pending} Completed : {completed}')


@click.command()
@click.argument('arg', nargs=-1)  # Taking all arguments provided in a tuple
def main(arg):
    # show help to user
    if len(arg) == 0 or arg[0] == 'help':
        get_help()

    # Add item to todo
    elif arg[0] == 'add':
        try:
            add_todo_item(arg[1])
        except IndexError:
            print('Error: Missing todo string. Nothing added!')

    # Remove item from todo
    elif arg[0] == 'del':
        try:
            number = int(arg[1])
            todo_item = delete_todo(number)
            if todo_item.startswith('Error'):
                print(todo_item, "Nothing deleted.")
            else:
                print(f'Deleted todo #{number}')
        except ValueError:
            print(f'Error: Please provide a valid number to delete item')
        except IndexError:
            print('Error: Missing NUMBER for deleting todo.')

    # Show pending todos
    elif arg[0] == 'ls':
        show_pending_todos()

    # Mark a todo as done
    elif arg[0] == 'done':
        try:
            number = int(arg[1])
            complete_todo(number)
            print(f'Marked todo #{number} as done.')
        except IndexError:
            print('Error: Missing NUMBER for marking todo as done.')

    # Get Report of Pending and Completed todos
    elif arg[0] == 'report':
        get_report()

    # Giving help when a wrong option is selected
    else:
        print('Please select valid option')
        get_help()


if __name__ == '__main__':
    main()
