# Country quiz game

Source code for Gege's country guessing quiz game made with Python.

## Start the game
Start the game by running the commands `python server.py` and `python client.py` in a terminal opened within the project directory.

## Guide
You will be asked to input the country you think the requested capital belongs to. The game will last until you fail to guess the correct country, even with a hint provided.

Once the game ended, you are given 5 options to choose from:

1. Play Again: Your console gets cleared, and a new game starts
2. Leaderboard: The top 5 scoring players will be displayed
3. Save Score: Choose this option to save your score to the database. You will be asked to provide a username and a password. If the given username does not exist, a new user will be registered
4. Reset Score: This option lets you reset your high score to 0 while keeping your account
5. Quit: Quits the game

## Requirements
Other than an up-to-date Python, you will need to install `sqlite3`. Every other package you see in the project comes with Python by default.