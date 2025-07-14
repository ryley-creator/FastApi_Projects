import random
import time
def get_level():
    print('Welcome to the number guessing game')
    print('1.Easy level')
    print('2.Medium level')
    print('3.Hard level')
    print('Choose from (1/2/3)')
    choice = int(input('Choose the level: '))
    
    if choice == 1:
        print('Great,you choosed the Easy level')
        print('You have 10 attempts to find the number')
        return 10
    elif choice == 2:
        print('Great you choosed the Medium level')
        print('You have 5 attempts to find the number')
        return 5
    elif choice == 3:
        print('Great you choosed the Hard level')
        print('You have 3 attempts to find the number')
        return 3
    else:
        print('Invalid choice.Choose from (1/2/3)')

def play():
    random_number = random.randint(1,100)
    attempts = get_level()
    guess = 0
    start_time = time.time()
    while guess != random_number and attempts != 0:
        guess = int(input('Input the number: '))
        if guess == random_number:
            print('Congrats you find the number!')
        elif guess < random_number:
            print(f'Incorrect the number is bigger than {guess}')
            attempts -= 1
            if random_number % 2 == 0:
                print('The number is divisible by 2')
            elif random_number % 3 == 0:
                print('The number is divisible by 2')
            elif guess > random_number:
                print(f'{guess} + {random_number} - {guess} = ?')
        else:
            print(f'Incorrect the number is smaller than {guess}')
            attempts -= 1
    print(f'You are out of attempts,the number was:{random_number}')
            
    end_time = time.time()
    elapsed_time = end_time - start_time  
     
    
    if guess == random_number:
        print(f'You guessed the number in {elapsed_time:.2f} seconds')
    else:
        print('Sorry try again you dont have attempts')
        
while True:
    play()
    play_again = input('Do you want to play one more time(yes/no):')
    if play_again != 'yes':
        print('Goodbye')
        break








