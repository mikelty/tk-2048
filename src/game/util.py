def move(dir, matrix):
    convert = {'left': 0, 'up': 270, 'right': 180, 'down': 90}
    deg = convert[dir]
    matrix = rotate_matrix(deg, matrix)
    matrix = swipe_left(matrix)
    matrix = rotate_matrix(360 - deg, matrix)
    return matrix

def swipe_left(matrix):
    for i, row in enumerate(matrix):
        # merge phase
        merged = [False] * 4
        for j, e in enumerate(row):
            if e > 0 and not merged[j]:
                for k, f in enumerate(row[j + 1:], j + 1):
                    if e == f and not merged[k]:
                        merged[j], merged[k] = True, True
                        row[j], row[k] = e + f, 0
                        break
                    elif f > 0:
                        break
        # squish phase
        matrix[i] = [e for e in row if e > 0] + [0] * row.count(0)
    return matrix


def rotate_matrix(deg, matrix):
    deg = deg % 360
    if deg == 0:
        return matrix
    elif deg == 90:
        return [list(row[::-1]) for row in zip(*matrix)]
    elif deg == 180:
        return [row[::-1] for row in matrix][::-1]
    else:
        return rotate_matrix(90, rotate_matrix(180, matrix))

def find_empty_locations(matrix):
    return [(i, j) for i in range(4) for j in range(4) if matrix[i][j] == 0]
