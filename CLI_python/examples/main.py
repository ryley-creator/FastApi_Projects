# def main():
#     try:
#         to_do_list = []
        
#         infile = open('todolist.txt','r')
#         line = infile.readline()
#         while line:
#             to_do_list.append(line.rstrip('\n').split(','))
#             line = infile.readline()
#         infile.close()
#     except FileNotFoundError:
#         print('The <todolist.txt> file is not found')

#     choice = None
#     while choice != 'quit':
#         print('*** ToDo List Manager')
#         print('(add) Add a task')
#         print('(task) Update the task')
#         print('(list) List of tasks')
#         print('(quit) Quiting from the ToDo List Manager')
#         choice = input()

#         if choice == 'add':
#             print('Adding a book...')
#             nTask = input('Add the task:')
#             to_do_list.append([nTask])
#         elif choice == 'task':
#             print('Looking up for the task...')
#             keyword = input('Enter the id of the task:')
#             for task in to_do_list:
#                 if keyword in task:
#                     print(task)
#         elif choice == 'list':
#             print('Displaying all of the tasks')
#             for i in range(len(to_do_list)):
#                 print(to_do_list[i])
#         elif choice == 'quit':
#             print('Quitting the programm')
#     print('Program Terminated!')
#     outfile = open('todolist.txt','w')
#     for task in to_do_list:
#         outfile.write(','.join(task) + '\n')
#     outfile.close()


# if __name__ == '__main__':
#     main()


import json


# json_string = '''{
#     "name": "John",
#     "age": 30,
#     "isAdmin": false,
#     "courses": ["html", "css", "js"],
#     "wife": null
# }'''


json_string = '''[
    {
        "title": "And Now for Something Completely Different",
        "year": 1971
    },
    {
        "title": "Monty Python and the Holy Grail",
        "year": 1975
    }
]'''


# data = json.loads(json_string)
# # print(data['courses'][0])
# data['Shodiyor'] = 'Full Stack Developer'

# new_json = json.dumps(data,indent=2)
# print(new_json)


#form file

# with open('data.json','r') as f:
#     data = json.load(f)
    
# print(data.items())

with open('data2.json','w') as f:
    json.dump(json_string,f)
    
def summary(month=None):
    tasks = load_tasks()
    total = 0
    
    for task in tasks:
        if month:
            task_month = datetime.fromisoformat(task['created_at']).month
            if task_month == month:
                total += float(task['amount'])
        else:
            total += float(task['amount'])
    
    if month:
        print(f"Total expenses for month {month}: ${total}")
    else:
        print(f"Total expenses: ${total}")

