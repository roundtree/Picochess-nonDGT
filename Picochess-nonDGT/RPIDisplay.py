__author__ = 'Brian'

import threading
from picochess import *
import pygame
from timecontrol import *

screen = pygame.display.set_mode((480, 320))

pieces = [{}, {}]
pieces[0][4] = pygame.image.load("./img/brw.png")  #white squares
pieces[0][2] = pygame.image.load("./img/bnw.png")  #black n white sq
pieces[0][3] = pygame.image.load("./img/bbw.png")
pieces[0][6] = pygame.image.load("./img/bkw.png")
pieces[0][5] = pygame.image.load("./img/bqw.png")
pieces[0][1] = pygame.image.load("./img/bpw.png")
pieces[0][14] = pygame.image.load("./img/wrw.png")
pieces[0][12] = pygame.image.load("./img/wnw.png")  #white n white square
pieces[0][13] = pygame.image.load("./img/wbw.png")
pieces[0][16] = pygame.image.load("./img/wkw.png")
pieces[0][15] = pygame.image.load("./img/wqw.png")
pieces[0][11] = pygame.image.load("./img/wpw.png")
pieces[0][0] = pygame.image.load("./img/w.png")
pieces[1][4] = pygame.image.load("./img/brb.png")  #black squares
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




        

class RpiDisplay(DisplayMsg,threading.Thread):

    def __init__(self):
        super(RpiDisplay, self).__init__()
        self.lock = threading.Lock()
        self.board = chess.Board()
        clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((480, 320))
        pygame.init()
        pygame.display.set_caption('Chess')
        self.font = pygame.font.Font(None, 48)
        self.fg = 0, 0, 0
        self.time_left = (0, 0, 0)
        self.time_right = (0, 0, 0)
        self.color=255
        self.level = 20
        self.timetext = "Blitz 5"
        self.info = 'info'
    
    def displaybrd(self):


        clock = pygame.time.Clock()

        board = self.board
        #print ("thread is fine")
        screen = self.screen
        screen.fill((255, 255, 255))
        for y in range(8):
            for x in range(8):
                piece = board.piece_at((y * 8) + x)
                if piece:
                   if not piece.color:
                       im = piece.piece_type
                   else:
                      im = piece.piece_type + 10
                else:
                   im = 0
                screen.blit(pieces[(x + y) % 2][im] ,(x * 32, (224 - y * 32)))
        stra = 'Clock: {} - {}'.format(self.time_left,self.time_right)
        ren = self.font.render('Clock: {} - {}'.format(self.time_left,self.time_right), 0, self.fg)
        a = screen.blit(ren, (0,256))
        ren = self.font.render(' Level: {} '.format(self.level),0,self.fg)
        a = screen.blit(ren, (256,0))
        ren = self.font.render(self.timetext,0,self.fg)
        a = screen.blit(ren, (256,80))
        ren = self.font.render(self.info,0,self.fg)
        a = screen.blit(ren, (256,144))
        pygame.display.flip()
        #pygame.display.update()

    def run(self):

        while True:
            #
            # Check if we have something to display
            message = self.msg_queue.get()

            for case in switch(message):
                if case(MessageApi.USER_MOVE):
                    self.board=message.game

                    break
                if case(MessageApi.COMPUTER_MOVE):
                    self.board=message.game
                    #displaybrd(message.game)

                    print('\n' + message.fen)
                    #print(message.game.fen())
                    #print('emulate user to make the computer move...sleeping for one second')
                    #time.sleep(1)
                    logging.debug('emulate user now finished doing computer move')
                    DisplayMsg.show(Message.DGT_FEN(fen=message.game.board_fen()))
                    break
                if case(MessageApi.SEARCH_STARTED):
                    if message.engine_status == EngineStatus.THINK:
                        print('Computer starts thinking')
                    if message.engine_status == EngineStatus.PONDER:
                        print('Computer starts pondering')
                    if message.engine_status == EngineStatus.WAIT:
                        print('Computer starts waiting - hmmm')
                    break
                if case(MessageApi.SEARCH_STOPPED):
                    if message.engine_status == EngineStatus.THINK:
                        print('Computer stops thinking')
                    if message.engine_status == EngineStatus.PONDER:
                        print('Computer stops pondering')
                    if message.engine_status == EngineStatus.WAIT:
                        print('Computer stops waiting - hmmm')
                    break
                if case(MessageApi.DGT_CLOCK_TIME):

                    self.time_left = message.time_left
                    self.time_right = message.time_right
                    self.displaybrd()

                    #self.py.displaybrd()

                    break;
                if case(MessageApi.LEVEL):
                    self.level = message.level
                    self.displaybrd()
                    break
                if case(MessageApi.RUN_CLOCK):
                    self.timetext = message.time_control.mode.value
                    self.displaybrd()
                    break
                if case(MessageApi.DISPLAY_TEXT):
                    self.info = message.text
                    self.displaybrd()
                    break
                if case():  # Default
                    pass
                #time.sleep(1)
