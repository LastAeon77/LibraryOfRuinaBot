import random
from copy import deepcopy

random.seed()


def start():  # returns a new grid
    t = 2
    t2 = 2
    if random.randint(0, 99) < 10:
        t = 4
    if random.randint(0, 99) < 10:
        t2 = 4
    grid = [[0, 0, 0, 0], [0, t2, 0, 0], [0, 0, 0, 0], [0, 0, t, 0]]
    for subgrid in grid:
        random.shuffle(subgrid)
    random.shuffle(grid)
    return grid


def left(z):  # moves objects in 2048 grid left
    g = deepcopy(z)
    for stuff in g:
        for sdfwf in range(3):
            for x in range(len(stuff) - 1):
                if stuff[x] == 0:
                    stuff[x] = stuff[x + 1]
                    stuff[x + 1] = 0
        for x in range(len(stuff) - 1):
            if stuff[x] == stuff[x + 1]:
                stuff[x] *= 2
                stuff[x + 1] = 0
        for sdfwf in range(3):
            for x in range(len(stuff) - 1):
                if stuff[x] == 0:
                    stuff[x] = stuff[x + 1]
                    stuff[x + 1] = 0
    return g


def right(z):
    g = deepcopy(z)
    for stuff in g:
        for sdfwf in range(3):
            for x in range(len(stuff) - 1, 0, -1):
                if stuff[x] == 0:
                    stuff[x] = stuff[x - 1]
                    stuff[x - 1] = 0
        for x in range(len(stuff) - 1, 0, -1):
            if stuff[x] == stuff[x - 1]:
                stuff[x] *= 2
                stuff[x - 1] = 0
        for sdfwf in range(3):
            for x in range(len(stuff) - 1, 0, -1):
                if stuff[x] == 0:
                    stuff[x] = stuff[x - 1]
                    stuff[x - 1] = 0
    return g


def up(z):
    g = deepcopy(z)
    for index in range(4):
        for sdfwf in range(3):
            for x in range(len(g[index]) - 1):
                if g[x][index] == 0:
                    g[x][index] = g[x + 1][index]
                    g[x + 1][index] = 0
        for x in range(len(g[index]) - 1):
            if g[x][index] == g[x + 1][index]:
                g[x][index] *= 2
                g[x + 1][index] = 0
        for sdfwf in range(3):
            for x in range(len(g[index]) - 1):
                if g[x][index] == 0:
                    g[x][index] = g[x + 1][index]
                    g[x + 1][index] = 0
    return g


def down(z):
    g = deepcopy(z)
    for index in range(4):
        for sdfwf in range(3):
            for x in range(len(g[index]) - 1, 0, -1):
                if g[x][index] == 0:
                    g[x][index] = g[x - 1][index]
                    g[x - 1][index] = 0
        for x in range(len(g[index]) - 1, 0, -1):
            if g[x][index] == g[x - 1][index]:
                g[x][index] *= 2
                g[x - 1][index] = 0
        for sdfwf in range(3):
            for x in range(len(g[index]) - 1, 0, -1):
                if g[x][index] == 0:
                    g[x][index] = g[x - 1][index]
                    g[x - 1][index] = 0
    return g


def gameOver(g):  # Check if game is over
    if up(g) == g and down(g) == g and right(g) == g and left(g) == g:
        return True
    return False


def win(g):  # Check if player won
    if 2048 in g:
        return True
    return False


# nums = {
#     0: Image.open("./data/2048Game/0.png").resize((50, 50)),
#     2: Image.open("./data/2048Game/2.png").resize((50, 50)),
#     4: Image.open("./data/2048Game/4.png").resize((50, 50)),
#     8: Image.open("./data/2048Game/8.png").resize((50, 50)),
#     16: Image.open("./data/2048Game/16.png").resize((50, 50)),
#     32: Image.open("./data/2048Game/32.png").resize((50, 50)),
#     64: Image.open("./data/2048Game/64.png").resize((50, 50)),
#     128: Image.open("./data/2048Game/128.png").resize((50, 50)),
#     256: Image.open("./data/2048Game/256.png").resize((50, 50)),
#     512: Image.open("./data/2048Game/512.png").resize((50, 50)),
#     1024: Image.open("./data/2048Game/1024.png").resize((50, 50)),
#     2048: Image.open("./data/2048Game/2048.png").resize((50, 50)),
# }


# def formImg(g):
#     finalImg = Image.new(("RGBA"), (200, 200), (0, 0, 0, 0))
#     height, width = nums[0].size
#     for i in range(4):
#         for j in range(4):
#             finalImg.paste(nums[g[j][i]], (height * i, width * j))

#     return finalImg


def formTable(g):
    finalStr = ""
    for i in range(4):
        finalStr += "|"
        for j in range(4):
            if g[i][j] == 0:
                finalStr += "     "
            elif g[i][j] < 10:
                finalStr += f"    {g[i][j]}"
            elif g[i][j] < 99:
                finalStr += f"   {g[i][j]}"
            elif g[i][j] < 999:
                finalStr += f"  {g[i][j]}"
            else:
                finalStr += f" {g[i][j]}"
        finalStr += "|\n\n"
    return finalStr


def spawnNew(g):
    indexes = []
    for i in range(len(g[0])):
        for j in range(len(g[0])):
            if g[i][j] == 0:
                indexes.append([i, j])
    if indexes:
        t = 2
        if random.randint(0, 99) < 10:
            t = 4
        random.shuffle(indexes)
        x, y = indexes[random.randint(0, len(indexes))]
        g[x][y] = t
