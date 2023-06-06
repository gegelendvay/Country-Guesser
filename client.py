import functions
import getpass
import json
import os
import socket

def handleGame(score: int):
        #If the game is over, provide the user with different options to choose from
    print('[1]Play Again\n[2]Leaderboard\n[3]Save Score\n[4]Reset Score\n[5]Quit')
    userInput = input()
        #If the input is not a number, end the game and close the connection
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

restart = True
score = 0
clearConsole()

while restart:
    #Establish socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        port = 9999
        s.connect(('localhost', port))
        #Welcome
        print(s.recv(1024).decode('utf-8'))
        while True:
            #Question
            print(s.recv(4096).decode('utf-8'))
            try:
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
                response = s.recv(1024).decode('utf-8')
                print(response)
                score = int(response.split(': ', 1)[1])
                restart = False
                break
    #Send the score to the handleGame function, which will return a boolean value
    restart = handleGame(score)
s.close()