#!/usr/bin/env python3
import os
import json
import argparse
from datetime import datetime


json_file = 'tasks.json'

def load_tasks():
    if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
        with open(json_file,'r') as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(json_file,'w') as file:
        json.dump(tasks,file,indent=4)
    return []

def get_id(tasks):
    last_id = 0
    for task in tasks:
        print(task)
        if 'id' in task and task['id'] > last_id:
            last_id = task['id']
    return last_id

def add_task(task):
    tasks = load_tasks()
    last_id = get_id(tasks)
    new_id = last_id + 1
    tasks.append({
        'id':new_id,
        'description':task,
        'status':'todo',
        'created_at':current_time(),
        'updated_at':current_time()
    })
    save_tasks(tasks)
    print(f'Task "{task}" was added with id {new_id}')

def current_time():
    return datetime.now().isoformat()

def list_of_tasks():
    tasks = load_tasks()
    if not tasks:
        print('There id no task.Add the task.')
    for task in tasks:
        info = ({
            'id':task['id'],
            'description':task['description'],
            'status':task['status'],
            'created_at':task['created_at'],
            'updated_at':task['updated_at']
        })
        print(info)
    return
        

def list_done():
    tasks = load_tasks()
    for task in tasks:
        if task['status'] == 'done':
            done = ({
            'id':task['id'],
            'description':task['description'],
            'status':task['status'],
            'created_at':task['created_at'],
            'updated_at':task['updated_at']

            })
            print(done)
    
            
    

def delete_task(id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == id:
            tasks.remove(task)
            print(f'Task with {id} was deleted')
            save_tasks(tasks)
            return
    print(f'Task with id {id} was not found')


def update_status(id,new_status):
    tasks = load_tasks()
    statuses = ['todo','in-progress','done']
    if new_status not in statuses:
        print(f'Invalid input.Choose from [{statuses}]')
    for task in tasks:
        if task.get('id') == id:
            task['status'] = new_status
            task['updated_at'] = current_time()
            save_tasks(tasks)
            print(f'{id} id"s status was updated to {new_status}')
        return 
    print('Invalid Id.Try again')

def update_desc(id,new_desc):
    tasks = load_tasks()
    for task in tasks:
        if task.get('id') == id:
            task['description'] = new_desc
            task['updated_at'] = current_time()
            save_tasks(tasks)
            print(f'Description with id {id} was updated to {new_desc}')
        return 
    print('Invalid Id.Try again.')

def main():
    parser = argparse.ArgumentParser('Managing ToDo list')
    subparser = parser.add_subparsers(help='Command',dest='command')
    
    add_task_parser = subparser.add_parser('add',help='Adds the task')
    add_task_parser.add_argument('description',help='Description of the task')
    
    delete_parser = subparser.add_parser('delete',help='Deletes the task')
    delete_parser.add_argument('id',type=int,help='Input an id of the task that u want to delete')
    
    list_parser = subparser.add_parser('list',help='Showes the list of the tasks')
    
    update_parser = subparser.add_parser('update',help='Updates the status or the description of the task')
    update_parser.add_argument('id',type=int,help='Id of the task')
    update_parser.add_argument('-s','--status',help='Update the status of the task')
    update_parser.add_argument('-d','--description',help='Updates the description of the task')
    
    args = parser.parse_args()
    
    if args.command == 'add':
        add_task(args.description)
    elif args.command == 'list':
        list_done()
    elif args.command == 'delete':
        delete_task(args.id)
    elif args.command == 'update':
        if args.description:
            update_desc(args.id,args.description)
        if args.status:
            update_status(args.id,args.status)
    else:
        parser.print_help()

if __name__ == '__main__':
    if not os.path.exists(json_file):
        save_tasks([])
    main()
            

    



        
    


