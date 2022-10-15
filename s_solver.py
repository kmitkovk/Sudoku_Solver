import copy

#%% Alogorithm description
"""
The algorithm iterates over the 9 diagonal (left to right, top to bottom) blocks
and it performs a check 1st on the row and 2nd on the column of the current
position of the target block on the diagonal traversing as follows:
    1. We look for missing number in the current row
    2. For every missing number we perform the folliowng checks:
        - is it contained in any of the neighbouring 2 blocks
            * this limits the scope of the search/check to the blocks where the
              number is not contained
        - then we perform a search/match in the vertical axis searching for match
        - when more than 1 possibility is found then we skip the number and move on
    3. We do the same for the columns
    4. If nothing more comes up, we perform a check withing the blocks
    5. Then we start the process again when the blocks check is exhausted

Improvements:
    1. Algo needs to be optimized to look more often into the blocks
    2. Algo could be changed so that it iterates over blocks instead of rows/cols

"""


#%% Process inputs
"""
test inputs 1: https://sudoku.com/easy/
test inputs 2: https://github.com/dimitri/sudoku/blob/master/sudoku.txt

"""
#easy:
i1 = "096150800008006745000084096900000370004920000085000420800540613030602980049030000"
s1 = "496157832218396745753284196962415378374928561185763429827549613531672984649831257"

i1 = "001000007800029060604105000008000210900200000000014708059000004086493150023801679"
s1 = "291346587835729461674185923548937216917268345362514798159672834786493152423851679"

i1 = "709000064000001300340900000050009013007400000000605420420590681006120000571830940"
s1 = "719358264862741395345962178654289713297413856138675429423597681986124537571836942"

#Medium:
i1 = "800000000600000108254681000000070080008024006320908010502037000036000020000250034"
s1 = "817593642693742158254681379469175283178324596325968417542837961736419825981256734"

i1 = "000080007000470096003000200002008005810040000030601900300000670060500001200163049"
s1 = "946382157128475396573916284692738415815249763734651928351894672469527831287163549"

#Hard:
i1 = "005010003306000000080020500000006300010004900460007008000000000040090800050001070"
s1 = "725619483396845712184723596972186345518234967463957128231478659647592831859361274"

i1 = "001700090000000206004020007050090360030800040060200000008900030040005070000000000"
s1 = "521768493973514286684329517857491362132856749469273851718942635246135978395687124"

#Expert:
i1 = "004007200010000480008000000106700000000482000900100000000005010350000006000020007"
s1 = "634817295715269483298534671186793542573482169942156738829675314357941826461328957"

#Evil:
i1 = "090000000000700080054030700600000000000001002073050800900000400800060000046005010"
s1 = "798512346362749185154638729621893574589471632473256891935127468817964253246385917"

grid = []
for i in range(0, 9 * 9, 9):
    grid.append([int(j) for j in i1[i : i + 9]])

solution = []
for i in range(0, 9 * 9, 9):
    solution.append([int(j) for j in s1[i : i + 9]])
#%% Constants

numbers = set([i for i in range(1, 10)])

bc = {  # block coordinates on 9x9 grid
    0: 0,
    1: 0,
    2: 0,
    3: 3,
    4: 3,
    5: 3,
    6: 6,
    7: 6,
    8: 6,
}

bc_big = {  # block coordinates on 3x3 grid
    0: 0,
    1: 0,
    2: 0,
    3: 1,
    4: 1,
    5: 1,
    6: 2,
    7: 2,
    8: 2,
}
#%% Functions


def get_block(grid, r, c):
    # returns a grid block of the current r,c
    grid_rows = grid[bc[r] : bc[r] + 3]
    block = [row[bc[c] : bc[c] + 3] for row in grid_rows]
    return block


def flatten_block(block):
    # returns a list the flattened block of the current r,c
    return [c for i in block for c in i]


