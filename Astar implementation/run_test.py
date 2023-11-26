from astar import AStar
import sys
import math
import unittest

def make_maze(w=30, h=30):
    from random import shuffle, randrange
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+--"] * w + ['+'] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                hor[max(y, yy)][x] = "+  "
            if yy == y:
                ver[y][max(x, xx)] = "   "
            walk(xx, yy)

    walk(randrange(w), randrange(h))
    result = ''
    for (a, b) in zip(hor, ver):
        result = result + (''.join(a + ['\n'] + b)) + '\n'
    return result.strip()


def drawmaze(maze, set1=[], set2=[], c='#', c2='*'):
    set1 = list(set1)
    set2 = list(set2)
    lines = maze.strip().split('\n')
    width = len(lines[0])
    height = len(lines)
    result = ''
    for j in range(height):
        for i in range(width):
            if (i, j) in set1:
                result = result + c
            elif (i, j) in set2:
                result = result + c2
            else:
                result = result + lines[j][i]
        result = result + '\n'
    return result


class MazeSolver(AStar):

    def __init__(self, maze):
        self.lines = maze.strip().split('\n')
        self.width = len(self.lines[0])
        self.height = len(self.lines)

    def heuristic_cost_estimate(self, n1, n2):
        #computes the 'direct' distance between two (x,y) tuples
        (x1, y1) = n1
        (x2, y2) = n2
        return math.hypot(x2 - x1, y2 - y1)

    def distance_between(self, n1, n2):
        #this method always returns 1, as two 'neighbors' are always adajcent
        return 1

    def neighbors(self, node):
        #for a given coordinate in the maze, returns up to 4 adjacent(north,east,south,west) nodes that can be reached (=any adjacent coordinate that is not a wall)
        x, y = node
        return[(nx, ny) for nx, ny in[(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]if 0 <= nx < self.width and 0 <= ny < self.height and self.lines[ny][nx] == ' ']

def solve_maze():
	size = 20
	m = make_maze(size, size)

	w = len(m.split('\n')[0])
	h = len(m.split('\n'))

	start = (1, 1)  # start at the upper left corner
	goal = (w - 2, h - 2)  # the goal is in the lower right corner

	# let's solve it
	foundPath = list(MazeSolver(m).astar(start, goal))

	return drawmaze(m, list(foundPath))

class MazeTests(unittest.TestCase):
	def test_solve_maze(self):
		solve_maze()

if __name__ == '__main__':
	print(solve_maze())

