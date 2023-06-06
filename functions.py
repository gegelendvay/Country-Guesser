import json
import random
import sqlite3
    
def setupDB():
    connection = sqlite3.connect('quiz.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS quiz (username TEXT, password TEXT, highScore INTEGER)')
    connection.commit()
    connection.close()

def getCountry():
    with open("quiz.json") as f:
        data = json.load(f)
    country = random.choice(list(data.keys()))
    return country

def getCapital(country: str):
    with open("quiz.json") as f:
        data = json.load(f)
    return data[country]['capital']

def getContinent(country: str):
    with open("quiz.json") as f:
        data = json.load(f)
    return data[country]['continent']

def getQuestion(country: str):
    with open("quiz.json") as f:
        data = json.load(f)
    
    correctAnswer = country
    options = [correctAnswer]
    while len(options) <= 3:
        newCountry = getCountry()
        if newCountry not in options and newCountry != correctAnswer:
            options.append(newCountry)
    random.shuffle(options)
    return options

def checkAnswer(answer: str, correctAnswer: str):
    if answer.lower() == correctAnswer.lower():
        return True
    else:
        return False

def leaderboard():
    connection = sqlite3.connect('quiz.db')
    cursor = connection.cursor()
    cursor.execute('SELECT username, highScore FROM quiz ORDER BY highScore DESC LIMIT 5')
    result = cursor.fetchall()
    connection.close()
    return result
    
def login(username: str, password: str):
    connection = sqlite3.connect('quiz.db')
    cursor = connection.cursor()
    cursor.execute('SELECT username, password FROM quiz WHERE username=?', (username,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute('INSERT INTO quiz VALUES (?, ?, ?)', (username, password, 0))
        connection.commit()
        connection.close()
        return True
    else:
        if result[1] == password:
            connection.close()
            return True
        else:
            connection.close()
            return False

def updateScore(username: str, score: int):
    connection = sqlite3.connect('quiz.db')
    cursor = connection.cursor()
    cursor.execute('SELECT highScore FROM quiz WHERE username=?', (username,))
    result = cursor.fetchone()
    if result is not None:
        currentScore = result[0]
        newScore = max(score, currentScore)
        cursor.execute('UPDATE quiz SET highScore=? WHERE username=?', (newScore, username))
        connection.commit()
        connection.close()
        return True
    else:
        connection.close()
        return False

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