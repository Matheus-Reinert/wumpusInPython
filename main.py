import random


def right(maze, row, column):
    return maze[row][column + 1]


def left(maze, row, column):
    return maze[row][column - 1]


def up(maze, row, column):
    return maze[row + 1][column]


def down(maze, row, column):
    return maze[row - 1][column]


def choose_character(actor):
    if actor == "w":
        return "_"
    if actor == "h":
        return "~"
    if actor == "g":
        return "!"


def generate_maze(rows, columns):
    maze = [[0 for _ in range(columns)] for _ in range(rows)]

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            maze[i][j] = "*"

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            maze[0][j] = "#"
            maze[i][0] = "#"
            maze[rows - 1][j] = "#"
            maze[i][columns - 1] = "#"

    return maze


def generate_sides_of_actor(maze, row, column, actor):
    character_that_represent_actor_sides = choose_character(actor)

    if right(maze, row, column) == "*":
        maze[row][column + 1] = character_that_represent_actor_sides
    if left(maze, row, column) == "*":
        maze[row][column - 1] = character_that_represent_actor_sides
    if up(maze, row, column) == "*":
        maze[row + 1][column] = character_that_represent_actor_sides
    if down(maze, row, column) == "*":
        maze[row - 1][column] = character_that_represent_actor_sides


def generate_actors_positions(maze, rows, columns, actors_in_maze, index):
    actor_position_row = random.randint(1, rows - 1)
    actor_position_column = random.randint(1, columns - 1)
    actor = actors_in_maze[index]

    if actor_position_row >= rows or actor_position_column >= columns:
        generate_actors_positions(maze, rows, columns, actors_in_maze, index)
    else:
        if maze[actor_position_row][actor_position_column] == "*" and index < len(actors_in_maze):
            maze[actor_position_row][actor_position_column] = actor
            generate_sides_of_actor(maze, actor_position_row, actor_position_column, actor)
            if index < len(actors_in_maze) - 1:
                generate_actors_positions(maze, rows, columns, actors_in_maze, index + 1)
        else:
            generate_actors_positions(maze, rows, columns, actors_in_maze, index)


def generate_world():
    index = 0
    rows = random.randint(5, 10)
    columns = random.randint(5, 10)
    actors_in_maze = ['h', 'w', 'g']

    maze = generate_maze(rows, columns)
    generate_actors_positions(maze, rows, columns, actors_in_maze, index)
    maze[1][1] = "p"

    return maze


def find_possible_moves(maze):
    rows = len(maze)
    columns = len(maze[0])
    possible_moves = [[0 for _ in range(columns)] for _ in range(rows)]

    for i in range(rows):
        for j in range(columns):
            if maze[i][j] == "#":
                possible_moves[i][j] = "false"
            else:
                possible_moves[i][j] = "true"

    return possible_moves


def find_origin_or_destine(param, maze):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if param == "origin" and maze[i][j] == "p":
                return i, j
            if param == "destine" and maze[i][j] == "g":
                return i, j


class Stack:
    def __init__(self):
        self.items = []

    def isNotEmpty(self):
        return self.items != []

    def push(self, item):
        self.items.insert(0, item)

    def pop(self):
        return self.items.pop(0)

    def peek(self):
        return self.items[0]

    def size(self):
        return len(self.items)


def arrive_in_gold(maze, current_position, dest, possible_moves):
    return maze[current_position[0]][current_position[1]] == maze[dest[0]][dest[1]] \
           and possible_moves[current_position[0]][current_position[1]] == "true"


def walking(stack, maze, current_position, dest, possible_moves):
    if arrive_in_gold(maze, current_position, dest, possible_moves):
        print("Parabéns")
        stack.pop()
        return True

    elif down(maze, current_position[0], current_position[1]) != "p" and down(possible_moves, current_position[0],
                                                                              current_position[1]) == "true":
        maze[current_position[0] - 1][current_position[1]] = "p"
        current_position = current_position[0] - 1, current_position[1]
        stack.push(current_position)
        walking(stack, maze, current_position, dest, possible_moves)

    elif right(maze, current_position[0], current_position[1]) != "p" and right(possible_moves, current_position[0],
                                                                                current_position[1]) == "true":
        maze[current_position[0]][current_position[1] + 1] = "p"
        current_position = current_position[0], current_position[1] + 1
        stack.push(current_position)

        walking(stack, maze, current_position, dest, possible_moves)

    elif left(maze, current_position[0], current_position[1]) != "p" and left(possible_moves, current_position[0],
                                                                              current_position[1]) == "true":
        maze[current_position[0]][current_position[1] - 1] = "p"
        current_position = current_position[0], current_position[1] - 1
        stack.push(current_position)
        walking(stack, maze, current_position, dest, possible_moves)

    elif up(maze, current_position[0], current_position[1]) != "p" and up(possible_moves, current_position[0],
                                                                          current_position[1]) == "true":
        maze[current_position[0] + 1][current_position[1]] = "p"
        current_position = current_position[0] + 1, current_position[1]
        stack.push(current_position)
        walking(stack, maze, current_position, dest, possible_moves)


    else:
        stack.pop()

    return False


def dfs(maze, origin, dest, possible_moves):
    stack = Stack()
    stack.push(origin)
    current_position = origin

    while stack.isNotEmpty():
        finish = walking(stack, maze, current_position, dest, possible_moves)
        if finish:
            print("Saída encontrada")
        else:
            stack.pop()
            print("Fim")
        break


def main():
    maze = generate_world()
    possible_moves = find_possible_moves(maze)
    origin = find_origin_or_destine("origin", maze)
    dest = find_origin_or_destine("destine", maze)
    dfs(maze, origin, dest, possible_moves)
    print(origin)
    print(dest)

    for row in maze:
        print(row)

    print("\n")

    for row in possible_moves:
        print(row)



main()
