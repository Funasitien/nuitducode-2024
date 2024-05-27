import pyxel

class App:
    def __init__(self) -> None:
        
        self.currentState = "title_screen"

        self.key_up = pyxel.KEY_UP
        self.key_down = pyxel.KEY_DOWN
        self.key_left = pyxel.KEY_LEFT
        self.key_right = pyxel.KEY_RIGHT

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


    def draw_title_screen(self): 


App()
