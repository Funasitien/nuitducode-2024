import pyxel

class App:
    def __init__(self) -> None:
        
        self.currentState = ""

        pyxel.init(128, 128, title="NDC")
        pyxel.run(self.update, self.draw)

    def update(self): getattr(self, f"update_{self.currentState}")
    def draw(self): getattr(self, f"draw_{self.currentState}")

    def update_(self): pass
    def draw_(self): pass

App()
