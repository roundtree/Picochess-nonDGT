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
    def __init__(self,ser):
        super(SensorBoard, self).__init__()

        self.arduino=ser
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
                            self.fire(Event.DGT_FEN(fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'))
                        elif side == 'b':
                            self.fire(Event.DGT_FEN(fen='RNBKQBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbkqbnr'))
                        else:
                            raise ValueError(raw)
                    else:
                        if cmd.startswith('print:'):
                            fen = raw.split(':')[1]
                            print(chess.Board(fen))
                        elif cmd.startswith('setup:'):
                            fen = raw.split(':')[1]
                            uci960 = False  # make it easy for the moment
                            bit_board = chess.Board(fen, uci960)
                            if bit_board.is_valid():
                                self.fire(Event.SETUP_POSITION(fen=bit_board.fen(), uci960=uci960))
                            else:
                                raise ValueError(fen)
                        # Here starts the simulation of a dgt-board!
                        # Let the user send events like the board would do
                        elif cmd.startswith('fen:'):
                            fen = raw.split(':')[1]
                            # dgt board only sends the basic fen => be sure
                            # it's same no matter what fen the user entered
                            self.fire(Event.DGT_FEN(fen=fen.split(' ')[0]))
                        elif cmd.startswith('b:'):
                            button = int(cmd.split(':')[1])
                            if button not in range(5):
                                raise ValueError(button)
                            self.fire(Event.DGT_BUTTON(button=button))
                        elif cmd.startswith('level:'):
                            level =int(cmd.split(':')[1])

                            self.fire(Event.LEVEL(level=level,beep=BeepLevel.BUTTON))
                        elif cmd.startswith('l:'):
                            from_square = cmd.split(':')[1]
                            self.fire(Event.LIFT_PIECE(square=from_square))
                        elif cmd.startswith('d:'):
                            to_square = cmd.split(':')[1]
                            self.fire(Event.DROP_PIECE(square=to_square))
                            print("Drop Piece")

                        elif cmd.startswith('t:'):
                            tc = cmd.split(':')[1]
                            self.fire(Event.SET_TIME_CONTROL(time_control=tc, time_control_string='ok time', beep=BeepLevel.BUTTON))

                        else:
                            # move => fen => virtual board sends fen
                            #move = chess.Move.from_uci(cmd)
                            # print (chess.Board.attacks(game,"E2"))
                            #self.fire(Event.KEYBOARD_MOVE(move=move))
                            print("command not recognised ", cmd)  #bl
                except ValueError as e:
                    logging.warning('Invalid user input [%s]', cmd)


# class TerminalDisplay(Display, threading.Thread):
#     def __init__(self,ser):
#         super(TerminalDisplay, self).__init__()
#         self.arduino = ser
#     def run(self):
#         while True:
#             time.sleep(1)
#             self.arduino.write(b"F23")              # need to create messages, only comes here on display command
#             self.arduino.flush()
#             # Check if we have something to display
#             message = self.message_queue.get()
#             for case in switch(message):
#                 if case(MessageApi.COMPUTER_MOVE):
#                     #print('\n' + str(message.game))
#                     #print(message.game.fen())
#                     #print('emulate user to make the computer move...sleeping for one second')
#                     time.sleep(1)
#                     logging.debug('emulate user now finished doing computer move')
#                     Display.show(Message.DGT_FEN(fen=message.game.board_fen()))
#                     break
#                 if case(MessageApi.SEARCH_STARTED):
#                     #if message.engine_status == EngineStatus.THINK:
#                         #print('Computer starts thinking')
#                     #if message.engine_status == EngineStatus.PONDER:
#                         #print('Computer starts pondering')
#                     #if message.engine_status == EngineStatus.WAIT:
#                         #print('Computer starts waiting - hmmm')
#                     break
#                 if case(MessageApi.SEARCH_STOPPED):
#                     #if message.engine_status == EngineStatus.THINK:
#                         #print('Computer stops thinking')
#                     #if message.engine_status == EngineStatus.PONDER:
#                         #print('Computer stops pondering')
#                     #if message.engine_status == EngineStatus.WAIT:
#                         #print('Computer stops waiting - hmmm')
#                     break
#                 if case(MessageApi.DGT_CLOCK_TIME):     #bl
#                     #print(message.time_left,message.time_right)
#                     #DgtDisplay.show(Dgt.CLOCK_TIME(time_left=message.time_left, time_right=message.time_right))
#                     break
#                 if case():  # Default
#                     pass
