import pyxel

class App:
    def __init__(self) -> None:
        
        self.currentState = "title_screen"

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
        pass
    def draw_title_screen(self): 
        pyxel.rect(0, 0, 16, 16, 3)
        pyxel.text(0, 16, "Yes", 3)

App()
