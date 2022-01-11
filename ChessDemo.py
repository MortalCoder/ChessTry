import pygame as pg


class Piece:
    def __init__(self, x: int, y: int, color: bool, p_type: str):
        if color:
            self.pic = pg.transform.scale(pg.image.load(f'white_{p_type}.png').convert_alpha(), (75, 75))
        else:
            self.pic = pg.transform.scale(pg.image.load(f'black_{p_type}.png').convert_alpha(), (75, 75))
        self.p_type = p_type
        self.color = color
        self.x, self.y = x, y
        self.rect = (25+75*x, 25+75*y)
        self.moves = [[0 for i in range(8)] for j in range(8)]

    def move(self, new_x: int, new_y: int):
        global piece_board, white_check, black_check, picked, white_turn
        if self.color:
            meow_high.play()
        if not self.color:
            meow_low.play()
        if (self.color and white_turn and not white_check) or (not self.color and not white_turn and not black_check):
            if piece_board[new_y][new_x] == 0 or piece_board[new_y][new_x].p_type != 'king':
                piece_board[new_y][new_x] = self
                piece_board[self.y][self.x] = 0
                self.x, self.y = new_x, new_y
                picked = None
                white_turn = not white_turn

    def highlight(self):
        global piece_board
        hlt = pg.Surface((75, 75), pg.SRCALPHA)
        for row in range(8):
            for cell in range(8):
                if self.moves[row][cell] == 1:
                    hlt.fill((90, 90, 210, 150))
                    screen.blit(hlt, (25 + 75 * cell, 25 + 75 * row))
                elif self.moves[row][cell] == -1:
                    hlt.fill((210, 90, 90, 150))
                    screen.blit(hlt, (25 + 75 * cell, 25 + 75 * row))

    def check(self):
        global piece_board, white_check, black_check
        self.moves = [[0 for i in range(8)] for j in range(8)]
        if self.p_type == 'pawn':
            if self.color:
                try:
                    assert self.y - 1 >= 0
                    assert self.x + 1 < 8
                    if piece_board[self.y-1][self.x+1] != 0:
                        self.moves[self.y-1][self.x+1] = 1
                except AssertionError:
                    pass
                try:
                    assert self.x-1 >= 0
                    assert self.y-1 >= 0
                    if piece_board[self.y-1][self.x-1] != 0:
                        self.moves[self.y-1][self.x-1] = 1
                except AssertionError:
                    pass
                try:
                    assert self.y - 1 >= 0
                    if piece_board[self.y-1][self.x] == 0:
                        self.moves[self.y-1][self.x] = 1
                    elif piece_board[self.y-1][self.x] != 0:
                        self.moves[self.y - 1][self.x] = -1
                except AssertionError:
                    pass
                if self.y == 6 and not piece_board[self.y-2][self.x]:
                    self.moves[self.y-2][self.x] = 1
            else:
                try:
                    assert self.y + 1 < 8
                    assert self.x + 1 < 8
                    if piece_board[self.y+1][self.x+1] != 0:
                        self.moves[self.y+1][self.x+1] = 1
                except AssertionError:
                    pass
                try:
                    assert self.x-1 >= 0
                    assert self.y + 1 < 8
                    if piece_board[self.y+1][self.x-1] != 0:
                        self.moves[self.y+1][self.x-1] = 1
                except AssertionError:
                    pass
                try:
                    assert self.y + 1 < 8
                    if piece_board[self.y+1][self.x] == 0:
                        self.moves[self.y+1][self.x] = 1
                    elif piece_board[self.y+1][self.x] != 0:
                        self.moves[self.y+1][self.x] = -1
                except AssertionError:
                    pass
                if self.y == 1 and not piece_board[self.y+2][self.x]:
                    self.moves[self.y+2][self.x] = 1

        elif self.p_type == 'rook':
            for direction in range(4):
                pair = [0, 0]
                while True:
                    try:
                        assert 0 <= self.x + pair[0] < 8
                        assert 0 <= self.y + pair[1] < 8
                        if not (pair[0] == pair[1] == 0):
                            self.moves[self.y + pair[1]][self.x + pair[0]] = 1
                        if piece_board[self.y + pair[1]][self.x + pair[0]] != 0 and not (pair[0] == pair[1] == 0):
                            if self.color == piece_board[self.y + pair[1]][self.x + pair[0]].color:
                                self.moves[self.y + pair[1]][self.x + pair[0]] = -1
                                break
                            elif piece_board[self.y + pair[1]][self.x + pair[0]] != 0:
                                break
                    except AssertionError:
                        break
                    finally:
                        if direction == 0:
                            pair[0] -= 1
                        elif direction == 1:
                            pair[1] -= 1
                        elif direction == 2:
                            pair[0] += 1
                        elif direction == 3:
                            pair[1] += 1
        elif self.p_type == 'knight':
            for pair in [(-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1)]:
                try:
                    assert 0 <= self.y+pair[1] < 8
                    assert 0 <= self.x+pair[0] < 8
                    self.moves[self.y+pair[1]][self.x+pair[0]] = 1
                except AssertionError:
                    pass
        elif self.p_type == 'bishop':
            for direction in range(4):
                pair = [0, 0]
                while True:
                    try:
                        assert 0 <= self.x + pair[0] < 8
                        assert 0 <= self.y + pair[1] < 8
                        if not (pair[0] == pair[1] == 0):
                            self.moves[self.y + pair[1]][self.x + pair[0]] = 1
                        if piece_board[self.y + pair[1]][self.x + pair[0]] != 0 and not (pair[0] == pair[1] == 0):
                            if self.color == piece_board[self.y + pair[1]][self.x + pair[0]].color:
                                break
                            elif piece_board[self.y + pair[1]][self.x + pair[0]].p_type == 'king':
                                break
                    except AssertionError:
                        break
                    finally:
                        if direction == 0:
                            pair[0] -= 1
                            pair[1] -= 1
                        elif direction == 1:
                            pair[0] -= 1
                            pair[1] += 1
                        elif direction == 2:
                            pair[0] += 1
                            pair[1] -= 1
                        elif direction == 3:
                            pair[0] += 1
                            pair[1] += 1
        elif self.p_type == 'queen':
            pass
        elif self.p_type == 'king':
            for y_step in [-1, 0, 1]:
                for x_step in [-1, 0, 1]:
                    try:
                        assert 0 <= self.x + x_step < 8
                        assert 0 <= self.y + y_step < 8
                        self.moves[self.y + y_step][self.x + x_step] = 1
                    except AssertionError:
                        pass

        # Preventing from attacking king or same-color pieces
        for row in range(8):
            for col in range(8):
                if self.moves[row][col] == 1 and type(piece_board[row][col]) == Piece:
                    if piece_board[row][col].p_type == 'king':
                        if self.color != piece_board[row][col].color and self.color:
                            black_check = True
                        elif self.color != piece_board[row][col].color and not self.color:
                            white_check = True
                    elif piece_board[row][col].color == self.color:
                        self.moves[row][col] = -1

    def draw(self):
        global white_turn
        self.check()
        if mouse_cords == [self.x, self.y] and self.color == white_turn:
            self.highlight()
        self.rect = (25 + 75 * self.x, 25 + 75 * self.y)
        screen.blit(self.pic, self.rect)


