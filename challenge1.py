import sys

# list of tuples for directions around the grid
directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def readInfo(filename):
    """
    Read information from a file.
    Returns the number of rows and columns, a 2D list of letters, the mode, and a list of words to search
    """
    try:
        f = open(filename, 'r')
        info = [i.strip() for i in f.readlines()]
        f.close()
        try:
            n, m = info[0].split(' ')  # row and col lengths
            n, m = int(n), int(m)
        except ValueError:
            print('Error: Row or column lengths not properly specified')
            sys.exit(1)
        grid = [[char.upper() for char in i] for c, i in enumerate(info) if 0 < c < n + 1]  # grid of letters
        # check if the grid dimensions are correct
        if len(grid[0]) != m:
            print('Error: Number of columns in grid do not match number of columns specified')
            sys.exit(1)
        mode = info[n + 1].upper()  # mode: either WRAP or NO_WRAP
        # check if the mode is correct
        if mode != 'WRAP' and mode != 'NO_WRAP':
            print('Error: Improper indication of mode (WRAP or NO_WRAP)')
            sys.exit(1)
        words = [i.upper() for c, i in enumerate(info) if c > n + 2]
        # check if the number of words is correct
        if len(words) != int(info[n + 2]):
            print('Error: Number of words does not match the specified number')
            sys.exit(1)
        return n, m, grid, mode, words
    except IOError:
        print("Error: Can't find file")
        sys.exit(1)


def findBase(c, grid):
    """
    Finds matches in the grid for the beginning of the word.
    """
    return [(i, j) for i, n in enumerate(grid) for j, m in enumerate(n) if c == m]


def match(grid, word, n, m, i, j, k, d, mode):
    """
    Sees if the next letter in the grid in this direction matches the next letter in the word.
    Returns True if it does and the indices.
    """
    k += 1
    # move in the specified direction
    x = i + d[0]
    y = j + d[1]
    # if boundary is reached and mode is WRAP reset the indices
    if mode == 'WRAP':
        if x >= n:
            x = 0
        if x < 0:
            x = n - 1
        if y >= m:
            y = 0
        if y < 0:
            y = m - 1
    # if boundary is reached and mode is NO_WRAP then return false
    if mode == 'NO_WRAP':
        if x >= n or x < 0:
            return False, i, j, k - 1
        if y >= m or y < 0:
            return False, i, j, k - 1
    # see if it matches
    if grid[x][y] == word[k]:
        return True, x, y, k
    # don't update the values if it doesn't match
    return False, i, j, k-1


def findDir(grid, word, n, m, i, j, k, mode):
    """
    Finds and returns the direction to the next letter and the next indices.
    """
    x, y = i, j
    for d in directions:
        mat, x, y, k = match(grid, word, n, m, x, y, k, d, mode)
        if mat:
            return d, x, y, k
    return None, i, j, k


def findNext(grid, word, n, m, i, j, k, d, mode):
    """
    Finds the next letters in the word in the direction given
    """
    x, y = i, j
    mat = True
    c = []  # list of coordinates
    while k < len(word) - 1 and mat:
        mat, x, y, k = match(grid, word, n, m, x, y, k, d, mode)
        c.append((x, y))
    return x, y, k, c


def findW(grid, n, m, i, j, word, mode):
    """
    Attempts to find a word from the grid.
    Returns the True if found, False if not and the coordinates of the last letter if found.
    """
    k = 0  # counter for letters
    ni, nj = i, j
    c = [(ni, nj)]  # list of coordinates
    # find the next letter and direction it's in
    d, ni, nj, k = findDir(grid, word, n, m, ni, nj, k, mode)
    c.append((ni, nj))
    # move in that direction
    if d is not None:
        ni, nj, k, coords = findNext(grid, word, n, m, ni, nj, k, d, mode)
        c = c + coords
    # letters can't be used more than once, so see if there are duplicates in the coordinates
    if len(c) != len(set(c)):
        return False, None
    if k == len(word) - 1:
        return True, (ni, nj)
    return False, None


def search(grid, word, n, m, mode):
    """
    Search for a word in the grid. Returns the start and end coordinates if found. If not found returns "NOT FOUND"
    """
    # find the coordinates of the potential first letters of the word
    bases = findBase(word[0], grid)
    for b in bases:
        i, j = b[0], b[1]
        r, e = findW(grid, n, m, i, j, word, mode)
        if r:
            return (i, j), e
    return "NOT FOUND"


def main():
    # get information from input file
    filename = input('Enter the filename: ')
    n, m, grid, mode, words = readInfo(filename)

    # search for words
    for word in words:
        print(search(grid, word, n, m, mode))


if __name__ == "__main__":
    main()
