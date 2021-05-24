This is the Tower of Hanoi classical puzzle implementation in Python language
using pygame library.

The puzzle consists of three rods and a number of disks of different diameters,
which can slide onto any rod. The game starts with the disks stacked on one rod
in order of decreasing size, the smallest at the top, thus approximating
a conical shape.

The objective of the puzzle is to move the entire stack to the last rod,
obeying the following simple rules:
    - Only one disk may be moved at a time.
    - Each move consists of taking the upper disk from one of the stacks and
      placing it on top of another stack or an empty rod.
    - No disk may be placed on top of a disk that is smaller than it.

For more info see the Wikipedia article:
    https://en.wikipedia.org/wiki/Tower_of_Hanoi

To run the game you should firstly install Python and pygame package. When it’s
done open command line or terminal session and navigate to the game directory.
Then input script name and press Enter:
    python pyramid_puzzle.py

In-game controls:
    Select source tower by first mouse click. When selected, the topmost
    tower’s disk starts blinking. You may cancel selection by pressing ESC key
    and choose another tower. Select target tower by second mouse click.
    The disk will move onto the target tower, if the game’s rules do allow
    such move.

    Also you can use numeric keys (1, 2 or 3) for quick selecting the towers.

    F1 - show help screen.
    F2 - perform automatic solution (pressing ESC will cancel the action).
    F3 - reset puzzle.
    F4 - quit the game.
    F11 - toggle fullscreen.

Requirements:
    - Python 3.8.6
    - pygame 2.0.1
