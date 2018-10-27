#!/usr/bin/env python
# encoding: utf-8

from table import TABLE,row,col, black, white,space
from value_function import NODE, valueFunc1
from value_function2 import valueFunc2
from value_function3 import valueFunc3
from value_function4 import valueFunc4, valueFunc5
from minmax_play import alpha_beta
from VCT import VCTFab, VCTFv4, VCTFmc
from mcts import mcts
from openDict import ovab, ovv4, ovmc
#from miniMax import alphaBeta, miniMax
from randomPlay import randPos
import Chessboard, gomoku, sys, pygame, time


class UnicodeStreamFilter:
    def __init__(self, target):
        self.target = target
        self.encoding = 'utf-8'
        self.errors = 'replace'
        self.encode_to = self.target.encoding

    def write(self, s):
        if type(s) == str:
            s = s.decode("utf-8")
        s = s.encode(self.encode_to, self.errors).decode(self.encode_to)
        self.target.write(s)

if sys.stdout.encoding == 'cp936':
    sys.stdout = UnicodeStreamFilter(sys.stdout)

def moveByHuman(status, table, game):
    game.chessboard.gogogo = True
    screen = pygame.display.set_mode((800, 600))
    mouse_cursor = pygame.image.load('white.png').convert_alpha()
    while game.chessboard.gogogo:
        game.update(table.table)
        game.draw()
        x, y = pygame.mouse.get_pos()
        x-= mouse_cursor.get_width() / 2
        y-= mouse_cursor.get_height() / 2
        screen.blit(mouse_cursor, (x, y))
        pygame.display.update()
        game.clock.tick(60)
    x = game.chessboard.prevX
    y = game.chessboard.prevY
    table.move(x, y, status)
    return (x, y)


def moveByAI(table, deep, status, game, AItype='value4'):
    node = NODE(table, deep, status)
    if AItype=='rand':
        randPos(node)
    elif AItype=='value1':
        valueFunc1(node, game)
    elif AItype=='value2':
        valueFunc2(node, game)
    elif AItype=='value3':
        valueFunc3(node)
    elif AItype=='Local Valuation':
        table.value += status * valueFunc4(node, game, printSc=False)
    elif AItype=='MCTS':
        mcts(node,game)
    elif AItype=='Multi-level Negascoutx':
        alpha_beta(node, 2, game, dist=2)
    elif AItype=='LV with Opening Lib and VCT':
        ovv4(node, game)
    elif AItype=='MN with Opening Lib and VCT':
        ovab(node, game)
    elif AItype=='MCTS with Opening Lib and VCT':
        ovmc(node, game)
    elif AItype=='LV with VCT':
        VCTFv4(node, game)
    elif AItype=='MN with VCT':
        VCTFab(node, game)
    elif AItype=='MCTS with VCT':
        VCTFmc(node, game)

    x, y = node.pos_i, node.pos_j
    if game.chessboard.set_piece(x, y):
        game.chessboard.check_win(x, y)
    game.draw()
    table.move(x, y, status)
    game.draw()
    return (x, y)

def start():
    pygame.init()
    pygame.display.set_caption("五子棋")
#    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    background = pygame.image.load('bg.png').convert()
    font = pygame.font.Font(r"ncsj.ttf", 30)
