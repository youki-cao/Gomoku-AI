# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 05:04:19 2017

@author: dell
"""

import pygame, time

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("五子棋")
pygame.font.Font(r"ncsj.ttf", 24)
screen.fill((255, 255, 255))
time.sleep(10)
pygame.quit()
