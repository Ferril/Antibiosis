from Units import Unit
from World import world, PROJ_BORD_COEF


class Projectile(Unit):
    '''
    This class contains logic of projectile.
    '''
    def __init__(self, x, y, target_x, target_y, group, listed, speed=13, shooting_range=300):
        Unit.__init__(self, x, y, r=7, colour='red')
        self.speed = speed
        self.shooting_range = shooting_range
        self.target_x = target_x
        self.target_y = target_y
        self.step = self.shooting_range/self.speed
        self.proj_calc(target_x, target_y)
        self.group = group
        self.listed = listed
    '''
    Calculates projectile's trajectory.
    '''
    def proj_calc(self, target_x, target_y):
        slip_x = abs(target_x - self.x)
        slip_y = abs(target_y - self.y)
        self.breaker = 1
        self.side = True
        self.check_shot = True
        if slip_x > slip_y:
            self.breaker = slip_y / slip_x
            self.side = True
        elif slip_x < slip_y:
            self.breaker = slip_x / slip_y
            self.side = False
        elif slip_x == 0 and slip_y == 0:
            self.check_shot = False
        if target_x > self.x:
            self.speed_x = self.speed
        elif target_x < self.x:
            self.speed_x = -self.speed
        else:
            self.speed_x = 0
        if target_y > self.y:
            self.speed_y = self.speed
        elif target_y < self.y:
            self.speed_y = -self.speed
        else:
            self.speed_y = 0
        self.tick()
    '''
    One frame actions of projectile.
    '''
    def tick(self):
        if self.x + self.r + PROJ_BORD_COEF >= world['width'] \
                or self.x - self.r - PROJ_BORD_COEF <= world['x'] \
                or self.y + self.r + PROJ_BORD_COEF >= world['height'] \
                or self.y - self.r - PROJ_BORD_COEF <= world['y']:
            self.step = 0
        if self.step <= 0:
            self.listed.remove(self)
        if self.step and self.check_shot:
            if self.side:
                self.x += self.speed_x
                self.y += self.speed_y * self.breaker
            else:
                self.y += self.speed_y
                self.x += self.speed_x * self.breaker
            self.step -= 1
    '''
    Logic of colliding with other objects.
    '''
    def collide(self, another_unit):
        if another_unit.group == 'Enemy':
            self.step = 0
            try:
                self.listed.remove(self)
            except ValueError:
                pass
