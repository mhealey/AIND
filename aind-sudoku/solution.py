assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    """Cross product of elements in A and elements in B."""
    return [x_ + y_ for x_ in A for y_ in B]

boxes = cross(rows,cols)
diagonals = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],
['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units + diagonals
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins by first locating all the entres of length = 2  
    
    for unit in unitlist:
        boxGroup = [(box1,box2) for box1 in unit for box2 in unit if values[box1]==values[box2] and len(values[box1])==2 and box1 != box2]
        if len(boxGroup) > 0:
            for i in range(len(boxGroup)):
                box1 = boxGroup[i][0]
                box2 = boxGroup[i][1]
                vals = values[box1]
                peerGroup = peers[box1] & peers[box2]
                for peer in peerGroup:
                    if len(values[peer]) > 2:
                        for val in vals:
                            assign_value(values,peer,values[peer].replace(val,""))
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    dct = dict(zip(boxes,grid))
    nums = '123456789'
    for key in dct:
        if dct[key] == '.':
            dct[key] = nums
    return dct

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    #  Define width of board (id 9 values, two bars)
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else ' ') for c in cols) )
        if r in 'CF': print(line)
    return

def eliminate(values):
    """  Processes values dictionary and eliminates all other peer choices if 
    """
    for key, value in values.items():
        if len(value)==1:
            kys = peers[key]
            for key2 in kys:
                if value in values[key2]:
                    assign_value(values,key2,values[key2].replace(value,""))

    return values    

def only_choice(values):
    """  Remove numbers, when there is only one choice amongst a unit group.  This can also accomplished
    by going through the dictionary of peers """
    for unit in unitlist:
        for num in cols:
            unitLst = [unt for unt in unit if num in values[unt]]
            if len(unitLst)==1:
                assign_value(values,unitLst[0],num)
            
        
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values) # Get the initial reduction, prior to performing any search

    #  If values has any issues, return failed
    if values is False:
        return False

    # if all values have a length of 1, solved!
    count = 0
    for key, value in values.items():
        if len(value) > 1:
            count+=1
    if count==0:
        return values

    #  Find the first place to search.  Beginning with the square with the least options in order to maximize our search
    #  speed.
    minn = 100
    for key, value in values.items():
        if len(value) < minn and len(value) > 1:
            n = value
            s = key 

    ## As shown in the solutions.py file from the course, this can also be done as a one line list 
    ## comprehension.  For accuracy, I've left my solution as is
    ## n, s = min((len(values[s]),s) for s in boxes if len(values[s]) > 1)

    for value in values[s]:
        new = values.copy()
        new[s] = value
        temp = search(new)
        if temp:
            return temp 



def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = reduce_puzzle(values)
    values = naked_twins(values)
    values = search(values)
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
