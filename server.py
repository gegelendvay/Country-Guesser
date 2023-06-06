import functions
import json
import socket
import threading

def handleClient(client, address):
    #Initialize the game
    points = 0
    client.sendall('Welcome to the country quiz game!'.encode('utf-8'))

    while True:
        #Get a random country and its capital
        country = functions.getCountry()
        capital = functions.getCapital(country)
        #Send the question and the options to the client
        question = f'Which country\'s capital city is {capital}?'
        client.sendall(question.encode('utf-8'))

        options = functions.getQuestion(country)
        client.sendall(json.dumps(options).encode('utf-8'))

        try:
            answer = client.recv(4096).decode('utf-8')
        except UnicodeDecodeError:
            break

        #Compare the given answer with the correct answer
        if functions.checkAnswer(answer, country):
            client.sendall('Correct answer!'.encode('utf-8'))
            #Add 2 points to the score
            points += 2
        else:
        #If the answer is incorrect, ask the user if they want a hint or not
            client.sendall('Incorrect answer. Do you want a hint?'.encode('utf-8'))
            hint = client.recv(1024).decode('utf-8')
            if hint.lower() == 'yes' or hint.lower() == 'y':
                #If the user wants a hint, send the continent to the client
                continent = functions.getContinent(country)
                client.sendall(f'The country is located in {continent}.'.encode('utf-8'))
                try:
                    hintAnswer = client.recv(1024).decode('utf-8')
                except UnicodeDecodeError:
                    break
                #Compare the given answer with the correct answer
                if functions.checkAnswer(hintAnswer, country):
                    client.sendall('Correct answer!'.encode('utf-8'))
                    #Add 1 point to the score if the answer is correct with the use of a hint
                    points += 1
                else:
                    #If the answer is incorrect, end the game
                    client.sendall(f'Incorrect answer. The correct answer was {country}! Your score: {points}'.encode('utf-8'))
                    client.close()
                    break
            else:
                #If the user doesn't want a hint, send the score to the client and end the game
                client.sendall(f'Thanks for playing! Your score: {points}'.encode('utf-8'))
                client.close()
                break

#Open a socket and listen for traffic
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    port = 9999
    s.bind(('localhost', port))
    s.listen()
    print(f'Listening on port {port}')
    #Initialize the database
    functions.setupDB()
    while True:
        client, address = s.accept()
        #Start a new thread for each client connection
        thread = threading.Thread(target=handleClient, args=(client, address))
        thread.start()