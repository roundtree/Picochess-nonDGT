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

class RpiDisplay(DgtIface, threading.Thread):
    Computer_Move = False

    def __init__(self, dgtserial, dgttranslate, enable_revelation_leds):
        super(RpiDisplay, self).__init__(dgtserial, dgttranslate, enable_revelation_leds)
        # self.lock = threading.Lock()
        self.game = chess.Board()

        self.rt = None
        self.time_side = ClockSide.NONE
        # setup virtual clock
        main_version = 2 if dgtserial.is_pi else 0
        DisplayMsg.show(Message.DGT_CLOCK_VERSION(main_version=main_version, sub_version=0, attached="virtual"))

        self.screen = pygame.display.set_mode((480, 320))
        pygame.init()
        pygame.display.set_caption('Chess')
        self.font = pygame.font.Font(None, 48)
        self.fg = 0, 0, 0
        self.time_left = (0, 0, 0)
        self.time_right = (0, 0, 0)
        self.color = 255
        self.level = 'Level 20'
        self.timetext = "Blitz 5"
        self.info = 'info'

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
        stra = 'Clock: {} - {}'.format(self.time_left, self.time_right)
        ren = self.font.render('Clock: {} - {}'.format(self.time_left, self.time_right), 0, self.fg)
        a = screen.blit(ren, (0, 256))
        ren = self.font.render(self.level, 0, self.fg)
        a = screen.blit(ren, (256, 0))
        ren = self.font.render(self.timetext, 0, self.fg)
        a = screen.blit(ren, (256, 80))
        ren = self.font.render(self.info, 0, self.fg)
        a = screen.blit(ren, (256, 144))
        pygame.display.flip()
        pygame.display.update()

    def runclock(self):
        if self.time_side == ClockSide.LEFT:
            h, m, s = self.time_left
            time_left = 3600 * h + 60 * m + s - 1
            if time_left <= 0:
                print('Clock flag: left')
                self.rt.stop()
            self.time_left = hours_minutes_seconds(time_left)
        if self.time_side == ClockSide.RIGHT:
            h, m, s = self.time_right
            time_right = 3600 * h + 60 * m + s - 1
            if time_right <= 0:
                print('Clock flag: right')
                self.rt.stop()
            self.time_right = hours_minutes_seconds(time_right)
        if self.maxtimer_running:
            print('Clock maxtime not run out')
        else:
            print('Clock time: {} - {}'.format(self.time_left, self.time_right))
        self.displaybrd()
        #DisplayMsg.show(Message.DGT_CLOCK_TIME(time_left=self.time_left, time_right=self.time_right))

    def display_move_on_clock(self, move, fen, side, beep=False, left_dots=0, right_dots=0):
        if self.enable_dgt_3000:
            bit_board = chess.Board(fen)
            text = bit_board.san(move)
        else:
            text = str(move)
        if side == ClockSide.RIGHT:
            text = text.rjust(8 if self.enable_dgt_3000 else 6)
        logging.debug(text)
        print('Clock move: {} Beep: {}'.format(text, beep))
        self.info = text
        self.displaybrd()

    def display_text_on_clock(self, text, beep=False, left_dots=0, right_dots=0):
        logging.debug(text)
        print('Clock text: {} Beep: {}'.format(text, beep))
        self.info = text
        self.displaybrd()
    def display_time_on_clock(self, force=False):
        if self.clock_running or force:
            print('Clock showing time again - running state: {}'.format(self.clock_running))
        else:
            logging.debug('virtual clock isnt running - no need for endClock')

    def stop_clock(self):
        if self.rt:
            print('Clock time stopped at {} - {}'.format(self.time_left, self.time_right))
            self.rt.stop()
        else:
            print('Clock not ready')
        self.clock_running = False

    def resume_clock(self, side):
        pass

    def start_clock(self, time_left, time_right, side):
        self.time_left = hours_minutes_seconds(time_left)
        self.time_right = hours_minutes_seconds(time_right)
        self.time_side = side

        print('Clock time started at {} - {} on {}'.format(self.time_left, self.time_right, side))
        if self.rt:
            self.rt.stop()
        if side != ClockSide.NONE:
            self.rt = RepeatedTimer(1, self.runclock)
            self.rt.start()
        self.clock_running = (side != ClockSide.NONE)

    def light_squares_revelation_board(self, squares):
        pass

    def clear_light_revelation_board(self):
        pass

    def update_display(self,game):
        self.game=game
        self.displaybrd()
    def displaylevel(self,leveltext):
        self.level=leveltext
        self.displaybrd()
    def displaytime(self,time):
        self.timetext = time
        self.displaybrd()
    def DisplayClose(self):
        pygame.display.quit()


