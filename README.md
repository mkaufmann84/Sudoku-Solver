# Web bot to solve a sudoku puzzle. 
This is the code for a web bot that can automatically solve a Sudoku Puzzle.

Sudoku Solver for websudoku.com

If NoelementException can be found, or something like that happens, you have slow internet. Increase the time.sleep by a few seconds. 

This can solve sudoku puzzle.
Initialize an ws object, and if inputted cv, where cv is a dictanary mapping a tuple(coordnite) to a value, where 0 is unknown,
it will print the solution to that puzzle. 

The way it is set up is it opens a window, and using webscripting can solve puzzles at the webpage websudoku.com. 
