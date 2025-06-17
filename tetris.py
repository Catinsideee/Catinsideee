# Simple Tetris implementation using curses
import curses
import random

WIDTH = 10
HEIGHT = 20

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1],
     [1, 1]],
    [[0, 1, 0],
     [1, 1, 1]],
    [[1, 0, 0],
     [1, 1, 1]],
    [[0, 0, 1],
     [1, 1, 1]],
    [[1, 1, 0],
     [0, 1, 1]],
    [[0, 1, 1],
     [1, 1, 0]]
]

class Piece:
    def __init__(self, shape):
        self.shape = shape
        self.x = WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Tetris:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.board = [[0] * WIDTH for _ in range(HEIGHT)]
        self.piece = self.new_piece()
        self.game_over = False
        self.score = 0

    def new_piece(self):
        return Piece(random.choice(SHAPES))

    def check_collision(self, px, py, shape=None):
        if shape is None:
            shape = self.piece.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    bx, by = px + x, py + y
                    if bx < 0 or bx >= WIDTH or by < 0 or by >= HEIGHT:
                        return True
                    if self.board[by][bx]:
                        return True
        return False

    def place_piece(self):
        for y, row in enumerate(self.piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.piece.y + y][self.piece.x + x] = cell
        self.clear_lines()
        self.piece = self.new_piece()
        if self.check_collision(self.piece.x, self.piece.y):
            self.game_over = True

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines_cleared = HEIGHT - len(new_board)
        for _ in range(lines_cleared):
            new_board.insert(0, [0] * WIDTH)
        self.board = new_board
        self.score += lines_cleared

    def move(self, dx, dy):
        new_x = self.piece.x + dx
        new_y = self.piece.y + dy
        if not self.check_collision(new_x, new_y):
            self.piece.x = new_x
            self.piece.y = new_y
        elif dy:
            self.place_piece()

    def rotate_piece(self):
        new_shape = [list(row) for row in zip(*self.piece.shape[::-1])]
        if not self.check_collision(self.piece.x, self.piece.y, new_shape):
            self.piece.shape = new_shape

    def draw(self):
        self.stdscr.clear()
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                ch = '#' if cell else '.'
                self.stdscr.addch(y, x, ch)
        for y, row in enumerate(self.piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.stdscr.addch(self.piece.y + y, self.piece.x + x, '#')
        self.stdscr.addstr(0, WIDTH + 2, f'Score: {self.score}')
        if self.game_over:
            self.stdscr.addstr(HEIGHT//2, WIDTH//2 - 4, 'GAME OVER')
        self.stdscr.refresh()

    def drop(self):
        if not self.check_collision(self.piece.x, self.piece.y + 1):
            self.piece.y += 1
        else:
            self.place_piece()

    def run(self):
        self.stdscr.nodelay(True)
        while not self.game_over:
            self.draw()
            try:
                key = self.stdscr.getch()
            except curses.error:
                key = -1
            if key == curses.KEY_LEFT:
                self.move(-1, 0)
            elif key == curses.KEY_RIGHT:
                self.move(1, 0)
            elif key == curses.KEY_DOWN:
                self.move(0, 1)
            elif key == curses.KEY_UP:
                self.rotate_piece()
            self.drop()
            curses.napms(300)
        self.draw()
        self.stdscr.nodelay(False)
        self.stdscr.getch()


def main(stdscr):
    curses.curs_set(0)
    t = Tetris(stdscr)
    t.run()

if __name__ == '__main__':
    curses.wrapper(main)
