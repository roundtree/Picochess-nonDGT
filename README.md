# Picochess-nonDGT
Modified version of picochess to run with reed switch chessboard controlled via Arduino nano

This system communicates with the arduino over the usb port.
The arduino scans the switch matrix of the chess board and send messages to picochess based on switch changes.
Additionaly it scans 5 buttons to simulate the buttons on a DGT clock, used by picochess for setting engine, mode time etc.

The messages are
L:square number when a chess piece is lifted.
D:square number, when a chess piece is dropped
B:button number when a button is pressed.

newgame:color starts a new game when all pieces are in starting position, and the last piece placed is the color to play.

The arduino can receive from picochess information to light leds on the board
They are 
L:square_number led on
F: square_number flash led
c:anything all led's off.

The squares are numberd with 0 at botton left.

I added to picochess code to handle these messages, mostly in sensorboard.py, which used keyboard.py as a template.
I also added rpidisplay.py, which displays game information, 
Picochess messages
current graphical representation of the board,
Level,
Time clocks for both players
Time control settings
