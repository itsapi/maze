import random
import sys


class Maze:
    def __init__(self, width, height):
        self.width = 1 + 2 * int(width / 2)
        self.height = 1 + 2 * int(height / 2)
        self.generate()

    def __str__(self):
        return '+' + ('-' * (self.width * 2 + 1)) + '+\n' + '\n'.join('| ' + ' '.join('#' if cell else ' ' for cell in row) + ' |' for row in self.maze) + '\n+' + ('-' * (self.width * 2 + 1)) + '+'

    def generate(self):
        space = lambda x, y: ((x % 2) and (y % 2))
        wall = lambda x, y: ((x % 2) and not (y % 2)) or (not (x % 2) and (y % 2))
        self.maze = [[not (space(x, y) or (wall(x, y) and random.randint(0, 1))) for x in range(self.width)] for y in range(self.height)]

        if not self.solve((self.width - 2, self.height - 2)):
            self.generate()

    def solve(self, end, coord=(1, 1), prev=False):
        x, y = coord
        
        if coord == end:
            return True

        if not prev:
            self.prev = []
        self.prev.append(coord)

        solved = False
        for d in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            x1, y1 = x + d[0], y + d[1]
            x2, y2 = x1 + d[0], y1 + d[1]
            
            if x2 >= 0 and x2 < len(self.maze[0]) and y2 >= 0 and y2 < len(self.maze) and not self.maze[y1][x1] and (x2, y2) not in self.prev:
                solved = self.solve(end, (x2, y2), True)
            if solved:
                break
        return solved


def main():
    x, y = (int(n) for n in sys.argv[1:3])
    
    maze = Maze(x, y)
    print(maze)
    solved = maze.solve((len(maze.maze[0])-2, len(maze.maze)-2))


if __name__ == '__main__':
    main()
