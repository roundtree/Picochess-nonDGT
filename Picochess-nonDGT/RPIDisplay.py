__author__ = 'Brian'

import threading
from picochess import *
import pygame
from timecontrol import *
from dgtiface import *
from utilities import RepeatedTimer



screen = pygame.display.set_mode((480, 320))

pieces = [{}, {}]
pieces[0][4] = pygame.image.load("./img/brw.png")  # white squares
pieces[0][2] = pygame.image.load("./img/bnw.png")  # black n white sq
pieces[0][3] = pygame.image.load("./img/bbw.png")
pieces[0][6] = pygame.image.load("./img/bkw.png")
pieces[0][5] = pygame.image.load("./img/bqw.png")
pieces[0][1] = pygame.image.load("./img/bpw.png")
pieces[0][14] = pygame.image.load("./img/wrw.png")
pieces[0][12] = pygame.image.load("./img/wnw.png")  # white n white square
pieces[0][13] = pygame.image.load("./img/wbw.png")
pieces[0][16] = pygame.image.load("./img/wkw.png")
pieces[0][15] = pygame.image.load("./img/wqw.png")
pieces[0][11] = pygame.image.load("./img/wpw.png")
pieces[0][0] = pygame.image.load("./img/w.png")
pieces[1][4] = pygame.image.load("./img/brb.png")  # black squares
pieces[1][2] = pygame.image.load("./img/bnb.png")
pieces[1][3] = pygame.image.load("./img/bbb.png")
pieces[1][6] = pygame.image.load("./img/bkb.png")
pieces[1][5] = pygame.image.load("./img/bqb.png")
pieces[1][1] = pygame.image.load("./img/bpb.png")
pieces[1][14] = pygame.image.load("./img/wrb.png")
pieces[1][12] = pygame.image.load("./img/wnb.png")
pieces[1][13] = pygame.image.load("./img/wbb.png")
pieces[1][16] = pygame.image.load("./img/wkb.png")
pieces[1][15] = pygame.image.load("./img/wqb.png")
pieces[1][11] = pygame.image.load("./img/wpb.png")
pieces[1][0] = pygame.image.load("./img/b.png")

keyboard_last_fen = None