def get_check_array(grid, r, c, cross_check_of="block"):
    # returns a list of numbers to check in the cross check of row/col/block
    if cross_check_of == "row":
        return [i[c] for i in grid]
    elif cross_check_of == "col":
        return [i for i in grid[r]]
    else:
        return [i for i in flatten_block(get_block(grid, r, c))]


def missing_nums(grid, r, c, look_in="block"):
    # returns a set missing nums in row, col, or block
    if look_in == "row":
        compare_list = [i for i in grid[r] if i > 0]
        return set(compare_list).symmetric_difference(numbers)
    elif look_in == "col":
        compare_list = [i[c] for i in grid if i[c] > 0]
        return set(compare_list).symmetric_difference(numbers)
    else:
        compare_list = [i for i in flatten_block(get_block(grid, r, c)) if i > 0]
        return set(compare_list).symmetric_difference(numbers)


def empty_positions(grid, r, c, look_in="block"):
    # return list of indices of the missing numbers in a row/col/block
    if look_in == "row":
        return [idx for idx, i in enumerate(grid[r]) if i == 0]
    elif look_in == "col":
        return [idx for idx, i in enumerate(grid) if i[c] == 0]
    else:
        return [
            idx for idx, i in enumerate(flatten_block(get_block(grid, r, c))) if i == 0
        ]


def solved_chec(nums_to_solve, num_solved):
    # checks if the puzzle has been solved and returns True/False
    return nums_to_solve == num_solved


def solved_check_old(grid):
    # checks if the puzzle has been solved and returns True/False
    if [c for c in flatten_block(grid) if c == 0]:
        return False
    return True


#%% Solver
grid_sol = copy.deepcopy(grid)
nums_to_solve = len([c for c in flatten_block(grid) if c == 0])
num_solved = 0  # increment 1 on revealing a number
solved = False
for loop in range(1000):  # for now using for loop to prevent infinte loop
# while not solved:
    for b in range(9):  # b = block in the diagonal traverse from 0 to 8
        # row_check():
        for mis_num in missing_nums(grid_sol, b, b, "row"):
            pos_poss_count = 0  # possibility count of pos -> must be < 2
            fit_pos = []
            for pos in empty_positions(grid_sol, b, b, "row"):
                if mis_num in get_check_array(grid_sol, "dummy", pos, "row"):
                    continue
                elif mis_num in get_check_array(
                    grid_sol, b, pos, "block"
                ):  # if in block
                    continue
                else:
                    pos_poss_count += 1
                    fit_pos.append(pos)  # position where the number fits
                if pos_poss_count > 1:
                    break  # break out number fittness in pos search, next missing num
            # overwrite the grid with answer and increment
            if pos_poss_count == 1:  # avoids pos-last pos error
                grid_sol[b][fit_pos[0]] = mis_num  # taking first (and only) fit
                # print("\nNumber Fit!\n")
                num_solved += 1

        # col_check():
        for mis_num in missing_nums(grid_sol, b, b, "col"):
            pos_poss_count = 0  # possibility count of pos -> must be < 2
            fit_pos = []
            for pos in empty_positions(grid_sol, b, b, "col"):

                if mis_num in get_check_array(grid_sol, pos, "dummy", "col"):
                    continue
                elif mis_num in get_check_array(
                    grid_sol, pos, b, "block"
                ):  # if in block
                    continue
                else:
                    pos_poss_count += 1
                    fit_pos.append(pos)  # position where the number fits
                if pos_poss_count > 1:
                    break  # break out number fittness in pos search, next missing num
            # overwrite the grid with answer and increment
            if pos_poss_count == 1:  # avoids pos-last pos error
                grid_sol[fit_pos[0]][b] = mis_num  # taking first (and only) fit
                # print("\nNumber Fit!\n")
                num_solved += 1

    if solved_chec(nums_to_solve, num_solved):
        break
        # solved = True
        
print(solution==grid_sol,f'\nAfter loop: {loop}')