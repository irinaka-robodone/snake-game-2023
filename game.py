import pyxel

class App:
    def __init__(self) -> None:
        self.widh = 160
        self.height= 160
        
        pyxel.init(self.width, self.height)
        pyxel.run(self.update,self.draw)
    
    def draw(selr):
        pass
    def drsw