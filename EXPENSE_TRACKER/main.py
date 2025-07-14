import argparse
import json
from datetime import datetime
import os
import calendar

json_file = 'tracker.json'

def load_tasks():
    if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
        with open(json_file, 'r') as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(json_file, 'w') as file:
        json.dump(tasks, file, indent=4)

def get_id(tasks):
    last_id = 0
    for task in tasks:
        if 'id' in task and task['id'] > last_id:
            last_id = task['id']
    return last_id

def time():
    return datetime.now().date().isoformat()

def add_task(task, amount):
    if task is None or amount is None:
        print("Description and amount are required.")
        return
    
    tasks = load_tasks()
    last_id = get_id(tasks)
    new_id = last_id + 1
    tasks.append({
        'id': new_id,
        'description': task,
        'amount': amount,
        'created_at': time(),
        'updated_at': time()
    })
    save_tasks(tasks)
    print(f'Task "{task}" added succefully with id:{new_id}')

def update(id, new_task):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == id:
            task['description'] = new_task
            task['updated_at'] = time()
            save_tasks(tasks)
            print(f'Description with id {id} was successfully updated to "{new_task}"')
            return 
    print('Invalid ID, try again')

def delete(id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == id:
            tasks.remove(task)
            print(f'Task with id {id} was successfully removed')
            save_tasks(tasks)
            return
    print(f'Task with id {id} was not found')



def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print('There is no tasks please add some.')
        return
    header = f'{'ID':<4} {'DATE':<12} {'DESCRIPTION':<15} {'AMOUNT':<7}'
    print(header)
    
    for task in tasks:
        amount = f'${task['amount']}'
        print(f'{task['id']:<4} {task['created_at']:<15} {task['description']:<15} {amount:<7}')
    
def summary(month=None):
    tasks = load_tasks()
    total = 0
    for task in tasks:
        if month:
            task_month = datetime.fromisoformat(task['updated_at']).month
            if task_month == int(month):
                total += int(float(task['amount']) * 1000) /1000.0
        else:
            total += float(task['amount'])
    if month:
        month_name = calendar.month_name[int(month)]
        print(f'Total expenses for month {month_name}:${int(total * 1000) / 1000.0}')
    else:
        print(f'Total expense {total}')
            

def main():
    parser = argparse.ArgumentParser(description='Managing Expense Tracker')
    subparser = parser.add_subparsers(help='Command', dest='command')

    add_task_parser = subparser.add_parser('add', help='Adds the task and amount')
    add_task_parser.add_argument('--description', help='Description of the task')
    add_task_parser.add_argument('--amount', help='Input an amount')

    delete_parser = subparser.add_parser('delete', help='Deletes the task')
    delete_parser.add_argument('id', type=int, help='Input an id of the task to delete')

    list_parser = subparser.add_parser('list', help='Shows the list of tasks')

    update_parser = subparser.add_parser('update', help='Updates the task')
    update_parser.add_argument('id', type=int, help='ID of the task to update')
    update_parser.add_argument('--description', help='New description of the task')
    
    summary_parser = subparser.add_parser('summary',help='Shows the summary of the expense')
    summary_parser.add_argument('--month',help='Input the month to see how much money did you spend')

    args = parser.parse_args()

    if args.command == 'add':
        add_task(args.description, args.amount)
    elif args.command == 'delete':
        delete(args.id)
    elif args.command == 'update':
        update(args.id, args.description)
    elif args.command == 'list':
        list_tasks()
    elif args.command == 'summary':
        if args.month:
            summary(args.month)
        else:
            summary()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
