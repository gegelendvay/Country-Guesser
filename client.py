import functions
import getpass
import json
import os
import socket
import time

def handleGame(s):
    score = 0
    while True:
        #Question
        print(s.recv(4096).decode('utf-8'))
        try:
            #Decode the options and print them
            #Since I had issues encoding lists, I had to use json
            options = json.loads(s.recv(1024).decode('utf-8'))
            for i in options:
                print(f'- {i}')
        except json.decoder.JSONDecodeError:
            s.close()
            break

        #Answer
        answer = input('Enter your answer: ')
        s.sendall(answer.encode('utf-8'))

        #Result
        response = s.recv(1024).decode('utf-8')
        print(response)

        #If the answer is correct, continue to the next question
        if response == 'Correct answer!':
            continue

        hint = input('Yes/No: ')
        s.sendall(hint.encode('utf-8'))
        if hint.lower() == 'yes' or hint.lower() == 'y':
            #Continent
            print(s.recv(1024).decode('utf-8'))
            answer = input('Enter your answer: ')
            s.sendall(answer.encode('utf-8'))
            #Result
            print(s.recv(1024).decode('utf-8'))
        else:
            #If the user doesn't want a hint, get the score and end the game cycle
            response = s.recv(1024).decode('utf-8')
            print(response)
            score = int(response.split(': ', 1)[1])
            break

    while True:
        #If the game is over, provide the user with different options to choose from
        print('[1]Play Again\n[2]Leaderboard\n[3]Save Score\n[4]Reset Score\n[5]Quit')
        userInput = input()
        #If the input is not a number, close the connection and end the game
        if not userInput.isdigit():
            return False

        userInput = int(userInput)
        clearConsole()
        #Play again
        if userInput == 1:
            return True
        #Leaderboard
        elif userInput == 2:
            leaderboard = functions.leaderboard()
            #Check if leaderboard is empty or not
            if len(leaderboard) != 0:
                print('Top 5 players:')
                for i, j in enumerate(leaderboard):
                    print(f'{i+1}. {j[0]}: {j[1]} points')
            else:
                print('No scores saved yet.')
            return False
        #Save score
        elif userInput == 3:
            #Get username and password
            username = input('Username: ')
            #This method hides the password when inputting it
            password = getpass.getpass()
            #If the login or signup is successful, save the score
            if functions.login(username, password):
                #Save score
                if functions.updateScore(username, int(score)):
                    print(f'Score saved for {username}!')
                else:
                    print(f'Error saving score.')
            else:
                print('Invalid credentials.')
            return False
        #Reset score
        elif userInput == 4:
            #Get username and password
            username = input('Username: ')
            password = getpass.getpass()
            #If the login was successful, reset the score to 0 without deleting the user
            if functions.login(username, password):
                if functions.resetScore(username):
                    print(f'Score reset for {username}!')
            else:
                print('Invalid credentials.')
            return False
        #Quit
        elif userInput > 4:
            return False

#Clear command depending on the operating system the program is running on
def clearConsole():
    os.system('cls' if os.name=='nt' else 'clear')

#Main function handling the game connection
def playGame():
    #Establish socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        port = 9999
        s.connect(('localhost', port))
        #Welcome message
        print(s.recv(1024).decode('utf-8'))
        state = handleGame(s)
    return state

restart = True
clearConsole()

#Main loop handling the game restart
while restart:
    restart = playGame()
    #If the user wants to play again, clear the console
    if restart:
        clearConsole()