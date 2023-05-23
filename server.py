import functions
import json
import socket
import threading

def handleClient(client, address):
    points = 0
    client.sendall('Welcome to the quiz game'.encode('utf-8'))
    while True:
        country = functions.getCountry()
        capital = functions.getCapital(country)
        question = f'Which countries capital city is {capital}?'
        client.sendall(question.encode('utf-8'))
        options = functions.getQuestion(country)
        client.sendall(json.dumps(options).encode('utf-8'))
        try:
            answer = client.recv(4096).decode('utf-8')
        except UnicodeDecodeError:
            break
        if functions.checkAnswer(answer, country):
            client.sendall('Correct answer!'.encode('utf-8'))
            points += 2
            #print(f'Client {address} has {points} points')
            continue
        else:
            client.sendall('Incorrect answer. Do you want a hint?'.encode('utf-8'))
            hint = client.recv(1024).decode('utf-8')
            if hint.lower() == 'yes' or hint.lower() == 'y':
                continent = functions.getContinent(country)
                client.sendall(f'The country is located in {continent}.'.encode('utf-8'))
                try:
                    hintAnswer = client.recv(1024).decode('utf-8')
                except UnicodeDecodeError:
                    break
                if functions.checkAnswer(hintAnswer, country):
                    client.sendall('Correct answer!'.encode('utf-8'))
                    points += 1
                    #print(f'Client {address} has {points} points')
                    continue
                else:
                    client.sendall(f'Incorrect answer. The correct answer was {country}! Your score: {points}'.encode('utf-8'))
                    client.close()
                    break
            else:
                client.sendall(f'Thanks for playing! Your score: {points}'.encode('utf-8'))
                client.close()
                break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    port = 9999
    s.bind(('localhost', port))
    s.listen()
    print(f'Listening on port {port}')
    functions.initDB()
    while True:
        client, address = s.accept()
        thread = threading.Thread(target=handleClient, args=(client, address))
        thread.start()