from Units import Unit
from World import start, world, HERO_MAX_SPEED, DIAG_SPEED_COEF


class Hero(Unit):
    '''
    This class contains playable unit's characteristics, it's motions and it's colliding action.
    '''
    def __init__(self, camera):
        Unit.__init__(self, x=start['x'], y=start['y'], r=start['hero_r'], colour='#23409E')
        self.counter = 0
        self.max_speed = HERO_MAX_SPEED
        self.moving = {'up': False,
                       'down': False,
                       'right': False,
                       'left': False}
        self.speed = {'y_up': 0,
                      'y_down': 0,
                      'x_right': 0,
                      'x_left': 0}
        self.camera = camera

    def move_up(self):
        if self.moving['up']:
            if self.speed['y_up'] - 1 >= -self.max_speed:
                self.speed['y_up'] -= 1
        else:
            if self.speed['y_up'] + 1 <= 0:
                self.speed['y_up'] += 1
            else:
                self.speed['y_up'] = 0
        if self.moving['left'] or self.moving['right']:
            self.speed['y_up'] *= DIAG_SPEED_COEF
        if self.y + self.speed['y_up'] <= world['y'] + self.r:
            self.y = world['y'] + self.r
        else:
            self.y += self.speed['y_up']
        self.camera.y = self.y - self.camera.h // 2

    def move_down(self):
        if self.moving['down']:
            if self.speed['y_down'] + 1 <= self.max_speed:
                self.speed['y_down'] += 1
        else:
            if self.speed['y_down'] - 1 >= 0:
                self.speed['y_down'] -= 1
            else:
                self.speed['y_down'] = 0
        if self.moving['left'] or self.moving['right']:
            self.speed['y_down'] *= DIAG_SPEED_COEF
        if self.y + self.speed['y_down'] >= world['height'] - self.r:
            self.y = world['height'] - self.r
        else:
            self.y += self.speed['y_down']
        self.camera.y = self.y - self.camera.h // 2

    def move_left(self):
        if self.moving['left']:
            if self.speed['x_left'] - 1 >= -self.max_speed:
                self.speed['x_left'] -= 1
        else:
            if self.speed['x_left'] + 1 <= 0:
                self.speed['x_left'] += 1
            else:
                self.speed['x_left'] = 0
        if self.moving['up'] or self.moving['down']:
            self.speed['x_left'] *= DIAG_SPEED_COEF
        if self.x + self.speed['x_left'] <= world['x'] + self.r:
            self.x = world['x'] + self.r
        else:
            self.x += self.speed['x_left']
        self.camera.x = self.x - self.camera.w // 2

    def move_right(self):
        if self.moving['right']:
            if self.speed['x_right'] + 1 <= self.max_speed:
                self.speed['x_right'] += 1
        else:
            if self.speed['x_right'] - 1 >= 0:
                self.speed['x_right'] -= 1
            else:
                self.speed['x_right'] = 0
        if self.moving['up'] or self.moving['down']:
            self.speed['x_right'] *= DIAG_SPEED_COEF
        if self.x + self.speed['x_right'] >= world['width'] - self.r:
            self.x = world['width'] - self.r
        else:
            self.x += self.speed['x_right']
        self.camera.x = self.x - self.camera.w // 2

    def collide(self, another_object):
        if another_object.group == 'Enemy':
            Unit.move_away(self, another_object)
            self.camera.x = self.x - self.camera.w//2
            self.camera.y = self.y - self.camera.h//2
