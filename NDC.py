import pyxel

class App:
    def __init__(self) -> None:
        
        self.currentState = "in_game"

        self.key_up = pyxel.KEY_UP
        self.key_down = pyxel.KEY_DOWN
        self.key_left = pyxel.KEY_LEFT
        self.key_right = pyxel.KEY_RIGHT

        self.map =  [[2 for y in range(14)] for x in range(16)]

        self.player = {'x' : 0, 'y' : 0}

        self.map[self.player['x']][self.player['y']] = 0

        self.timer = 60

        pyxel.init(256, 256, title="NDC")
        pyxel.run(self.update, self.draw)

    def update(self): getattr(self, f"update_{self.currentState}")()
    def draw(self): getattr(self, f"draw_{self.currentState}")()

    #Air       = 0
    #Chest     = 1
    #Breakable = 2
    #Unbreak   = 3 
    #Ladder    = 4
    #Exit      = 5


    def update_title_screen(self):
        if pyxel.btn(pyxel.KEY_RETURN):
            self.currentState = "in_game"

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

    def draw_title_screen(self): pass

    def update_in_game(self):
        #Player movement:
        if pyxel.btnp(pyxel.KEY_DOWN):
            if self.player['y'] < 13 and self.map[self.player['x']][self.player['y']+1] == 2:
                self.map[self.player['x']][self.player['y']+1] = 0
            while self.player['y'] < 13 and self.map[self.player['x']][self.player['y']+1] in [0, 1, 4, 5]: 
                self.player['y'] += 1

        if pyxel.btnp(pyxel.KEY_RIGHT): 
            if self.player['x'] < 15 and self.map[self.player['x']+1][self.player['y']] in [1, 2]:
                self.map[self.player['x']+1][self.player['y']] = 0
            if self.player['x'] < 15 and self.map[self.player['x']+1][self.player['y']] in [0, 4, 5]:
                self.player['x'] += 1

        if pyxel.btnp(pyxel.KEY_LEFT):
            if self.player['x'] > 0 and self.map[self.player['x']-1][self.player['y']] in [1, 2]:
                self.map[self.player['x']-1][self.player['y']] = 0
            if self.player['x'] > 0 and self.map[self.player['x']-1][self.player['y']] in [0, 4, 5]:
                self.player['x'] -= 1

        if pyxel.btnp(pyxel.KEY_UP) and self.map[self.player['x']][self.player['y']] == 4:
            if self.player['y'] > 0 and self.map[self.player['x']][self.player['y']] == 2:
                self.map[self.player['x']][self.player['y']] == 0
            if self.player['y'] > 0 and self.map[self.player['x']][self.player['y']-1] in [0, 1, 4]:
                self.player['y'] -= 1 

    def draw_in_game(self): 
        for x in range(16):
            for y in range(14):
                pyxel.rect(x*16, y*16+32, 16, 16, self.map[x][y])
        pyxel.rect(self.player['x']*16, self.player['y']*16+32, 16, 16, 7)

App()
