import pyxel
from threading import Thread
from time import time


class App:
    def __init__(self) -> None:
        self.map_number = -1
        self.map, self.map_title = self.get_new_level()

        self.first_pause = True

        self.fade_x, self.fade_y = -16, 0
        self.fade_dir = 1
        
        self.level = 1        
        self.chest_opend = [0, 0, 0]        
        self.chest_opend = [0, 0, 0]

        self.slow_fall = False

        self.idle_animation = False
        self.animation_frame = 0
        
        self.current_state = "title_screen"

        self.looking_at = "r"

        self.last_move = None

        self.key_up = pyxel.KEY_W
        self.key_down = pyxel.KEY_S
        self.key_left = pyxel.KEY_A
        self.key_right = pyxel.KEY_D

        self.currentXGold = [120, 104, 120, 136]
        self.currentYGold = 128
        
        self.score = 0

        self.is_pause_menu = False

        self.player = {'x' : 0, 'y' : 0}

        self.chest_opend = [0, 0, 0]

        self.map[self.player['x']][self.player['y']] = 0
        
        self.difficulty = 0
        self.timer = 90

        pyxel.init(256, 256, title="NDC", fps=60)
        
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
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.current_state = "in_game"
            self.first_pause = False
            self.is_pause_menu = False
            self.last_time_moved = time()
            Thread(target=self.decrement_time, daemon=True).start()

        if pyxel.btn(pyxel.KEY_UP):
            self.key_up = pyxel.KEY_UP
            self.key_down = pyxel.KEY_DOWN
            self.key_left = pyxel.KEY_LEFT
            self.key_right = pyxel.KEY_RIGHT
            self.currentXGold = [192, 176, 192, 208]
        elif pyxel.btn(pyxel.KEY_Z):
            self.key_up = pyxel.KEY_Z
            self.key_down = pyxel.KEY_S
            self.key_left = pyxel.KEY_Q
            self.key_right = pyxel.KEY_D
            self.currentXGold = [48, 32, 48, 64]
        elif pyxel.btn(pyxel.KEY_W):
            self.key_up = pyxel.KEY_W
            self.key_down = pyxel.KEY_S
            self.key_left = pyxel.KEY_A
            self.key_right = pyxel.KEY_D
            self.currentXGold = [120, 104, 120, 136]

        if pyxel.btn(pyxel.KEY_1 or pyxel.KEY_KP_1) and self.first_pause:
            self.timer = 90
            self.difficulty = 0
            self.currentYGold = 128
        elif pyxel.btn(pyxel.KEY_2 or pyxel.KEY_KP_1) and self.first_pause:
            self.timer = 60
            self.difficulty = 1
            self.currentYGold = 149
        elif pyxel.btn(pyxel.KEY_3 or pyxel.KEY_KP_3) and self.first_pause:
            self.timer = 30
            self.difficulty = 2
            self.currentYGold = 170
        self.chest_opend = [0, 0, 0]
    def draw_title_screen(self):
        pyxel.cls(0)
        for i in range(16):
            for j in range(14):
                pyxel.blt(i * 16, j * 16 + 32, 0, 0, 0, 16, 16)

        for i in range(16):
            for j in range(2):
                pyxel.blt(i * 16, j * 16, 0, [16, 0][j], 80, 16, 16)

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

        pyxel.blt(48, 96, 0, 64, 64, 156, 16, 11)

        pyxel.blt(64, 128, 0, 0, 110, 128, 16, 15)
        pyxel.blt(64, 149, 0, 0, 126, 128, 16, 15)
        pyxel.blt(64, 170, 0, 0, 142, 128, 16, 15)

        for i in range(4):
            pyxel.blt(self.currentXGold[i], [48, 64, 64, 64][i], 0, 96 + (self.difficulty * 16) , 48, 16, 16, 15)
        pyxel.blt(64, self.currentYGold, 0, 144, 48, 16, 16, 15)

    def update_in_game(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.current_state = "title_screen"
            self.is_pause_menu = True

        if self.slow_fall: return

        #Player movement:
        self.last_move = None
        already_moved = False

        if pyxel.btnp(self.key_down):
            already_moved = True
            self.last_move = "d"
            if self.player['y'] < 13 and self.map[self.player['x']][self.player['y']+1] == 2:
                self.map[self.player['x']][self.player['y']+1] = 0

        if not already_moved and pyxel.btnp(self.key_right): 
            self.looking_at = "r"
            self.last_move = "r"
            already_moved = True
            if self.player['x'] < 15 and self.map[self.player['x']+1][self.player['y']] == 2:
                self.map[self.player['x']+1][self.player['y']] = 0
            if self.player['x'] < 15 and self.map[self.player['x']+1][self.player['y']] in [0, 1, 4, 5]:
                self.player['x'] += 1

        if not already_moved and pyxel.btnp(self.key_left):
            self.looking_at = "l"
            self.last_move = "l"
            already_moved = True
            if self.player['x'] > 0 and self.map[self.player['x']-1][self.player['y']] == 2:
                self.map[self.player['x']-1][self.player['y']] = 0
            if self.player['x'] > 0 and self.map[self.player['x']-1][self.player['y']] in [0, 1, 4, 5]:
                self.player['x'] -= 1

        if not already_moved and pyxel.btnp(self.key_up) and self.map[self.player['x']][self.player['y']] == 4:
            if self.player['y'] > 0 and self.map[self.player['x']][self.player['y']-1] == 2:
                self.map[self.player['x']][self.player['y']-1] = 0
            if self.player['y'] > 0 and self.map[self.player['x']][self.player['y']-1] in [0, 1, 4]:
                self.player['y'] -= 1 

        if self.last_move != None: self.last_time_moved = time()

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
            self.falling_objects = [0, 1, 4, 5] if self.last_move == "d" else [0, 1, 5]
            last_y = self.player['y']
            while self.player['y'] < 13 and self.map[self.player['x']][self.player['y']+1] in self.falling_objects: 
                self.player['y'] += 1

            if self.player['y'] != last_y: self.slow_fall = True
            self.slow_fall_list = list(range((self.player['y']-last_y)*16, 0, -1))
            return

        #Player/Chest collision
        if self.map[self.player['x']][self.player['y']] == 1:
            self.chest_opend = [self.player['x'], self.player['y'], 60]
            self.score += 10
            self.map[self.player['x']][self.player['y']] = 0
            self.timer += 2

        if time()-self.last_time_moved >= 2:
            self.idle_animation = True
            self.animation_frame += 1
        else: 
            self.idle_animation = False

        #Player/Exit collsion
        if self.map[self.player['x']][self.player['y']] == 5: 
            self.level += 1
            self.map, self.map_title = self.get_new_level()
            self.player['y'] = 0
            self.map[self.player['x']][self.player['y']] = 0
            self.is_pause_menu = True
            self.current_state = "fading"

    def draw_in_game(self):             
        idle_show = 0
        pyxel.cls(0)

        for i in range(16):
            for j in range(2):
                pyxel.blt(i * 16, j * 16, 0, [16, 0][j], 80, 16, 16)

        pyxel.text(0, 0, f"Score : {self.score}", 0)
        pyxel.text(0, 10, f"Timer : {round(self.timer)}", 0)
        pyxel.text(0, 20, f"level : {self.level}", 0)
        pyxel.text(100, 15, f"Map Title : {self.map_title}", 0)

        for x in range(16):
            for y in range(14):
                pyxel.blt(x*16, y*16+32, 0, 16*self.map[x][y], 0, 16, 16, 11)

        player_show_x, player_show_y = self.player['x']*16, self.player['y']*16
        
        if self.slow_fall: 
            player_show_y -= self.slow_fall_list[0]
            self.slow_fall_list = self.slow_fall_list[1:]
            if not self.slow_fall_list: self.slow_fall = False

        idle_show = ( self.animation_frame % 64 )
        idle_show = 16 if idle_show >= 50 else 0
        if self.looking_at == "r": 
            if self.idle_animation: pyxel.blt(player_show_x, player_show_y+32, 0, idle_show, 16, 16, 16, 11)
            else: pyxel.blt(player_show_x, player_show_y+32, 0, 0, 16, 16, 16, 11)
        elif self.looking_at == "l": 
            if self.idle_animation: pyxel.blt(player_show_x, player_show_y+32, 0, 32+idle_show, 16, 16, 16, 11)
            else: pyxel.blt(player_show_x, player_show_y+32, 0, 32, 16, 16, 16, 11)

        if self.chest_opend[2] != 0:
            self.chest_opend[2] -= 1
            pyxel.text(self.chest_opend[0] * 16 + 8, self.chest_opend[1] * 16 + 3 + 0.15 * self.chest_opend[2], "+2", 7)

    def update_time_over(self): pass
    def draw_time_over(self): 
        pyxel.cls(0)
        pyxel.text(0, 0, f"Time's up ! You scored {self.score} ", 7)

    def update_fading(self): pass
    def draw_fading(self):
        self.fade_x += 32*self.fade_dir
        if (self.fade_x >= 256 and self.fade_dir == 1) or (self.fade_x < 0 and self.fade_dir == -1):
            self.fade_y += 16
            self.fade_x -= 16*self.fade_dir
            self.fade_dir *= -1
        pyxel.rect(self.fade_x, self.fade_y, 32, 16, 0)
        pyxel.rect(0, 0, 16, 16, 0)
        if self.fade_x >= 256 and self.fade_y >= 256: 
            self.current_state = "in_game"
            self.is_pause_menu = False
            Thread(target=self.decrement_time, daemon=True).start()
            self.fade_x = -16
            self.fade_y = 0
            self.fade_dir = 1

    def decrement_time(self):
        decrement_delay = last_time =time()
        while self.timer > 0 and not self.is_pause_menu: 
            current_time = time()
            decrement_delay = current_time - last_time
            last_time = current_time
            self.timer -= decrement_delay
        if self.is_pause_menu: return
        self.current_state = "time_over"

    def get_new_level(self): 
        map0 = [[2, 2, 2, 3, 3, 2, 2, 2, 2, 1, 3, 3, 2, 5],
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
                [4, 4, 4, 4, 2, 2, 2, 4, 4, 4, 4, 2, 1, 2],
                [2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2]]
        
        map2 = [[2, 2, 4, 4, 4, 4, 4, 3, 2, 3, 2, 3, 3, 5], 
                [3, 2, 2, 3, 3, 3, 2, 3, 2, 2, 2, 3, 3, 2], 
                [3, 3, 2, 2, 1, 3, 2, 2, 2, 3, 2, 3, 3, 2], 
                [3, 3, 2, 3, 2, 2, 2, 3, 3, 3, 2, 2, 2, 2], 
                [4, 4, 4, 3, 1, 3, 3, 3, 3, 3, 2, 3, 3, 2], 
                [2, 3, 2, 3 ,3, 1, 4, 4, 2, 2, 2, 3, 3, 2], 
                [1, 3, 2, 2, 2, 3, 3, 2, 3, 3, 2, 3, 3, 2], 
                [3, 3, 2, 3, 2, 3, 3, 2, 3, 3, 2, 2, 2, 2], 
                [2, 3, 3, 3, 2, 2, 2, 2, 2, 2, 3, 3, 3, 2], 
                [2, 4, 4, 4, 4, 3, 3, 3, 3, 2, 3, 1, 2, 4], 
                [2, 3, 2, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 2], 
                [2, 3, 3, 1, 4, 4, 4, 4, 4, 4, 2, 2, 3, 2], 
                [1, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 2], 
                [3, 3, 2, 3, 3, 3, 2, 3, 2, 4, 4, 4, 4, 4], 
                [4, 4, 4, 4, 4, 4, 4, 3, 4, 1, 3, 3, 3, 2], 
                [1, 3, 2 ,3, 3, 3, 3, 3, 1, 3, 3, 1, 4, 4]]
        
        map1 = [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 1, 2, 2, 3, 1, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2],
                [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2], 
                [2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2],
                [2, 2, 2, 2, 1, 2, 3, 2, 3, 2, 2, 3, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], 
                [2, 3, 2, 3, 2, 2, 2, 3, 2, 2, 2, 1, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2],
                [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [3, 2, 2, 2, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 1],
                [2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
                [2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]
        
        self.map_number += 1
        if self.map_number >= 3: self.map_number = 0
        if self.map_number == 0: return (map0, "The First One")
        if self.map_number == 1: return (map1, "One by one")
        if self.map_number == 2: return (map2, "The Maze")

App()


"""
        self.map_Time_is_the_key = [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 5],
                    [3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                    [2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 2],
                    [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2],
                    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2],
                    [3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2],
                    [2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 2],
                    [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2],
                    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2],
                    [3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2],
                    [1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 2],
                    [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2],
                    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2],
                    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2],
                    [1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 2],
                    [1, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2, 2]] """
