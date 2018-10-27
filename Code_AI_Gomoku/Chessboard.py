# encoding: utf-8
import pygame




class Chessboard:

    def __init__(self):
        self.grid_size = 35
        self.start_x, self.start_y = 120, 80
        self.edge_size = self.grid_size / 2
        self.grid_count = 15
        self.piece = 'b'
        self.winner = None
        self.game_over = False
        self.prevX = -1
        self.prevY = -1
        self.gogogo = True

        self.grid = []
        for i in range(self.grid_count):
            self.grid.append(list("." * self.grid_count))

    def addToDict(self, table):
        f = open('openDict2.txt', 'a')
        go = True
        while go:
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN:
                    x, y = self.handle_key_event(e, table, 0)
                    print x, y
                    go = False
                    break
        for line in table:
            for item in line:
                f.write('%d,' % item)
            f.write('.')
        f.write('%d,%d' % (x, y))
        f.write('\n')
        f.close()

    def handle_key_event(self, e, table, Ty = 1):
        if Ty:
            origin_x = self.start_x - self.edge_size
            origin_y = self.start_y - self.edge_size
            size = (self.grid_count - 1) * self.grid_size + self.edge_size * 2
            pos = e.pos
            if origin_x <= pos[0] <= origin_x + size and origin_y <= pos[1] <= origin_y + size:
                if not self.game_over:
                    x = pos[0] - origin_x
                    y = pos[1] - origin_y
                    r = int(y // self.grid_size)
                    c = int(x // self.grid_size)
                    if self.set_piece(r, c, table):
                        self.check_win(r, c)
            if pos[0] >= origin_x + size and origin_y <= pos[1] <= origin_y + size:
                self.addToDict(table)
            return
        origin_x = self.start_x - self.edge_size
        origin_y = self.start_y - self.edge_size
        size = (self.grid_count - 1) * self.grid_size + self.edge_size * 2
        pos = e.pos
        if origin_x <= pos[0] <= origin_x + size and origin_y <= pos[1] <= origin_y + size:
            x = pos[0] - origin_x
            y = pos[1] - origin_y
            r = int(y // self.grid_size)
            c = int(x // self.grid_size)
            return (r, c)

    def set_piece(self, r, c, table = []):
        if self.grid[r][c] == '.':
            self.grid[r][c] = self.piece

            if self.piece == 'b':
                self.piece = 'w'
            else:
                self.piece = 'b'
            self.prevX = r
            self.prevY = c
            self.gogogo = False
            return True
        self.grid[r][c] = '.'
        if table:
            table[r][c] = 0
        return False

    def check_win(self, r, c):
        n_count = self.get_continuous_count(r, c, -1, 0)
        s_count = self.get_continuous_count(r, c, 1, 0)

        e_count = self.get_continuous_count(r, c, 0, 1)
        w_count = self.get_continuous_count(r, c, 0, -1)

        se_count = self.get_continuous_count(r, c, 1, 1)
        nw_count = self.get_continuous_count(r, c, -1, -1)

        ne_count = self.get_continuous_count(r, c, -1, 1)
        sw_count = self.get_continuous_count(r, c, 1, -1)

        if (n_count + s_count + 1 >= 5) or (e_count + w_count + 1 >= 5) or \
                (se_count + nw_count + 1 >= 5) or (ne_count + sw_count + 1 >= 5):
            self.winner = self.grid[r][c]
            self.game_over = True

    def get_continuous_count(self, r, c, dr, dc):
        piece = self.grid[r][c]
        result = 0
        i = 1
        while True:
            new_r = r + dr * i
            new_c = c + dc * i
            if 0 <= new_r < self.grid_count and 0 <= new_c < self.grid_count:
                if self.grid[new_r][new_c] == piece:
                    result += 1
                else:
                    break
            else:
                break
            i += 1
        return result

    def draw(self, screen):
        pygame.draw.rect(screen, (185, 122, 87),[0, 0, 800, 600], 0)

        for r in range(self.grid_count):
            y = self.start_y + r * self.grid_size
            pygame.draw.line(screen, (0, 0, 0), [self.start_x, y], [self.start_x + self.grid_size * (self.grid_count - 1), y], 2)

        for c in range(self.grid_count):
            x = self.start_x + c * self.grid_size
            pygame.draw.line(screen, (0, 0, 0), [x, self.start_y], [x, self.start_y + self.grid_size * (self.grid_count - 1)], 2)

        for r in range(self.grid_count):
            for c in range(self.grid_count):
                piece = self.grid[r][c]
                if piece != '.':
                    if piece == 'b':
                        color = (0, 0, 0)
                    else:
                        color = (255, 255, 255)

                    x = self.start_x + c * self.grid_size
                    y = self.start_y + r * self.grid_size
                    pygame.draw.circle(screen, color, [x, y], self.grid_size // 2)