#        mouse_cursor = pygame.image.load('white.png').convert_alpha()
    B1 = pygame.image.load('B1.png').convert()
    B2 = pygame.image.load('B2.png').convert()
    B3 = pygame.image.load('B3.png').convert()
    B4 = pygame.image.load('B4.png').convert()
    B5 = pygame.image.load('B5.png').convert()
    B6 = pygame.image.load('B6.png').convert()

    B7 = pygame.image.load('B6.png').convert()
    B8 = pygame.image.load('B6.png').convert()
    B9 = pygame.image.load('B6.png').convert()
    B10 = pygame.image.load('B10.png').convert()
    B11 = pygame.image.load('B11.png').convert()
    B12=pygame.image.load('B12.png').convert()
    B13=pygame.image.load('B13.png').convert()
    B14=pygame.image.load('B14.png').convert()
    pic1 = pygame.image.load('pic1.png').convert()
    pic2 = pygame.image.load('pic2.png').convert()
    pic3 = pygame.image.load('pic3.png').convert()
    pic4 = pygame.image.load('pic4.png').convert()
    pic5 = pygame.image.load('pic5.png').convert()
    pic6 = pygame.image.load('pic6.png').convert()
    pic7 = pygame.image.load('pic7.png').convert()
    pic8 = pygame.image.load('pic8.png').convert()
    pic9 = pygame.image.load('pic9.png').convert()
    pics = [pic1, pic2, pic3, pic4, pic5, pic6, pic7, pic8, pic9]
    blacktype=['LV with Opening Lib and VCT', 'Local Valuation', 'LV with VCT', 'MN with Opening Lib and VCT', 'Multi-level Negascoutx', 'MN with VCT', 'MCTS with Opening Lib and VCT', 'MCTS', 'MCTS with VCT']

    whitetype=['LV with Opening Lib and VCT', 'Local Valuation', 'LV with VCT', 'MN with Opening Lib and VCT', 'Multi-level Negascoutx', 'MN with VCT', 'MCTS with Opening Lib and VCT', 'MCTS', 'MCTS with VCT']

    picid = 0
    pic = pic4
    isB1 = False # 开始pre
    isB2 = False# 进入demo!
    isB3 = False # 下一页
    isB4 = False # 返回
    isB5 = True# 人机对战
    isB6 = True

    isB7=False
    isB8=False
    isB9=False
    isB10=False
    isB11=False
    isB12=False
    isB13=False
    isB14=False
    blackk=0
    whitee=0
    while True:
        for event in pygame.event.get():
            # ai对战
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                screen.blit(pic1, (0, 0))
                if x>10 and x<130 and y>10 and y<70 and isB4 is True:
                #点击返回
                    pic = pic4
                    isB1 = False # 开始pre
                    isB2 = False # 进入demo
                    isB3 = False # 下一页
                    isB4 = False # 返回
                    isB5 = True # 人机对战
                    isB6 = True # ai对战
                    isB7=False
                    isB8=False
                    isB9=False
                    isB10=False
                    isB11=False
                    isB12=False
                    isB13=False
                    isB14 =False
                if x>300 and x<500 and y>300 and y<400 and isB1 is True:
                #点击开始
                    '''
                    picid = 3
                    pic = pics[picid]
                    isB1 = False # 开始pre
                    isB2 = True # 进入demo
                    isB3 = True # 下一页
                    isB4 = True # 返回
                    isB5 = True # 人机对战
                    isB6 = True
                    '''
                    picid = 3
                    pic = pics[picid]
                    isB1 = False # 开始pre
                    isB2 = False # 进入demo
                    isB3 = False# 下一页
                    isB4 = True # 返回
                    isB5 = True # 人机对战
                    isB6 = True # ai对战
                    isB7=False
                    isB8=False
                    isB9=False
                    isB10=False
                    isB11=False
                    isB12=False
                    isB13=False
                if x>10 and x<130 and y>530 and y<590 and isB2 is True:
                #点击进入
                    picid = 3
                    pic = pics[picid]
                    isB1 = False # 开始pre
                    isB2 = True # 进入demo
                    isB3 = True # 下一页
                    isB4 = True # 返回
                    isB5 = True # 人机对战
                    isB6 = True # ai对战

                    '''
                    elif picid == 8:
                        pygame.mixer.music.load('firstblood.mp3')
                        pygame.mixer.music.play(loops=0, start=0.0)
                        pic = pics[picid]
                        isB1 = False # 开始pre
                        isB2 = True # 进入demo
                        isB3 = False # 下一页
                        isB4 = True # 返回
                        isB5 = False # 人机对战
                        isB6 = False # ai对战
                    else:
                        pic = pics[picid]
                        isB1 = False # 开始pre
                        isB2 = True # 进入demo
                        isB3 = True # 下一页
                        isB4 = True # 返回
                        isB5 = False # 人机对战
                        isB6 = False # ai对战
                    '''
                if x>300 and x<500 and y>250 and y<350 and isB5 is True:
                #点击进入
                    '''
                    picid = 3
                    pic = pics[picid]
                    isB1 = False # 开始pre
                    isB2 = False # 进入demo
                    isB3 = False# 下一页
                    isB4 = True # 返回
                    isB5 = False # 人机对战
                    isB6 = False # ai对战
                    isB7=True
                    isB8=True
                    isB9=True
                    '''
                    picid=3
                    pic=pics[picid]
                    isB1 = False # 开始pre
                    isB2 = False # 进入demo
                    isB3 = True# 下一页
                    isB4 = False # 返回
                    isB5 = False # 人机对战
                    isB6 = False # ai对战
                    isB7=False
                    isB8=False
                    isB9=False

                if x>200 and x<400 and y>300 and y<400 and isB10 is True:


                    isB1 = False # 开始pre
                    isB2 = False # 进入demo
                    isB3 = True# 下一页
                    isB4 = False # 返回
                    isB5 = False # 人机对战
                    isB6 = False # ai对战
                    isB7=False
                    isB8=False
                    isB9=False
                    isB10=False
                    isB11=False
                    isB14 = False
                    picid=8
                    style = '2'
                if x>400 and x<600 and y>300 and y<400 and isB11 is True:


                    isB1 = False # 开始pre
                    isB2 = False # 进入demo
                    isB3 = True# 下一页
                    isB4 = False # 返回
                    isB5 = False # 人机对战
                    isB6 = False # ai对战
                    isB7=False
                    isB8=False
                    isB9=False
                    isB10=False
                    isB11=False
                    isB14 = False
                    picid=8
                    style = '3'
                if x>200 and x<400 and y>0 and y<100 and isB12 is True:


                    isB1 = False # 开始pre
                    isB2 = False # 进入demo
                    isB3 = False# 下一页
                    isB4 = True # 返回
                    isB5 = False # 人机对战
                    isB6 = False # ai对战
                    isB7=False
                    isB8=False
                    isB9=False
                    isB10=False
                    isB11=False
                    isB14=True
                    if blackk==len(blacktype)-1:
                        blackk=0
                    else :
                        blackk+=1

                if x>400 and x<600 and y>0 and y<100 and isB13 is True:


                    isB1 = False # 开始pre
                    isB2 = False # 进入demo
                    isB3 = False# 下一页
                    isB4 = True # 返回
                    isB5 = False # 人机对战
                    isB6 = False # ai对战
                    isB7=False
                    isB8=False
                    isB9=False
                    isB10=False
                    isB11=False
                    isB14=True
                    if whitee==len(blacktype)-1:
                        whitee=0
                    else :
                        whitee+=1

                if x>300 and x<500 and y>500 and y<600 and isB14 is True:
                    play(style,blacktype[blackk],whitetype[whitee])
                    picid = 3
                    pic = pics[picid]
                    isB1 = False # 开始pre
                    isB2 = False # 进入demo
                    isB3 = False # 下一页
                    isB4 = False # 返回
                    isB5 = True # 人机对战
                    isB6 = True # ai对战
                    isB7=False
                    isB8=False
                    isB9=False
                    isB10=False
                    isB11=False
                    isB12=False
                    isB13=False
                    isB14=False


                if x>300 and x<500 and y>400 and y<500 and isB6 is True:
                #点击进入




                    picid = 7
                    pic = pics[3]
                    isB1 = False # 开始pre
                    isB2 = False # 进入demo
                    isB3 = True # 下一页
                    isB4 = False # 返回
                    isB5 = False# 人机对战
                    isB6 = False # ai对战
                    style = '4'
            if isB3 is True:
                #点击下一页
                    if picid==8:
                        pic=pics[3]
                        isB1 = False # 开始pre
                        isB2 = False # 进入demo
                        isB3 = False# 下一页
                        isB4 = True # 返回
                        isB5 = False # 人机对战
                        isB6 = False # ai对战
                        isB10=False
                        isB11=False
                        isB14=True
                        if style == '3':
                            isB12=True
                            isB13=False
                        else:
                            isB12=False
                            isB13=True
                    elif picid == 7:

                        pic = pics[3]
                        isB1 = False # 开始pre
                        isB2 = False#emo
                        isB3 = False # 下一页
                        isB4 = True # 返回
                        isB5 = False # 人机对战
                        isB6 = False # ai对战
                        isB7=False
                        isB8=False
                        isB9=False
                        isB10=False
                        isB11=False
                        isB12=True
                        isB13=True
                        isB14=True

                    else:


                        picid = 3
                        pic = pics[picid]
                        isB1 = False # 开始pre
                        isB2 = False # 进入demo
                        isB3 = False# 下一页
                        isB4 = True # 返回
                        isB5 = False # 人机对战
                        isB6 = False # ai对战
                        isB7=False
                        isB8=False
                        isB9=False
                        isB10=True
                        isB11=True
                        isB14=False

            clock.tick(30)
            screen.blit(pic, (0, 0))
            if isB1:
                screen.blit(B1, (600, 500))
            if isB2:
                screen.blit(B2, (10, 530))
            if isB3:
                screen.blit(B3, (670, 530))
            if isB4:
                screen.blit(B4, (10, 10))
            if isB5:
                screen.blit(B5, (300, 250))
            if isB6:
                screen.blit(B6, (300, 400))

            if isB7:
                screen.blit(B7,(300,100))
            if isB8:
                screen.blit(B8,(300,250))
            if isB9:
                screen.blit(B9,(300,400))
            if isB10:
                screen.blit(B10,(200,300))
            if isB11:
                screen.blit(B11,(400,300))
            if isB12:
                screen.blit(B12,(200,0))
                screen.blit(font.render('Black AI Type: %s' % blacktype[blackk], True, (0, 0, 0)), (100, 200))
            if isB13:
                screen.blit(B13,(400,0))
                screen.blit(font.render('White AI Type: %s' % whitetype[whitee], True, (0, 0, 0)), (100, 300))
            if isB14:
                screen.blit(B14,(300,500))