class RpiDisplay(DisplayMsg,threading.Thread):
    Computer_Move = False

    def __init__(self):
        super(RpiDisplay,self).__init__()
        # # self.lock = threading.Lock()
        self.game = chess.Board()

        self.rt = None
        self.time_side = ClockSide.NONE
        # setup virtual clock
        #main_version = 2 if dgtserial.is_pi else 0
        #DisplayMsg.show(Message.DGT_CLOCK_VERSION(main_version=main_version, sub_version=0, attached="virtual"))

        self.screen = pygame.display.set_mode((480, 320))
        pygame.init()
        pygame.display.set_caption('Chess')

        self.fg = 0, 0, 0
        self.time_left = (0, 0, 0)
        self.time_right = (0, 0, 0)
        self.color = 255
        self.level = 'Level'
        self.timetext = "TimeMode"
        #self.info = ''
        self.score = "score"
        self.ponder = "ponder"
        self.engine_name = "engine"
        self.mode ="normal"

        self.version = "version"
        self.displaybrd()


    def displaybrd(self):

        #board = self.board
        screen = self.screen
        screen.fill((255, 255, 255))
        for y in range(8):
            for x in range(8):
                #piece = board.piece_at((y * 8) + x)
                piece = self.game.piece_at((y * 8) + x)
                if piece:
                    if not piece.color:
                        im = piece.piece_type
                    else:
                        im = piece.piece_type + 10
                else:
                    im = 0
                screen.blit(pieces[(x + y) % 2][im], (x * 32, (224 - y * 32)))
        #stra = 'Clock: {} - {}'.format(self.time_left, self.time_right)
        self.font = pygame.font.Font(None, 40)
        ren = self.font.render('Clock: {} - {}'.format(self.time_left, self.time_right), 0, self.fg)
        a = screen.blit(ren, (0, 256))
        ren = self.font.render(self.engine_name, 0, self.fg)
        a = screen.blit(ren, (256, 0))
        ren = self.font.render(self.level, 0, self.fg)
        a = screen.blit(ren, (256, 40))
        ren = self.font.render(self.timetext, 0, self.fg)
        a = screen.blit(ren, (256, 80))

        self.font = pygame.font.Font(None, 24)
        ren = self.font.render(self.mode, 0, self.fg)
        a = screen.blit(ren, (256, 200))

        ren = self.font.render(self.version, 0, self.fg)
        a = screen.blit(ren, (0, 300))
        ren = self.font.render(self.score, 0, self.fg)
        a = screen.blit(ren, (200, 300))
        ren = self.font.render(self.ponder, 0, self.fg)
        a = screen.blit(ren, (300, 300))
        pygame.display.flip()
        pygame.display.update()


    def update_display(self,game):
         self.game=game
         self.displaybrd()
    # def displaylevel(self,leveltext):
    #     self.level=leveltext
    #     self.displaybrd()
    # def displaytime(self,time):
    #     self.timetext = time
    #     self.displaybrd()
    def DisplayClose(self):
        pygame.display.quit()


    def run(self):
        global keyboard_last_fen
        logging.info('msg_queue RPIDisplay ready')
        while True:
            # Check if we have something to display
            message = self.msg_queue.get()
            for case in switch(message):
                # print(message)
                if case(MessageApi.DISPLAY_TEXT):
                    self.version =  str(message.text)
                    #logging.info("msg_queue {}".format(message.text))
                    self.displaybrd()
                    break
                if case(MessageApi.DGT_BUTTON):
                    button = message.button
                    break
                if case(MessageApi.ENGINE_READY):

                    self.engine_name = message.name
                    self.displaybrd()
                    break
                if case(MessageApi.ENGINE_STARTUP):
                    self.engine_name = message.name
                    self.displaybrd()

                    break
                if case(MessageApi.INTERACTION_MODE):
                    self.mode = str(message.mode)
                    self.displaybrd()

                    break
                if case(MessageApi.OPENING_BOOK):
                    self.info = message.book_name

                    break
                if case(MessageApi.COMPUTER_MOVE):
                    self.game=message.game
                    self.displaybrd()
                    break
                if case(MessageApi.USER_TAKE_BACK):
                    self.game=message.game
                    self.displaybrd()
                    break
                if case(MessageApi.TIME_CONTROL):
                    self.timetext = message.time_text
                    self.displaybrd()
                    break
                if case(MessageApi.COMPUTER_MOVE_DONE_ON_BOARD):
                    keyboard_last_fen = None
                    break
                if case(MessageApi.USER_MOVE):
                    self.game = message.game
                    self.displaybrd()
                    break
                if case(MessageApi.START_NEW_GAME):
                    keyboard_last_fen = None
                    self.time_left = (0, 0, 0)
                    self.time_right = (0, 0, 0)
                    self.game = message.game
                    self.displaybrd()

                    break
                if case(MessageApi.NEW_SCORE):
                    self.score = "Score {}".format(message.score)
                    self.displaybrd()
                    break
                if case(MessageApi.DGT_CLOCK_TIME):
                    self.time_left = message.time_left
                    self.time_right =  message.time_right
                    self.displaybrd()
                    break
                if case(MessageApi.NEW_PV):         #Principal variation
                    self.ponder = "Pondering " + str(message.pv[0])     #pondering  move
                    self.hint_fen = message.fen
                    self.hint_turn = message.turn
                    self.displaybrd()
                    #self.game =

                        #DisplayDgt.show(Dgt.DISPLAY_MOVE(move=self.hint_move, fen=self.hint_fen, side=side, wait=False,
                          #                               beep=self.dgttranslate.bl(BeepLevel.NO), maxtime=0))
                    break
                if case(MessageApi.STARTUP_INFO):
                    self.mode_index = message.info['interaction_mode']
                    self.mode_result = message.info['interaction_mode']
                    self.book_index = message.info['book_index']
                    self.all_books = message.info['books']
                    tc = message.info['time_control']

                    if tc.mode == TimeMode.BLITZ:
                        self.timetext =  'Blitz {:d}'.format(tc.minutes_per_game)
                    elif tc.mode == TimeMode.FISCHER:
                        self.timetext = 'Fisher {:d} {:d}'.format(tc.minutes_per_game,tc.fischer_increment)
                    elif tc.mode == TimeMode.FIXED:
                        self.timetext = 'Fixed {:d}'.format(tc.seconds_per_move)
                    self.displaybrd()
                    break
                # if case(MessageApi.DGT_CLOCK_VERSION):  #version of attached DGT clock
                #     self.info = message.main_version
                #         # sub_version=message.sub_version, attached=message.attached))
                #     self.displaybrd()
                #     break
                if case(MessageApi.KEYBOARD_MOVE):
                    fen = message.fen.fen().split(' ')[0]
                    Observable.fire(Event.DGT_FEN(fen=fen))
                    self.game = message.fen
                    keyboard_last_fen = fen
                    self.displaybrd()
                    break
                if case(MessageApi.UCI_OPTION_LIST):
                    self.level = "Skill Level " + message.options['skill level']
                    self.displaybrd()
                    break
                if case(MessageApi.LEVEL):
                    self.level = message.level_text.m

                    break
                # if case(MessageApi.PLAYMOVE):
                #     if message.fen is not None:
                #         Observable.fire(Event.DGT_FEN(fen=keyboard_last_fen))
                #     else:
                #         print('last move already send to virtual board')
                #     break

                if case():  # Default
                    pass

