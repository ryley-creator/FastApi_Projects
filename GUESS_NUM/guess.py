import os
import random
import json
import time

json_file = 'high.json'

def load():
    if os.path.exists(json_file):
        with open(json_file, 'r') as file:
            return json.load(file)
    return []  


def save(score):
    with open(json_file, 'w') as file:
        json.dump(score, file)

def get_level():
    print('Welcome to the number guessing game')
    print('Choose one of these levels (1/2/3)')
    print('1. Easy level (10 attempts)')
    print('2. Medium level (5 attempts)')
    print('3. Hard level (3 attempts)')
    choice = int(input('Input your choice: '))
    
    if choice == 1:
        print('Great, you chose the easy level')
        return 10
    elif choice == 2:
        print('Great, you chose the medium level')
        return 5
    elif choice == 3:
        print('Great, you chose the hard level')
        return 3
    else:
        print('Invalid input. Please choose from (1/2/3)')
        return get_level()
    
def play():
    name = input('Input your name: ')
    print(f'Hello {name}')
    
    guess = 0
    attempts = get_level()
    attempts_made = 0
    random_number = random.randint(1,100)
    start_time = time.time()
    
    high_scores = load()
    player_record = None
    
    for record in high_scores:
        if record['name'] == name:
            player_record = record
            break
    
    while guess != random_number and attempts != 0:
        guess = int(input('Input the number: '))
        if guess == random_number:
            print('Congrats you find the number')
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            if player_record:
                if elapsed_time < player_record['score']:
                    player_record['score'] = elapsed_time
                    print(f'Congrats {name}! New high score: {elapsed_time:.2f} seconds')
                else:
                    print(f'Congrats {name}! Your score: {elapsed_time:.2f} seconds')
            else:
                high_scores.append({'name': name, 'score': elapsed_time})
                print(f'Congrats {name}! New high score: {elapsed_time:.2f} seconds')
            save(high_scores)
            return
        elif guess > random_number:
            print(f'Incorrect.The number is smaller than {guess}')
            attempts = attempts - 1
            attempts_made += 1
        else:
            print(f'Incorrect the number is greater than {guess}')
            attempts_made += 1
            attempts =  attempts - 1
        if attempts_made % 4 == 0:
            print(f'Hint: The number is between {random_number - 5} and {random_number + 5}')

    if guess != random_number:
        print(f'You are out of attempts the number was {random_number}')
    end_time = time.time()
    elapsed_time = end_time - start_time
    if guess == random_number:
        print(f'You guessed the number in {elapsed_time:.2f} seconds')
    else:
        print('Sorry try again you dont have attempts')
while True:
    play()
    play_again = input('Do you want to play again (yes/no)')
    if play_again != 'yes':
        print('Goodbye!')
        break
    