screen = pg.display.set_mode((75*8+50, 75*8+50))
game_clock = pg.time.Clock()
pg.display.set_caption('Chess practice')

pg.mixer.init()
meow = pg.mixer.Sound('meow.wav')
meow_low = pg.mixer.Sound('meow_low.wav')
meow_high = pg.mixer.Sound('meow_high.wav')

pg.font.init()
pixel_font = pg.font.Font('FreePixel.ttf', 16)

mouse_cords = (0, 0)
piece_board = [[0 for i in range(8)] for j in range(8)]
white_turn, white_check, black_check = True, False, False
picked = False


def show_board():
    for row in [['0' if i == 0 else '1' for i in j] for j in piece_board]:
        print(' | '.join(row))


def click_debug():
    print('Debug log ---------------------------')
    if white_turn:
        print('White turn')
    if not white_turn:
        print('Black turn')
    if white_check:
        print('White Check!')
    if black_check:
        print('Black Check!')
    if type(picked) == Piece:
        print(f'Piece: {picked.p_type}, Color: {["Black", "White"][picked.color]}, X, Y: {picked.x, picked.y}')
    if type(picked) != Piece:
        print(f'Empty Cell at x: {mouse_cords[0]}, y: {mouse_cords[1]}')


def place_board():
    global piece_board

    piece_board = [[0 for i in range(8)] for j in range(8)]

    for k in range(8):
        piece_board[1][k] = Piece(k, 1, False, 'pawn')
        piece_board[6][k] = Piece(k, 6, True, 'pawn')

    piece_board[0][0], piece_board[0][7] = Piece(0, 0, False, 'rook'), Piece(7, 0, False, 'rook')
    piece_board[0][1], piece_board[0][6] = Piece(1, 0, False, 'knight'), Piece(6, 0, False, 'knight')
    piece_board[0][2], piece_board[0][5] = Piece(2, 0, False, 'bishop'), Piece(5, 0, False, 'bishop')
    piece_board[0][3], piece_board[0][4] = Piece(3, 0, False, 'king'), Piece(4, 0, False, 'queen')

    piece_board[7][0], piece_board[7][7] = Piece(0, 7, True, 'rook'), Piece(7, 7, True, 'rook')
    piece_board[7][1], piece_board[7][6] = Piece(1, 7, True, 'knight'), Piece(6, 7, True, 'knight')
    piece_board[7][2], piece_board[7][5] = Piece(2, 7, True, 'bishop'), Piece(5, 7, True, 'bishop')
    piece_board[7][3], piece_board[7][4] = Piece(3, 7, True, 'king'), Piece(4, 7, True, 'queen')


