___author__ = 'Brian'



import threading
import chess
import time
import logging
import serial
import chess.uci

from utilities import *
from timecontrol import *
from picochess import *




class SensorBoard(Observable, threading.Thread):
    def __init__(self):
        super(SensorBoard, self).__init__()
        self.flip_board = False
        self.arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=.1)

    def Light_Square(self,mvlist,on):
         if len(mvlist):
            for square in mvlist:
                if on:
                    sq = "L" + str(square)
                    self.arduino.write(str.encode(sq))
                else:
                    sq = "C" + str(square)
                    self.arduino.write(str.encode(sq))
            self.arduino.flush()
    def Beep(self,tone):
        cmd = "B" + str(tone)
        self.arduino.write(str.encode(cmd))
        self.arduino.flush()


    def run(self):
        global playersturn
        while True:
            btxt = ""
            if self.arduino.inWaiting()>0:
                btxt = self.arduino.readline().strip()
                self.arduino.flush()
            if btxt:
                print(btxt)
                cmd = btxt.decode('utf-8').lower()

                #raw = input('PicoChess v' + version + ':>').strip()
                #cmd = raw.lower()
                #print(cmd)
                try:
                    # commands like "newgame:<w|b>" or "setup:<legal_fen_string>"
                    # or "print:<legal_fen_string>"
                    #
                    # for simulating a dgt board use the following commands
                    # "fen:<legal_fen_string>" or "button:<0-4>"
                    #
                    # everything else is regarded as a move string
                    if cmd.startswith('newgame:'):
                        side = cmd.split(':')[1]
                        if side == 'w':
                            self.flip_board = False
                            self.fire(Event.DGT_FEN(fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'))
                        elif side == 'b':
                            self.flip_board = True
                            self.fire(Event.DGT_FEN(fen='RNBKQBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbkqbnr'))
                        else:
                            raise ValueError(cmd)
                    else:
                        # if cmd.startswith('print:'):
                        #     fen = cmd.split(':')[1]
                        #     print(chess.Board(fen))
                        # elif cmd.startswith('setup:'):
                        #     fen = cmd.split(':')[1]
                        #     uci960 = False  # make it easy for the moment
                        #     bit_board = chess.Board(fen, uci960)
                        #     if bit_board.is_valid():
                        #         self.fire(Event.SETUP_POSITION(fen=bit_board.fen(), uci960=uci960))
                        #     else:
                        #         raise ValueError(fen)
                        # Here starts the simulation of a dgt-board!
                        # Let the user send events like the board would do
                        # elif cmd.startswith('fen:'):
                        #     fen = cmd.split(':')[1]
                        #     # dgt board only sends the basic fen => be sure
                        #     # it's same no matter what fen the user entered
                        #     self.fire(Event.DGT_FEN(fen=fen.split(' ')[0]))
                        if cmd.startswith('b:'):
                            button = int(cmd.split(':')[1])
                            if button not in range(5):
                                raise ValueError(button)
                            self.fire(Event.DGT_BUTTON(button=button))
                        # elif cmd.startswith('level:'):
                        #     level =int(cmd.split(':')[1])
                        #
                        #     self.fire(Event.LEVEL(level=level,beep=BeepLevel.BUTTON))
                        elif cmd.startswith('l:'):
                            from_square = cmd.split(':')[1]
                            self.fire(Event.LIFT_PIECE(square=from_square))
                        elif cmd.startswith('d:'):
                            to_square = cmd.split(':')[1]
                            self.fire(Event.DROP_PIECE(square=to_square))
                            print("Drop Piece")
                        elif cmd.startswith("tb:"):
                            self.fire(Event.TAKE_BACK())
                        elif cmd.startswith('shutdown'):
                            self.fire(Event.SHUTDOWN())


                        # elif cmd.startswith('t:'):
                        #     tc = cmd.split(':')[1]
                        #     self.fire(Event.SET_TIME_CONTROL(time_control=tc, time_control_string='ok time', beep=BeepLevel.BUTTON))

                        else:
                            # move => fen => virtual board sends fen
                            #move = chess.Move.from_uci(cmd)
                            # print (chess.Board.attacks(game,"E2"))
                            #self.fire(Event.KEYBOARD_MOVE(move=move))
                            print("command not recognised ", cmd)  #bl
                except ValueError as e:
                    logging.warning('Invalid user input [%s]', cmd)


