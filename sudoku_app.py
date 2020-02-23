import pygame, sys
from settings import *
from buttons import *
from sudoku_gen import *
import time
import time


class Sudoku:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))

        self.running = True
        self.selected = None
        self.clicked = None
        self.mouse_pos = None
        self.state = "playing"
        self.finished = False
        self.cellChanged = False
        self.playingButton = []

        self.menuButton = []
        self.endButton = []
        self.lockCells = []
        self.incorrectCells = []
        self.font = pygame.font.SysFont("arial", round(CELL_SIZE//2))
        # GRID
        self.the_grid = SudokuGenerator()
        self.grid = self.the_grid.grid
        self.load()

    def run(self):
        while self.running:
            if self.state == "playing":
                self.events()
                self.update()
                self.draw()
        pygame.quit()
        sys.exit()

# PLAYING FUNCTIONS START

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # USER MOUSE CONTROL
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseOnGrid()
                if selected:
                    self.selected = selected
                else:
                    print("NO CELL SELECTED")
                    self.selected = None
                for button in self.endButton:
                    btn_selected = self.mouseOnButton(button)
                    if btn_selected:
                        self.clicked = True
                        self.button_action(btn_selected)
                    else:
                        print('NO button selected')
            # USER NUM INPUT KEY
            if event.type == pygame.KEYDOWN:
                if self.selected is not None and self.selected not in self.lockCells:
                    if self.isInt(event.unicode):
                        # Cell Changed
                        self.grid[self.selected[1]][self.selected[0]] = int(event.unicode)
                        self.cellChanged = True

    def update(self):
        # self.grid = self.the_grid.grid
        self.mouse_pos = pygame.mouse.get_pos()
        for button in self.endButton:
            button.update(self.mouse_pos)
        if self.cellChanged:
            self.incorrectCells = []
            if self.allCellsDone():
                # BOARD CHECK
                self.checkAllCells()
                if len(self.incorrectCells) == 0:
                    self.finished = True
                else:
                    self.finished = False


    def draw(self):
        self.window.fill(BACK_GROUND)
        self.window.fill(WHITE, GRID_SIZE)
        for button in self.endButton:
            button.draw(self.window)
        if self.selected:
            self.drawSelection(self.window, self.selected)

        self.shadeLockCells(self.window)
        self.shadeIncorrectCells(self.window)

        self.drawNumbers(self.window)
        self.drawGrid(self.window)
        if self.finished:
            self.text_to_screen(self.window, "Sudoku is solved!!", [300, 510])
        pygame.display.update()

# PLAYING FUNCTIONS END

    def drawGrid(self, window):
        pygame.draw.rect(window, BLACK, GRID_SIZE, 2)
        for x in range(9):
            for_x = [(GRID_POS[0], GRID_POS[1] + (x * CELL_SIZE)), (GRID_POS[0] + 479, GRID_POS[1] + (x * CELL_SIZE))]
            for_y = [(GRID_POS[0] + (x * CELL_SIZE), GRID_POS[1]), (GRID_POS[0] + (x * CELL_SIZE), GRID_POS[1] + 479)]
            pygame.draw.line(window, BLACK, for_x[0], for_x[1], 2 if x % 3 == 0 else 1)
            pygame.draw.line(window, BLACK, for_y[0], for_y[1], 2 if x % 3 == 0 else 1)

    def mouseOnButton(self, button):
        if self.mouse_pos[0] < button.pos[0] or self.mouse_pos[1] < button.pos[1]:
            return False
        if self.mouse_pos[0] > button.pos[0]+button.rect.width or self.mouse_pos[1] > button.pos[1]+button.rect.height:
            return False

        return button.text

    def mouseOnGrid(self):
        if self.mouse_pos[0] < GRID_POS[0] or self.mouse_pos[1] < GRID_POS[1]:
            return False
        if self.mouse_pos[0] > GRID_POS[0]+GRID_SIZE_BY_CELL or self.mouse_pos[1] > GRID_POS[1]+GRID_SIZE_BY_CELL:
            return False

        selected = (round((self.mouse_pos[0] - GRID_POS[0])//CELL_SIZE), round((self.mouse_pos[1] - GRID_POS[1])//CELL_SIZE))
        return selected

    def drawSelection(self, window, pos):
        pygame.draw.rect(window, GREEN, ((pos[0] * CELL_SIZE) + GRID_POS[0], (pos[1] * CELL_SIZE) + GRID_POS[1], CELL_SIZE, CELL_SIZE))

    def load(self):
        self.loadButtons()
        # Set LOCK CELL where number is 0
        for y_index, row in enumerate(self.grid):
            for x_index, num in enumerate(row):
                if num != 0:
                    self.lockCells.append((x_index, y_index))

    def loadButtons(self):
        # self.playingButton.append(Button(10, 500, 100, 40, "Start"))
        self.endButton.append(Button(10, 500, 100, 40, "Solve"))
        self.endButton.append(Button(10, 560, 100, 40, "Random"))

    def text_to_screen(self, window, text, pos, text_color=BLACK):
        font = self.font.render(text, False, BLACK)
        font_width = font.get_width()
        font_height = font.get_height()
        pos[0] += (CELL_SIZE - font_width)//2
        pos[1] += (CELL_SIZE - font_height)//2
        window.blit(font, pos)

    def timer(self):
        time_string = str(round(pygame.time.get_ticks()/1000)) + 's'
        self.text_to_screen(self.window, time_string, [540, 20])

    def drawNumbers(self, window):
        for y_index, row in enumerate(self.grid):
            for x_index, num in enumerate(row):
                if num != 0:
                    pos = [(x_index * CELL_SIZE) + GRID_POS[0], (y_index * CELL_SIZE) + GRID_POS[1]]
                    self.text_to_screen(window, str(num), pos)

    def shadeLockCells(self, window):
        for cell in self.lockCells:
            pygame.draw.rect(window, GREY, (cell[0] * CELL_SIZE + GRID_POS[0], cell[1] * CELL_SIZE + GRID_POS[1], CELL_SIZE, CELL_SIZE))

    def shadeIncorrectCells(self, window):
        for cell in self.incorrectCells:
            if (cell[0], cell[1]) not in self.lockCells:
                pygame.draw.rect(window, RED, (cell[0] * CELL_SIZE + GRID_POS[0], cell[1] * CELL_SIZE + GRID_POS[1], CELL_SIZE, CELL_SIZE))
            # else:
            #     pygame.draw.rect(window, YELLOW, (cell[0] * CELL_SIZE + GRID_POS[0], cell[1] * CELL_SIZE + GRID_POS[1], CELL_SIZE, CELL_SIZE))

    def isInt(self, string):
        try:
            int(string)
            return True
        except:
            return False

    ## BOARD CHECK FUNCTION

    def allCellsDone(self):
        for row in self.grid:
            for num in row:
                if num == 0:
                    return False
        return True

    def checkAllCells(self):
        self.checkRows()
        self.checkCols()
        self.checkSmallGrid()



    def checkRows(self):
        for y_index, row in enumerate(self.grid):
            possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for x_index in range(9):
                if self.grid[y_index][x_index] in possibles:
                    possibles.remove(self.grid[y_index][x_index])
                else:
                    if [x_index, y_index] not in self.lockCells and [x_index, y_index] not in self.incorrectCells:
                        self.incorrectCells.append([x_index, y_index])

    def checkCols(self):
        for row_index in range(9):
            possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for y_index, row in enumerate(self.grid):
                if self.grid[y_index][row_index] in possibles:
                    possibles.remove(self.grid[y_index][row_index])
                else:
                    if [row_index, y_index] not in self.lockCells and [row_index, y_index] not in self.incorrectCells:
                        self.incorrectCells.append([row_index, y_index])

    def checkSmallGrid(self):
        for x in range(3):
            for y in range(3):
                possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                for i in range(3):
                    for j in range(3):
                        # print(x*3+i, y*3+j)
                        x_index, y_index = x*3+i, y*3+j
                        if self.grid[x_index][y_index] in possibles:
                            possibles.remove(self.grid[x_index][y_index])
                        else:
                            if [x_index, y_index] not in self.lockCells and [x_index, y_index] not in self.incorrectCells:
                                self.incorrectCells.append([x_index, y_index])


    def button_action(self, btn_name):
        if btn_name == "Solve":
            self.grid_solve()
            self.finished = True
        elif btn_name == "Random":
            self.finished = False
            self.the_grid.getGridApi(1)
            self.grid = self.the_grid.grid
            self.lockCells = []
            self.window.fill(BACK_GROUND)
            for y_index, row in enumerate(self.grid):
                for x_index, num in enumerate(row):
                    if num != 0:
                        self.lockCells.append((x_index, y_index))


    """ ---------------------------BACK TRACKING ALGORITHM ----------------------------------- """

    def grid_solve(self):
        find = self.find_empty()
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.valid_grid(i, (row, col)):
                self.grid[row][col] = i
                if self.grid_solve():  # after adding the value ('i') check again if the grid is valid
                    return True
                self.grid[row][col] = 0  # reset the value to to backtrack
                # time.sleep(0.001)
        return False

    def find_empty(self):
        for row in range(len(self.grid)):
            for cell in range(len(self.grid[0])):
                if self.grid[row][cell] == 0:
                    tpl = (row, cell)
                    return tpl

    def valid_grid(self, num, pos):
        #  Check the row
        for i in range(len(self.grid[0])):
            if self.grid[pos[0]][i] == num and pos[1] != i:  # "pos[1] != i"  ignore the recent inserted position
                return False

        # Check the column
        for i in range(len(self.grid)):
            if self.grid[i][pos[1]] == num and pos[0] != i:  # "pos[1] != i"  ignore the recent inserted position
                return False

        # Small 3x3 grid check
        box_row = pos[1] // 3
        box_col = pos[0] // 3

        for i in range(box_col * 3, box_col * 3 + 3):
            for j in range(box_row * 3, box_row * 3 + 3):
                if self.grid[i][j] == num and (i, j) != pos:
                    return False

        return True
