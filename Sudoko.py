# -*- coding: utf-8 -*-
"""
Sudoko solver(Under Progresss)

@author: Microsoftlabs
"""


def init_value():
    """
    Intitilize grid with value 0
    """
    grid = []
    for i in range(0, 9):
        element = [0 for i in range(9)]
        grid.append(element)
    return grid


def check_hor(grid, val, pos):
    """
    Check that value val can adjusted
    in grid at position pos by checking
    only the Horizontal rows
    """
    row_val = []
    col_no = pos[1]
    for i in range(0, 9):
        row_val.append(grid[i][col_no])
    if val in row_val:
        return False
    return True


def check_vert(grid, val, pos):
    """
    Check that value val can adjusted
    in grid at position pos by checking
    only the Vertical columns
    """
    col_val = []
    row_no = pos[0]
    for i in range(0, 9):
        col_val.append(grid[row_no][i])
    if val in col_val:
        return False
    return True


def extract_cell(grid, pos):
    """
    Extract cell from grid located
    at cell position pos
    """
    cell_start_index = []
    for i in range(2):
        data = (pos[i]//3)*3
        cell_start_index.append(data)
    row, column = cell_start_index
    cell_val = []
    for i in range(column, column+3):
        for j in range(row, row+3):
            cell_val.append(grid[j][i])
    return cell_val


def check_cell(grid, val, pos):
    """
    Check that value val can adjusted
    in grid at position pos by checking
    only the cell
    """
    cell_val = extract_cell(grid, pos)
    if val in cell_val:
        return False
    return True


def check_all(grid, val, pos):
    """
    Check that value val can adjusted
    in grid at position pos by checking
    all the parameters
    """
    if validate_pos(pos) and validate_val(val):
        check1 = check_hor(grid, val, pos)
        check2 = check_vert(grid, val, pos)
        check3 = check_cell(grid, val, pos)
        if check1 and check2 and check3:
            return True
        return False
    print("Invalid data")
    return False


def validate_pos(pos):
    """
    Check validity of position
    pos i.e.,posx and posy
    lie in between 0 to 8
    """
    for i in range(2):
        if pos[i] not in range(0, 9):
            return False
    return True


def validate_val(val):
    """
    Check validity of value
    val i.e.,val
    lie in between 1 to 9
    """
    if val in range(1, 10):
        return True
    return False


def display_sudoko(grid):
    """
    Print sudoko to console
    """
    print("Sudoko\n")
    for i in range(9):
        if i % 3 == 0:
            print("-"*19)

        for j in range(9):
            val = grid[j][i]
            print("|" if j % 3 == 0 else " ", end="")
            print(val if val != 0 else " ", end="")
            print("|\n" if j == 8 else "", end="")
    print("-"*19)
    print("End of sudoko!")
    return


def enter_value(grid, val, pos):
    """
    Enter value of val at position
    pos in grid
    """
    x_cor, y_cor = pos
    if check_all(grid, val, pos):
        grid[x_cor][y_cor] = val
    return grid


def is_solved(grid):
    """
    Check whether sudoko is solved or not
    """
    for i in grid:
        if 0 in i:
            return False
    return True


def solver_phase_1(grid, super_flag=0):
    """
    Solve sudoko using conventional method
    """
    flag = 0
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                data = []
                pos = (i, j)
                for k in range(9):
                    if check_all(grid, k+1, pos):
                        data.append(k+1)
                if len(data) == 1:
                    enter_value(grid, data[0], pos)
                    flag = 1
    super_flag += flag
    if flag == 0:
        return (grid, super_flag)
    return solver_phase_1(grid, super_flag)


def init_cell():
    """
    Initialize a distionary cell
    in order key=(x,y):0
    where x,y is in between 0 to 2
    """
    cell = {}
    for i in range(3):
        for j in range(3):
            cell[(i, j)] = 0
    return cell


def find_left_elements(arr):
    """
    Find sudoko compliment of
    list

    Example
    -------
    Sudoko compliment of [1,2,3...,7] is[8,9]
    """
    narr = []
    for i in range(1, 10):
        if i not in arr:
            narr.append(i)
    return narr


def create_cell_order(grid):
    """
    Store no. of filled element in
    cell in form position:no. of occurence pair
    """
    cell = init_cell()
    for i in range(9):
        for j in range(9):
            pos = (i//3, j//3)
            if grid[i][j] != 0:
                cell[pos] += 1
    return cell


def solver_phase_2(grid):
    """
    Solve sudoko using contradiction method
    """
    cell = create_cell_order(grid)
    flag = 0
    for i in range(9):
        pos = max(cell, key=cell.get)
        flag += solve_cell(grid, pos)
        del cell[pos]
    if flag == 0:
        return False
    return True


def solve_cell(grid, cell_pos):
    """
    Solve cell of sudoko using contradiction method
    """
    flag = 0
    cell_pos = list(cell_pos)
    for i in range(2):
        cell_pos[i] *= 3
    row, column = cell_pos
    data = extract_cell(grid, (row, column))
    data = find_left_elements(data)
    for k in data:
        counter = val = 0
        pos = (row, column)
        for i in range(column, column+3):
            for j in range(row, row+3):
                if grid[j][i] == 0:
                    if check_all(grid, k, (j, i)):
                        counter += 1
                        val = k
                        pos = (j, i)
        if counter == 1:
            enter_value(grid, val, pos)
            flag = 1
    return flag


def find_empty_location(grid):
    """
    Parameters
    ----------
    grid : 2-D List
        Store sudoko.

    Returns
    -------
    pos : list
        Return location of unfilled element.

    """
    pos = [9, 9]
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                pos[0] = row
                pos[1] = col
                return pos
    return pos


def final_algorithm(grid):
    """
    Parameters
    ----------
    grid : 2-D List
        Store sudoko.

    Returns
    -------
    grid : Return solved grid using backtrack
        algorithm
    OR
    False/ True : For Recursion or in case sudoko is unsolvable

    """
    pos = [0, 0]

    if is_solved(grid):
        return grid
    pos = find_empty_location(grid)
    row, col = pos
    for i in range(1, 10):
        if check_all(grid, i, pos):
            grid[row][col] = i
            if final_algorithm(grid):
                if is_solved(grid):
                    return grid
                return True
            grid[row][col] = 0
    return False


def solver(grid):
    """
    Solve sudoko(main method)
    """
    flag = flag_2 = 1
    while flag > 0 or flag_2 > 0:
        grid, flag = solver_phase_1(grid)
        print("Phase : 1 passed succesfully")
        flag_2 = solver_phase_2(grid)
        print("Phase : 2 passed succesfully")
    display_sudoko(grid)
    grid = final_algorithm(grid)
    return grid


grid_1 = init_value()

grid_1[0][0] = 8
grid_1[2][1] = 3
grid_1[3][1] = 6
grid_1[1][2] = 7
grid_1[4][2] = 9
grid_1[6][2] = 2
grid_1[1][3] = 5
grid_1[5][3] = 7
grid_1[4][4] = 4
grid_1[5][4] = 5
grid_1[6][4] = 7
grid_1[3][5] = 1
grid_1[7][5] = 3
grid_1[2][6] = 1
grid_1[7][6] = 6
grid_1[8][6] = 8
grid_1[2][7] = 8
grid_1[3][7] = 5
grid_1[7][7] = 1
grid_1[1][8] = 9
grid_1[6][8] = 4

display_sudoko(grid_1)
grid_1 = solver(grid_1)
if not isinstance(grid_1, bool):
    display_sudoko(grid_1)
    
else:
    print("Unsolvable")
