import functions
import json
import socket
import os

score = 0
highScore = 0

functions.register('Joe', '1234')

def handleGame():
    global highScore
    print('[1]Play Again\n[2]Leaderboard\n[3]Login\n[4]Register\n[5]Quit')
    userInput = input()
    if not userInput.isdigit():
        return False

    userInput = int(userInput)
    if userInput == 1:
        return True
    elif userInput == 2:
        print(functions.leaderboard())
        return False
    elif userInput == 3:
        username = input('Enter your username: ')
        password = input('Enter your password: ')
        if functions.login(username, password):
            print('Login successful!')
            highScore = functions.getHighScore(username)
            functions.updateScore(username, highScore)
            return True
        else:
            print('Login failed!')
            return False
    elif userInput == 4:
        username = input('Enter your username: ')
        password = input('Enter your password: ')
        functions.register(username, password)
        return False
    elif userInput == 5 or userInput > 5:
        return False
    
def clearConsole():
    os.system('cls' if os.name=='nt' else 'clear')

restart = True
clearConsole()

while restart:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        port = 9999
        s.connect(('localhost', port))
        #print(f'Connected to port {port}')
        welcome = s.recv(1024).decode('utf-8')
        print(welcome)
        while True:
            #Question
            question = s.recv(4096).decode('utf-8')
            print(question)
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
                continent = s.recv(1024).decode('utf-8')
                print(continent)
                answer = input('Enter your answer: ')
                s.sendall(answer.encode('utf-8'))
                response = s.recv(1024).decode('utf-8')
                print(response)
            else:
                result = s.recv(1024).decode('utf-8')
                print(result)
                score = result.split(': ', 1)[1]
                restart = False
                break
    restart = handleGame()
    clearConsole()
s.close()