# Gomoku-AI

Final Project for AI course at Fudan University

## Environment

The code, including demo, is written in Python 2.7. And demo is made by pygame. 

## Originality

Some code are borrowed from others. But most of them is used for debugging, including the code for printing chessboard in command line. The only borrowed code we adapted is the structure of NODE and TABLE class, including its move and judge method, from HackerSir’s GitHub. The final edition of the project has 2232 lines of code, and 1846 of them are original.
The algorithm for VCT and Local Valuation are totally original, and VCT perfroms really good.

## How to Use the Demo

Since we used pygame to build the demo, you should first install it by pip install pygame
Then, run play.py with Python 2.7, the demo will pop out.
Choose Human vs AI or AI vs AI, and change AI type by clicking the button at the top of the window.
There are 9 types of AIs. They are Cartesian product of three algorithms and some reinforcement–Basic algorithm, with VCT and with both Opening Lib and VCT.
Blue and red dots means the program is calculating score of the points, red dots are better than the blue ones. Purple dots means it is simulating that point using MCTS. Green ones means it is calculating VCF, and pink ones represent VCT.

- Collaborators: Shangyi Ning, Peng Zhang
