import functions
import json
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    port = 9999
    s.connect(('localhost', port))
    print(f'Connected to port {port}')
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
            print(s.recv(1024).decode('utf-8'))
            break
s.close()