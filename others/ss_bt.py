# https://www.youtube.com/watch?v=G_UYXzGuqvM&ab_channel=Computerphile
def solve():
    global grid
    for i in range(0, 9):
        for j in range(0, 9):
            if grid[i][j] == 0:
                for n in range(1, 10):
                    if possible(i, j, n):
                        grid[i][j] = n
                        # Can puzzle be solved from current state?
                        backtrack = solve()
                        # Can't be solved that way so reset square and try next `n`.
                        if backtrack:
                            grid[i][j] = 0
                        # A solution was found! Don't backtrack!
                        else:
                            return False
                # No `n` worked. I must backtrack.
                return True
    # I solved the last square!
