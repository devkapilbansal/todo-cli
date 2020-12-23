import os
import sys
from datetime import datetime

try:
    import click
except ImportError:
    from io import StringIO

    from pip._internal import main as pip

    sys.stderr, sys.stdout = StringIO(), StringIO()
    pip(['install', '--user', 'click'])
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    import click


def help_():
    commands = [
        'Usage :-',
        '$ ./todo add "todo item" # Add a new todo',
        '$ ./todo ls\t\t # Show remaining todos',
        '$ ./todo del NUMBER\t # Delete a todo',
        '$ ./todo done NUMBER\t # Complete a todo',
        '$ ./todo help\t\t # Show usage',
        '$ ./todo report\t\t # Statistics',
    ]
    print("\n".join(commands))
    sys.exit(0)


def add_todo(todo_item):
    with open('todo.txt', 'a+') as f:
        f.write(todo_item + "\n")
        print(f'Added todo: "{todo_item}"')


def delete_todo(number):
    try:
        with open('todo.txt', 'r+') as f:
            data = f.readlines()
        item = data.pop(number - 1)
        with open('todo.txt', 'w') as f:
            f.writelines(data)
        return item
    except (IndexError, FileNotFoundError):
        return f'Error: todo #{number} does not exist.'


def show_todos():
    with open('todo.txt') as f:
        data = f.readlines()
    data = data[::-1]

    pending_todos = len(data)
    for i in range(pending_todos):
        print(f'[{pending_todos-i}] {data[i].strip()}')


def complete_todo(number):
    todo_item = delete_todo(number)
    if todo_item.startswith('Error'):
        print(todo_item)
        sys.exit(0)

    today_date = datetime.utcnow().strftime('%Y-%m-%d')
    with open('done.txt', 'a+') as f:
        f.write(f'x {today_date} {todo_item}')

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
@click.argument('src', nargs=-1)
def main(src):
    if len(src) == 0 or src[0] == 'help':
        help_()

    elif src[0] == 'add':
        add_todo(src[1])

    elif src[0] == 'del':
        try:
            if len(src) == 1:
                raise ValueError
            number = int(src[1])
            todo_item = delete_todo(number)
            if todo_item.startswith('Error'):
                print(todo_item, "Nothing Deleted.")
            print(f'Deleted todo #{number}')
        except ValueError:
            print(f'Error: Please provide a valid number to delete item')

    elif src[0] == 'ls':
        show_todos()

    elif src[0] == 'done':
        try:
            if len(src) == 1:
                raise ValueError
            number = int(src[1])
            complete_todo(number)
            print(f'Marked todo #{number} as done.')
        except Exception as e:
            print(e)

    elif src[0] == 'report':
        get_report()

    else:
        print('Please select valid option')
        help_()

if __name__ == '__main__':
    main()
