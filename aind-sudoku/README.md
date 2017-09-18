# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: *Student should provide answer here*

A:  Constraint propogation refers to the method of applying a set of rules (or constraints) to a game board after having made a decision on a particular value.  In the case of naked_twins, we notice that if two peers are to have only two potential values, then none of the remaining peers may have that value.  This, therefore further constrains the peers by removing this two choices possibilities, and propogating there removal throughout the peers. 

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Constraint propogation via addition of a diagonal rule set, further constrains the available values along those diagonals.  When a choice is made on the diagonal, the propogation of the removal of this option from its peers not only travels along the boxes, columns, and rows, but along the existing diagonal axis as well.  This actually makes the game easier by removing more potential answers via constraint propogation.
