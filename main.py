import random
import sys

from nbinput import BlockingInput


class Maze:
    def __init__(self, width, height):
        self.width = 1 + 2 * int(width / 2)
        self.height = 1 + 2 * int(height / 2)
        self.end = (self.width - 2, self.height - 2)
        self.generate()

    def __str__(self):
        return self.string()
        
    def string(self, objs={}):
        h_border = '+' + ('-' * (self.width * 2 + 1)) + '+\n' 
        string = h_border
        for y, row in enumerate(self.maze):
            string += '|'
            for x, cell in enumerate(row):
                string += ' '
                try:
                    string += objs[(x, y)]
                except KeyError:
                    string += '#' if cell else ' '
            string += ' |\n'
        string += h_border
        return string

    def generate(self):
        space = lambda x, y: ((x % 2) and (y % 2))
        wall = lambda x, y: ((x % 2) and not (y % 2)) or (not (x % 2) and (y % 2))
        self.maze = [[not (space(x, y) or (wall(x, y) and random.randint(0, 1))) or (x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1) for x in range(self.width)] for y in range(self.height)]

        if not self.solve():
            self.generate()

    def solve(self, coord=(1, 1), prev=False):
        x, y = coord
        
        if coord == self.end:
            return True

        if not prev:
            self.prev = []
        self.prev.append(coord)

        solved = False
        for d in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            x1, y1 = x + d[0], y + d[1]
            x2, y2 = x1 + d[0], y1 + d[1]
            
            if x2 >= 0 and x2 < len(self.maze[0]) and y2 >= 0 and y2 < len(self.maze) and not self.maze[y1][x1] and (x2, y2) not in self.prev:
                solved = self.solve((x2, y2), True)
            if solved:
                break
        return solved


def play(maze):
    solved = False
    x, y = (1, 1)
    with BlockingInput() as bi:
        while not (x, y) == maze.end:
            print(maze.string({(x, y): 'X'}))
            dx, dy = (0, 0)
            c = bi.char()
            if c in 'aA':
                dx = -1
            elif c in 'dD':
                dx = 1
            elif c in 'wW':
                dy = -1
            elif c in 'sS':
                dy = 1
            x += dx * (not maze.maze[y][x + dx])
            y += dy * (not maze.maze[y + dy][x])
    print(maze.string({(x, y): 'X'}))
    print('Completed!')


def main():
    x, y = (int(n) for n in sys.argv[1:3])
    
    maze = Maze(x, y)
    print(maze)
    play(maze)


if __name__ == '__main__':
    main()
