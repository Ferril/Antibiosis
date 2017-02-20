from Projectile import Projectile
from World import DELAY


class Controls:
    '''
    This class contains controls methods for 'w','a','s','d' keys:
    start motion for pressed keys and stop motion for released, -
    and function for shot on left button click.
    '''

    def __init__(self, camera, hero, screen, good_shots):
        self.keys = {'w': [0, self.up, self.stop_up],
                     's': [0, self.down, self.stop_down],
                     'a': [0, self.left, self.stop_left],
                     'd': [0, self.right, self.stop_right]}
        self.camera = camera
        self.hero = hero
        self.screen = screen
        self.projectiles = good_shots

    '''
    This methods called start-moving-function on press and stop-moving on release.
    '''
    def key_pressed(self, event):
        if event.char in self.keys:
            if not self.keys[event.char][0]:
                self.keys[event.char][0] = 1
                self.keys[event.char][1](event.char)

    def key_release(self, event):
        if event.char in self.keys:
            self.keys[event.char][0] = 0

    '''
    Motion methods.
    '''
    def up(self, char):
        if self.keys[char][0]:
            self.hero.moving['up'] = True
            self.hero.move_up()
            self.screen.after(DELAY, self.keys[char][1], char)
        else:
            self.keys[char][2](char)

    def down(self, char):
        if self.keys[char][0]:
            self.hero.moving['down'] = True
            self.hero.move_down()
            self.screen.after(DELAY, self.keys[char][1], char)
        else:
            self.keys[char][2](char)

    def left(self, char):
        if self.keys[char][0]:
            self.hero.moving['left'] = True
            self.hero.move_left()
            self.screen.after(DELAY, self.keys[char][1], char)
        else:
            self.keys[char][2](char)

    def right(self, char):
        if self.keys[char][0]:
            self.hero.moving['right'] = True
            self.hero.move_right()
            self.screen.after(DELAY, self.keys[char][1], char)
        else:
            self.keys[char][2](char)

    '''
    Stop motion methods.
    '''
    def stop_up(self, char):
        if not self.keys[char][0]:
            self.hero.moving['up'] = False
            if self.hero.speed['y_up'] < 0:
                self.hero.move_up()
                self.screen.after(DELAY, self.keys[char][2], char)

    def stop_down(self, char):
        if not self.keys[char][0]:
            self.hero.moving['down'] = False
            if self.hero.speed['y_down'] > 0:
                self.hero.move_down()
                self.screen.after(DELAY, self.keys[char][2], char)

    def stop_left(self, char):
        if not self.keys[char][0]:
            self.hero.moving['left'] = False
            if self.hero.speed['x_left'] < 0:
                self.hero.move_left()
                self.screen.after(DELAY, self.keys[char][2], char)

    def stop_right(self, char):
        if not self.keys[char][0]:
            self.hero.moving['right'] = False
            if self.hero.speed['x_right'] > 0:
                self.hero.move_right()
                self.screen.after(DELAY, self.keys[char][2], char)

    '''
    Calling Projectile on left-click event.
    '''
    def click(self, event):
        if not self.projectiles:
            self.projectiles.append(Projectile(self.hero.x, self.hero.y,
                                               event.x + self.camera.x, event.y + self.camera.y,
                                               'Projectile', self.projectiles))
