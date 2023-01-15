#!pgzrun
WIDTH = 800
HEIGHT = 600

class ship:
    x = 370
    y = 550
    @classmethod
    def update(cls):
        screen.draw.filled_circle( (cls.x, cls.y), 10, (128,128,128))

def update():
    if keyboard.left:
        ship.x = ship.x - 5
    if keyboard.right:
        ship.x = ship.x + 5

def draw():
    screen.fill((80,0,70))
    ship.update()


