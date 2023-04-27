import json
import random

def getCountry():
    with open("quiz.json") as f:
        data = json.load(f)
    country = random.choice(list(data.keys()))
    return country

def getCapital(country):
    with open("quiz.json") as f:
        data = json.load(f)
    return data[country]['capital']

def getContinent(country):
    with open("quiz.json") as f:
        data = json.load(f)
    return data[country]['continent']

def getQuestion(country):
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

def checkAnswer(answer, correctAnswer):
    if answer.lower() == correctAnswer.lower():
        return True
    else:
        return False