def run():
    global mouse_cords, picked, white_turn

    place_board()

    running = True
    while running:
        game_clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_cords = list(pg.mouse.get_pos())
                mouse_cords[0], mouse_cords[1] = (mouse_cords[0] - 25) // 75, (mouse_cords[1] - 25) // 75
                if type(picked) == Piece:
                    if picked.color == white_turn:
                        if picked.moves[mouse_cords[1]][mouse_cords[0]] == 1:
                            piece_board[picked.y][picked.x].move(mouse_cords[0], mouse_cords[1])
                        else:
                            picked = piece_board[mouse_cords[1]][mouse_cords[0]]
                picked = piece_board[mouse_cords[1]][mouse_cords[0]]
                click_debug()
                try:
                    print(*piece_board[mouse_cords[1]][mouse_cords[0]].moves, sep='\n')
                except:
                    pass
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    show_board()

        # Logics

        # Render

        # Заполняем экран фоновым цветом
        screen.fill((30, 30, 30))
        # Вывод полей по бокам
        for i in range(8):
            screen.blit(pixel_font.render(str(8-i), True, (240, 240, 240),  (30, 30, 30)), (8, 60+75*i))
            screen.blit(pixel_font.render(str(8-i), True, (240, 240, 240), (30, 30, 30)), (75*8+32, 60 + 75 * i))
        for i in range(8):
            screen.blit(pixel_font.render('ABCDEFGH'[i], True, (240, 240, 240),  (30, 30, 30)), (60+75*i, 5))
            screen.blit(pixel_font.render('ABCDEFGH'[i], True, (240, 240, 240), (30, 30, 30)), (60 + 75 * i, 75*8+32))
        # При помощи цикла выводим 8*8 клеток
        for y in range(8):
            for x in range(8):
                # Сначала создаем клетку
                cell = pg.Surface((75, 75))
                # Если сумма координат нечетна, то клетка заполняется светлым цветом
                if (x + y) % 2 == 1:
                    cell.fill((170, 200, 130))
                # Если же сумма координат четна, то клетка заполняется темным цветом
                else:
                    cell.fill((65, 130, 65))
                # Затем клетка вставляется в свое место
                screen.blit(cell, (25 + 75 * x, 25 + 75 * y))
        # Вырисовка всех фигур на доске
        for row in piece_board:
            for col in row:
                if type(col) == Piece:
                    col.draw()

        # FLIP IT!
        pg.display.flip()


run()

pg.quit()
