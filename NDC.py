import pyxel

class App:
    def __init__(self) -> None:
        
        self.current_state = "title_screen"

        self.looking_at = "r"

        self.last_move = None

        self.key_up = pyxel.KEY_UP
        self.key_down = pyxel.KEY_DOWN
        self.key_left = pyxel.KEY_LEFT
        self.key_right = pyxel.KEY_RIGHT

        self.map =  [[2, 2, 2, 3, 3, 2, 2, 2, 2, 1, 3, 3, 2, 2],
                    [2, 2, 2, 1, 3, 2, 2, 2, 2, 2, 3, 3, 2, 2],
                    [2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 3, 2, 2],
                    [2, 2, 1, 4, 4, 4, 3, 2, 2, 0, 0, 0, 2, 2],
                    [2, 2, 2, 2, 2, 2, 3, 1, 2, 2, 2, 2, 2, 2],
                    [2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2],
                    [2, 2, 2, 2, 2, 2, 1, 3, 2, 1, 2, 2, 2, 2],
                    [2, 2, 0, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                    [2, 1, 0, 3, 3, 2, 0, 0, 2, 2, 4, 4, 4, 4],
                    [2, 2, 0, 1, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                    [2, 2, 2, 2, 2, 2, 4, 4, 4, 3, 2, 2, 2, 2],
                    [2, 0, 0, 2, 2, 2, 2, 2, 2, 3, 3, 3, 2, 2],
                    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2],
                    [4, 4, 4, 4, 3, 3, 3, 4, 4, 4, 4, 3, 1, 2],
                    [2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                    [2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2], ]

        self.player = {'x' : 0, 'y' : 0}

        self.map[self.player['x']][self.player['y']] = 0

        self.timer = 60

        pyxel.init(256, 256, title="NDC")
        
        pyxel.load("theme2.pyxres")
        
        pyxel.run(self.update, self.draw)

    def update(self): getattr(self, f"update_{self.current_state}")()
    def draw(self): getattr(self, f"draw_{self.current_state}")()

    #Air       = 0
    #Chest     = 1
    #Breakable = 2
    #Unbreak   = 3 
    #Ladder    = 4
    #Exit      = 5


    def update_title_screen(self):
        if pyxel.btn(pyxel.KEY_RETURN):
            self.current_state = "in_game"

        if pyxel.btn(pyxel.KEY_UP):
            self.key_up = pyxel.KEY_UP
            self.key_down = pyxel.KEY_DOWN
            self.key_left = pyxel.KEY_LEFT
            self.key_right = pyxel.KEY_RIGHT
        elif pyxel.btn(pyxel.KEY_Z):
            self.key_up = pyxel.KEY_Z
            self.key_down = pyxel.KEY_S
            self.key_left = pyxel.KEY_Q
            self.key_right = pyxel.KEY_D
        elif pyxel.btn(pyxel.KEY_W):
            self.key_up = pyxel.KEY_W
            self.key_down = pyxel.KEY_S
            self.key_left = pyxel.KEY_A
            self.key_right = pyxel.KEY_D

        if pyxel.btn(pyxel.KEY_1):
            self.timer = 90
        elif pyxel.btn(pyxel.KEY_2):
            self.timer = 60
        elif pyxel.btn(pyxel.KEY_3):
            self.timer = 30

    def draw_title_screen(self):
        pyxel.cls(0)
        for i in range(16):
            for j in range(14):
                pyxel.blt(i * 16, j * 16 + 32, 0, 0, 0, 16, 16)

        for i in range(16):
            for j in range(2):
                pyxel.blt(i * 16, j * 16, 0, 0, 80, 16, 16)

        pyxel.blt(16,16, 0, 0, 16, 16, 16, 11)

        pyxel.blt(48, 48, 0, 64, 48, 16, 16, 11)
        pyxel.blt(32, 64, 0, 80, 48, 16, 16, 11)
        pyxel.blt(48, 64, 0, 32, 48, 16, 16, 11)
        pyxel.blt(64, 64, 0, 48, 48, 16, 16, 11)

        pyxel.blt(120, 48, 0, 0, 48, 16, 16, 11)
        pyxel.blt(104, 64, 0, 16, 48, 16, 16, 11)
        pyxel.blt(120, 64, 0, 32, 48, 16, 16, 11)
        pyxel.blt(136, 64, 0, 48, 48, 16, 16, 11)

        pyxel.blt(192, 48, 0, 0, 64, 16, 16, 11)
        pyxel.blt(176, 64, 0, 16, 64, 16, 16, 11)
        pyxel.blt(192, 64, 0, 32, 64, 16, 16, 11)
        pyxel.blt(208, 64, 0, 48, 64, 16, 16, 11)

    def update_in_game(self):
        #Player movement:
        self.last_move = None
        already_moved = False

        if pyxel.btnp(pyxel.KEY_DOWN):
            already_moved = True
            self.last_move = "d"
            if self.player['y'] < 13 and self.map[self.player['x']][self.player['y']+1] == 2:
                self.map[self.player['x']][self.player['y']+1] = 0

        if not already_moved and pyxel.btnp(pyxel.KEY_RIGHT): 
            self.looking_at = "r"
            self.last_move = "d"
            already_moved = True
            if self.player['x'] < 15 and self.map[self.player['x']+1][self.player['y']] in [1, 2]:
                self.map[self.player['x']+1][self.player['y']] = 0
            if self.player['x'] < 15 and self.map[self.player['x']+1][self.player['y']] in [0, 4, 5]:
                self.player['x'] += 1

        if not already_moved and pyxel.btnp(pyxel.KEY_LEFT):
            self.looking_at = "l"
            already_moved = True
            if self.player['x'] > 0 and self.map[self.player['x']-1][self.player['y']] in [1, 2]:
                self.map[self.player['x']-1][self.player['y']] = 0
            if self.player['x'] > 0 and self.map[self.player['x']-1][self.player['y']] in [0, 4, 5]:
                self.player['x'] -= 1

        if not already_moved and pyxel.btnp(pyxel.KEY_UP) and self.map[self.player['x']][self.player['y']] == 4:
            if self.player['y'] > 0 and self.map[self.player['x']][self.player['y']-1] == 2:
                self.map[self.player['x']][self.player['y']-1] = 0
            if self.player['y'] > 0 and self.map[self.player['x']][self.player['y']-1] in [0, 1, 4]:
                self.player['y'] -= 1 

        #Make chests fall
        for x in range(16):
            for y in range(14):
                if self.map[x][y] == 1:
                    chest_y = y
                    while chest_y < 13 and self.map[x][chest_y+1] in [0, 1]: 
                        chest_y += 1
                    if chest_y != y: 
                        if self.map[x][chest_y] == 1: chest_y -= 1
                        self.map[x][y] = 0
                        self.map[x][chest_y] = 1

        #Make player fall
        if self.last_move != None:
            while self.player['y'] < 13 and self.map[self.player['x']][self.player['y']+1] in [0, 1, 4, 5]: 
                self.player['y'] += 1

    def draw_in_game(self): 
        pyxel.cls(0)
        for x in range(16):
            for y in range(14):
                pyxel.blt(x*16, y*16+32, 0, 16*self.map[x][y], 0, 16, 16)
        if self.looking_at == "r": pyxel.blt(self.player['x']*16, self.player['y']*16+32, 0, 0, 16, 16, 16, 11)
        elif self.looking_at == "l": pyxel.blt(self.player['x']*16, self.player['y']*16+32, 0, 32, 16, 16, 16, 11)

App()
