WIDTH = 520
HEIGHT = 610


#GRID

TEST_BOARD = [[0 for x in range(9)] for x in range(9)]
TEST_BOARD_2 = [[8, 2, 0, 1, 5, 4, 3, 9, 6],
                [9, 6, 5, 3, 2, 0, 1, 4, 8],
                [3, 4, 1, 6, 8, 9, 7, 5, 2],
                [5, 9, 3, 4, 6, 8, 2, 7, 1],
                [4, 7, 2, 5, 1, 3, 6, 8, 9],
                [6, 1, 8, 9, 0, 2, 4, 3, 5],
                [7, 8, 6, 2, 3, 5, 9, 1, 4],
                [1, 5, 4, 0, 9, 6, 8, 2, 3],
                [2, 3, 9, 8, 4, 1, 5, 6, 0]]

FINISH_BOARD = [[8, 2, 7, 1, 5, 4, 3, 9, 6],
                [9, 6, 5, 3, 2, 7, 1, 4, 8],
                [3, 4, 1, 6, 8, 9, 7, 5, 2],
                [5, 9, 3, 4, 6, 8, 2, 7, 1],
                [4, 7, 2, 5, 1, 3, 6, 8, 9],
                [6, 1, 8, 9, 7, 2, 4, 3, 5],
                [7, 8, 6, 2, 3, 5, 9, 1, 4],
                [1, 5, 4, 7, 9, 6, 8, 2, 3],
                [2, 3, 9, 8, 4, 1, 5, 6, 7]]

# Colors
BACK_GROUND = (248, 158, 125)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 245, 137)
GREEN = (191, 253, 176)
GREY = (189, 189, 189)
RED = (195, 121, 121)
# Positions

GRID_POS = (20, 10)
GRID_SIZE = (GRID_POS[0], GRID_POS[1], WIDTH - 40, HEIGHT - 130)
CELL_SIZE = 53.333
GRID_SIZE_BY_CELL = CELL_SIZE * 9

