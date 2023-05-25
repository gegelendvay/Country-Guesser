import functions
import json
import socket
import os
import getpass

highScore = 0

#functions.register('Joe', '1234')

def handleGame(score: int):
    global highScore
    print('[1]Play Again\n[2]Leaderboard\n[3]Login/Register to save score\n[4]Quit')
    userInput = input()
    if not userInput.isdigit():
        return False
    
    if score > highScore:
        highScore = score

    userInput = int(userInput)
    if userInput == 1:
        return True
    elif userInput == 2:
        print(functions.leaderboard())
        return False
    elif userInput == 3:
        clearConsole()
        username = input('Username: ')
        #password = input('Password: ')
        password = getpass.getpass()
        if functions.login(username, password):
            functions.updateScore(username, highScore)
        else:
            print('Login failed!')
        return False
    elif userInput == 4 or userInput > 4:
        return False
    
def clearConsole():
    os.system('cls' if os.name=='nt' else 'clear')

restart = True
score = 0
#clearConsole()

while restart:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        port = 9990
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
    restart = handleGame(score)
    #clearConsole()
s.close()