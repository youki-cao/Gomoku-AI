# encoding: utf-8
import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(curPath)
import numpy, pygame

import Chessboard
class Gomoku():

    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("五子棋")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(r"ncsj.ttf", 24)
        self.going = True

        self.chessboard = Chessboard.Chessboard()


    def getStyle(self):
        background = pygame.image.load('bg.png').convert()
        mouse_cursor = pygame.image.load('white.png').convert_alpha()
        button = pygame.image.load('button.png').convert()
        pic1 = pygame.image.load('pic1.png').convert()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    x+= mouse_cursor.get_width() / 2
                    y-= mouse_cursor.get_height() / 2
                    self.screen.blit(pic1, (0, 0))
                    if x>400 and x<520 and y>300 and y<360:
                        return '3'
                    self.screen.blit(pic1, (0, 0))
                    pygame.display.update()
                    return '4'

            self.screen.blit(background, (0, 0))
            self.screen.blit(button, (400, 300))
            x, y = pygame.mouse.get_pos()
            x-= mouse_cursor.get_width() / 2
            y-= mouse_cursor.get_height() / 2
            self.screen.blit(mouse_cursor, (x, y))
            pygame.display.update()

    def loop(self):
        while self.going:
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    def update(self, table):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.going = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                self.chessboard.handle_key_event(e, table)
#        return (x, y)

    def draw(self):
        self.screen.fill((255, 255, 255))

        self.chessboard.draw(self.screen)
        if self.chessboard.game_over:
            self.screen.blit(self.font.render("{0} Win".format("Black" if self.chessboard.winner == 'b' else "White"), True, (0, 0, 0)), (500, 10))
        pygame.display.update()


if __name__ == '__main__':
    game = Gomoku()
    game.loop()