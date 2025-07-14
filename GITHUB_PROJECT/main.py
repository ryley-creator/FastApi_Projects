import argparse
import requests
from collections import defaultdict


def get_user(username):
    url = f'https://api.github.com/users/{username}/events'
    response = requests.get(url)
    
    if response.status_code == 200:
        events = response.json()
        return events
    else:
        print(f'User {username} is invalid.Please try again later.')
        return None

def event(events):
    if not events:
        print('The user does not have events')
        return
    
    count = defaultdict(int)
    # count = 0
    for event in events:
        if event['type'] == 'PushEvent':
            rep_name = event['repo']['name']
            count_comm = len(event['payload']['commits'])
            count[rep_name] += count_comm
            # print(f'Pushed {count_comm} commit to {rep_name}')
        elif event['type'] == 'WatchEvent':
            name = event['repo']['name']
            print(f'Starred {name}')
        elif event['type'] == 'IssueEvent':
            action = event['payload']['action']
            issue = event['payload']['issue']['title']
            repo_name = event['repo']['name']
            print(f'{action} a new issue {issue} in {repo_name}')
    
    for rep_name,count_comm in count.items():
        print(f'Pushed {count_comm} commits to {rep_name}')

def main():
    
    parser = argparse.ArgumentParser(description='Getting information about GitHub user')
    parser.add_argument('username',help='Input the name of the user to get the info')
    args = parser.parse_args()
    
    if args.username:
        events = get_user(args.username)
        event(events)
if __name__ == '__main__':
    main()





    
        
       







