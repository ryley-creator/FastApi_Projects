import random
import time
import json
import os


json_file = 'high_scores.json'

def load_high_scores():
    if os.path.exists(json_file):
        with open(json_file,'r') as file:
            return json.load(file)
    return {}

def save_high_scores(scores):
    with open(json_file,'w') as file:
        json.dump(scores,file)

def get_level():
    print('Welcome to the number guessing game')
    print('Choose one of this levels to play (1/2/3)')
    print('1.Easy level')
    print('2.Medium level')
    print('3.Hard level')
    choice = int(input('Input the level: '))
    
    if choice == 1:
        print('Great,you choosed the easy level')
        print('You have 10 attempts to guess the number')
        return 10
    elif choice == 2:
        print('Great,you choosed the medium level')
        print('You have 5 attempts to guess the number')
        return 5
    elif choice == 3:
        print('Great,you choosed the hard level')
        print('You have 3 attempts to guess the number')
        return 3
    else:
        print('Invlid choice.Choose from(1/2/3)')
    
def play():
    name = input('Input your name: ')
    print(f'Hello {name}')
    
    random_number = random.randint(1,100)
    attempts = get_level()
    guess = 0
    start_time = time.time()
    attempts_made = 0
    while guess != random_number and attempts != 0:
        guess = int(input('Input the number: '))
        if guess == random_number:
            print('Congrats you find the number')
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            high_score = load_high_scores()
            if name in high_score:
                if elapsed_time < high_score[name]:
                    high_score[name] = elapsed_time
                    save_high_scores(high_score)
                    print(f'Congrats {name}! New high score: {elapsed_time:.2f} seconds!')
                else:
                    print(f'Congrats {name}! Your score is {elapsed_time:.2f} seconds.Your current high score {high_score[name]:.2f} seconds')
            else:
                high_score[name] = elapsed_time
                save_high_scores(high_score)
                print(f'Congrats {name}! New high score {elapsed_time:.2f} seconds')
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

    
