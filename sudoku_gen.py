from random import randint, shuffle, random
import requests
import time

class SudokuGenerator:
    def __init__(self):
        self.grid = [[0 for x in range(9)] for x in range(9)]
        self.get_board_api = "https://sugoku.herokuapp.com/board"  # ?difficulty=
        self.get_solved_api = "https://sugoku.herokuapp.com/solve"
        self.difficulties = ['easy', 'medium', 'hard', 'random']
        self.getGridApi(1)  # FILLS the self.grid

        self.unsolved_data = None
        self.solved_data = None


    def getGridApi(self, level):
        # 3 level will be random difficulty
        # defining a params dict for the parameters to be sent to the API
        params = {'difficulty': self.difficulties[level]}
        # sending get request and saving the response as response object
        r = requests.get(url=self.get_board_api, params=params)
        if r.reason == 'OK':
            self.unsolved_data = r.json()
            self.grid = []
            for row in self.unsolved_data['board']:
                self.grid.append(row)
        # extracting data in json format
