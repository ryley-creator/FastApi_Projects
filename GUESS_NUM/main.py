# import random
# def get_level():
#     while True:
#         print('Please choose one of these levels')
#         print('1. Easy(10)')
#         print('2. Medium(5)')
#         print('3. Hard(3)')
#         choice = int(input('Choose your level(1/2/3): '))
        
#         if choice == 1:
#             return 10
#         elif choice == 2:
#             return 5
#         elif choice == 3:
#             return 3
#         else:
#             print('Incorrect input.Please choose form (1/2/3)')

# def play():
#     print('Welcome to the number guessing game')
#     print('Find the number the number that computer has generated')
    
#     attempts = get_level()
#     print(f'You have {attempts} attempts to find the number')
    
#     random_number = random.randint(1,100)
    
#     attempts_used = 0
#     guessed = False
    
#     while attempts_used < attempts and not guessed:
#         guess = int(input('Input the number: '))
#         attempts_used += 1
        
#         if guess == random_number:
#             guessed = True
#             print(f'Congrats you find the number {random_number} in {attempts_used} attempts')
#         elif guess < random_number:
#             print('Incorrect the number is bigger')
#         else:
#             print('Incorrect the number is smaller')
    
#     if not guessed:
#         print(f'Your attempts are over the number was {random_number}')

# def main():
    
#     while True:
#         play()
        
#         play_again = input('Do you want to play one more time(yes/no)')
#         if play_again != 'yes':
#             print('Goodbye.')
#             break

# if __name__ == '__main__':
#     main()


import random

def get_level():
    while True:
        print('Please choose one of these levels')
        print('1. Easy(10)')
        print('2. Medium(5)')
        print('3. Hard(3)')
        choice = int(input('Choose your level(1/2/3): '))
        
        if choice == 1:
            print('Great,you choosed the Easy level')
            return 10
        elif choice == 2:
            print('Great,you choosed the Medium level')
            return 5
        elif choice == 3:
            print('Great,you choosed the Hard level')
            return 3
        else:
            print('Incorrect input.Please choose from (1/2/3)')

def play():
    print('Welcome to the number guessing game')
    print('Find the number that the computer has generated')
    
    attempts = get_level()
    print(f'You have {attempts} attempts to find the number')
    
    random_number = random.randint(1, 100)
    
    attempts_used = 0
    guessed = False
    
    while attempts_used < attempts and not guessed:
        guess = int(input('Input the number: '))
        attempts_used += 1
        
        if guess == random_number:
            guessed = True
            print(f'Congrats! You found the number {random_number} in {attempts_used} attempts')
        elif guess < random_number:
            print(f'Incorrect, the number is bigger than {guess}')
        else:
            print(f'Incorrect, the number is smaller than {guess}')
    
    if not guessed:
        print(f'Your attempts are over. The number was {random_number}')

while True:
    play()
    
    play_again = input('Do you want to play one more time (yes/no)? ')
    if play_again != 'yes':
        print('Goodbye.')
        break
