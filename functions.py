import json
import random
import sqlite3

#Initialize database
def setupDB():
    connection = sqlite3.connect('quiz.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS quiz (username TEXT, password TEXT, highScore INTEGER)')
    connection.commit()
    connection.close()

#Get a random country
def getCountry():
    with open("quiz.json") as f:
        data = json.load(f)
    country = random.choice(list(data.keys()))
    return country

#Get the capital of the given country
def getCapital(country: str):
    with open("quiz.json") as f:
        data = json.load(f)
    return data[country]['capital']

#Get the continent of the given country
def getContinent(country: str):
    with open("quiz.json") as f:
        data = json.load(f)
    return data[country]['continent']

#Construct a question with the given country
def getQuestion(country: str):
    correctAnswer = country
    options = [correctAnswer]
    #Get 3 random additional countries, and add them to the options list
    while len(options) <= 3:
        newCountry = getCountry()
        if newCountry not in options and newCountry != correctAnswer:
            options.append(newCountry)
    #Shuffle the options list
    random.shuffle(options)
    return options

#Check if the given answer is correct
def checkAnswer(answer: str, correctAnswer: str):
    if answer.lower() == correctAnswer.lower():
        return True
    else:
        return False

#Return the top 5 scoring players' usernames and scores
def leaderboard():
    connection = sqlite3.connect('quiz.db')
    cursor = connection.cursor()
    cursor.execute('SELECT username, highScore FROM quiz ORDER BY highScore DESC LIMIT 5')
    result = cursor.fetchall()
    connection.close()
    return result

#Combined login and register function
def login(username: str, password: str):
    connection = sqlite3.connect('quiz.db')
    cursor = connection.cursor()
    cursor.execute('SELECT username, password FROM quiz WHERE username=?', (username,))
    result = cursor.fetchone()
    #If the username doesn't exist, create a new user
    if result is None:
        cursor.execute('INSERT INTO quiz VALUES (?, ?, ?)', (username, password, 0))
        connection.commit()
        connection.close()
        return True
    #If it does exist, check if the password is correct or not
    else:
        if result[1] == password:
            connection.close()
            return True
        else:
            connection.close()
            return False

#Update the user's high score
def updateScore(username: str, score: int):
    connection = sqlite3.connect('quiz.db')
    cursor = connection.cursor()
    cursor.execute('SELECT highScore FROM quiz WHERE username=?', (username,))
    result = cursor.fetchone()
    if result is not None:
        currentScore = result[0]
        #Choose the bigger score: the currently stored high score or the score from the game
        newScore = max(score, currentScore)
        cursor.execute('UPDATE quiz SET highScore=? WHERE username=?', (newScore, username))
        connection.commit()
        connection.close()
        return True
    else:
        connection.close()
        return False

#Reset the user's high score to 0, if the user exists
def resetScore(username: str):
    connection = sqlite3.connect('quiz.db')
    cursor = connection.cursor()
    cursor.execute('SELECT username FROM quiz WHERE username=?', (username,))
    result = cursor.fetchone()
    if result is not None:
        cursor.execute('UPDATE quiz SET highScore=? WHERE username=?', (0, username))
        connection.commit()
        connection.close()
        return True
    else:
        connection.close()
        return False