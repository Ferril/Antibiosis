from Units import Unit
from World import world, SPAWN_TIME
from random import choice, randint


class Enemy(Unit):
    '''
    This class contains logic of a non-playable unit.
    '''

    limit_counter = 0  # enemies counter
    killed_enemies_counter = 0

    def __init__(self, x, y, listed, food=(), level=0, group='Enemy'):
        Unit.__init__(self, x, y, colour='#6d2f84')
        self.logic = {1: {'r': 14, 'max_speed': 4, 'vision_range': 0, 'health': 1, 'value': 0,
                          'colour': '#6d2f84', 'limit_counter': 0},
                      2: {'r': 32, 'max_speed': 5, 'vision_range': 60, 'health': 1, 'value': 2,
                          'colour': '#1B702F', 'limit_counter': 1},
                      3: {'r': 47, 'max_speed': 3, 'vision_range': 47, 'health': 2, 'value': 3,
                          'colour': '#a39b49', 'limit_counter': 1}}
        self.group = group
        self.level = level
        self.food = food
        self.r = self.logic[self.level]['r']
        self.max_speed = self.logic[self.level]['max_speed']
        self.vision_range = self.logic[self.level]['vision_range']
        self.health = self.logic[self.level]['health']
        self.colour = self.logic[self.level]['colour']
        self.value = self.logic[self.level]['value']
        self.exp = 0
        self.alive = True
        self.move_counter = 0
        self.hit_counter = 0
        self.spawn_counter = 0
        self.fertility = 3
        self.listed = listed
        self.move_y = choice([self.move_down, self.move_up])
        self.move_x = choice([self.move_left, self.move_right])
        self.speed = {'y': 0,
                      'x': 0}
        Enemy.limit_counter += self.logic[self.level]['limit_counter']
    '''
    Unit's transformation in other unit. Changes it's characteristics.
    '''
    def level_up(self):
        self.level += 1
        self.r = self.logic[self.level]['r']
        self.max_speed = self.logic[self.level]['max_speed']
        self.vision_range = self.logic[self.level]['vision_range']
        self.health = self.logic[self.level]['health']
        self.colour = self.logic[self.level]['colour']
        self.value = self.logic[self.level]['value']
        self.width = 7
        self.exp = 0
    '''
    Unit's transformation in other unit. Changes it's characteristics.
    '''
    def spawning_food(self):
        self.food.extend(Enemy(self.x, self.y, self.food, level=1, group='Food') for x in range(self.value))

    def spawning_enemies(self):
        self.listed.append(Enemy(self.x, self.y, self.listed, self.food, level=2))
    '''
    Colliding of unit with other objects.
    '''
    def collide(self, another_object):
        if another_object.group == 'Hero':
            self.move_away(another_object)
        elif another_object.group == 'Projectile':
            self.colour = 'white'
            self.health -= 1
            self.width = self.health * 2 + 1
            if self.health == 0:
                self.alive = False
                Enemy.killed_enemies_counter += 1
                self.spawning_food()
        else:
            if self.level == 2:
                if another_object.level == 1:
                    another_object.alive = False
                    self.exp += 1
                else:
                    self.move_away(another_object)
            else:
                self.move_away(another_object)
    '''
    One frame actions of units.
    '''
    def tick(self):
        if self.colour == 'white':
            self.hit_counter += 1
            if self.hit_counter > 15:
                self.hit_counter = 0
                self.colour = self.logic[self.level]['colour']
        self.move_counter += 1
        if self.level == 3:
            self.spawn_counter += 1
            if self.spawn_counter == SPAWN_TIME and self.fertility > 1:
                self.spawning_enemies()
                self.spawn_counter = 0
                self.fertility -= 1
            elif self.spawn_counter == SPAWN_TIME and self.fertility == 1:
                self.spawn_counter = 0
                self.colour = '#CE4906'
                self.logic[self.level]['colour'] = '#CE4906'
                self.fertility -= 1
            elif self.spawn_counter == SPAWN_TIME and self.fertility == 0:
                self.alive = False
                self.value = 6
                self.spawning_food()
        if self.move_counter > randint(1, 20):
            self.move_y = choice([self.move_down, self.move_up])
            self.move_x = choice([self.move_left, self.move_right])
            self.move_counter = 0
        else:
            self.move_y()
            self.move_x()
        if not self.alive:
            Enemy.limit_counter -= self.logic[self.level]['limit_counter']
            self.listed.remove(self)
        if self.exp >= 4 > self.level:
            self.level_up()
    '''
    Logic of unit's motions to or away other objects.
    '''
    def move_to(self, another_object):
        if self.level == 2:
            if self.x > another_object.x:
                self.move_left()
            elif self.x < another_object.x:
                self.move_right()
            if self.y > another_object.y:
                self.move_up()
            elif self.y < another_object.y:
                self.move_down()

    def move_away(self, another_object):
        if self.x > another_object.x and self.x + self.r + self.speed['x'] <= world['width']:
            self.move_x = self.move_right
            self.move_counter = 0
        elif self.x < another_object.x and self.x - self.r - self.speed['x'] >= world['x']:
            self.move_x = self.move_left
            self.move_counter = 0
        if self.y > another_object.y and self.y + self.r + self.speed['y'] <= world['height']:
            self.move_y = self.move_down
            self.move_counter = 0
        elif self.y < another_object.y and self.y - self.r - self.speed['y'] >= world['y']:
            self.move_y = self.move_up
            self.move_counter = 0
    '''
    Unit's motion methods.
    '''
    def move_up(self):
        if self.speed['y'] - 1 >= -self.max_speed:
            self.speed['y'] -= 1
        if self.y + self.speed['y'] <= world['y'] + self.r:
            self.y = world['y'] + self.r
        else:
            self.y += self.speed['y']

    def move_down(self):
        if self.speed['y'] + 1 <= self.max_speed:
            self.speed['y'] += 1
        if self.y + self.speed['y'] >= world['height'] - self.r:
            self.y = world['height'] - self.r
        else:
            self.y += self.speed['y']

    def move_left(self):
        if self.speed['x'] - 1 >= -self.max_speed:
            self.speed['x'] -= 1
        if self.x + self.speed['x'] <= world['x'] + self.r:
            self.x = world['x'] + self.r
        else:
            self.x += self.speed['x']

    def move_right(self):
        if self.speed['x'] + 1 <= self.max_speed:
            self.speed['x'] += 1
        if self.x + self.speed['x'] >= world['width'] - self.r:
            self.x = world['width'] - self.r
        else:
            self.x += self.speed['x']