#            x, y = pygame.mouse.get_pos()
#            x-= mouse_cursor.get_width() / 2
#            y-= mouse_cursor.get_height() / 2
#            screen.blit(mouse_cursor, (x, y))
            pygame.display.update()



def menu():
    pass

def play(style,blacktype,whitetype):
#    if style == '3':
#        pygame.mixer.music.load('welcome.mp3')
#        pygame.mixer.music.play(loops=0, start=0.0)
#    pygame.mouse.set_visible(False)
    bwin = 0
    draw = 0
    wwin = 0
    print style,blacktype,whitetype
#    style = raw_input("Game Type: 1: HUMAN vs HUMAN\t 2: HUMAN vs AI\t\
#    3: AI vs HUMAN\t4: AI vs AI")
#    for _ in range(10):

    table = TABLE()
#    table.display()
#    AItype1 = raw_input("Input AItype: rand/value1")
#    AItype2 = raw_input("Input AItype: rand/value1")

    # 黑棋AI
    status = black
    deep = 0
    game = 0
    game = gomoku.Gomoku()
    game.draw()
    while True:
        if style == '1':
            x, y = moveByHuman(status, table, game)
        if style == '2':
            if status == black:
                x, y = moveByHuman(status, table, game)
            else:
                x, y = moveByAI(table, deep, status, game, whitetype)


        if style == '3':
            if status == white:
                x, y = moveByHuman(status, table, game)
            else:
                x, y = moveByAI(table, deep, status, game, blacktype)

        if style=='4':
            if status == white:
                x, y = moveByAI(table, deep, status, game, whitetype)

            else:
                x, y = moveByAI(table, deep, status, game, blacktype)



#        table.display()
        if table.judge(x, y, status):
            if status == black:
                bwin += 1

            else:
                wwin += 1
            print((bwin,wwin))
#            if style == '3':
#                pygame.mixer.music.load('victory.mp3')
#                pygame.mixer.music.play(loops=0, start=0.0)
#            table.display()
            time.sleep(3)
            pygame.mouse.set_visible(True)

            return
        elif table.is_full():
            draw += 1
#                table.display()
            pygame.mouse.set_visible(True)
            return
        else:
            #交换手
            status = -status



if __name__ == '__main__':
    start()
