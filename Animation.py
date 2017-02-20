from tkinter import *
from World import camera_size, world, ENEMY_LIMIT
from Enemy import Enemy


class Animation:
    '''
    This class displays graphical objects.
    '''
    def __init__(self, camera):
        self.camera = camera
        self.screen = Canvas(width=camera_size['width'], height=camera_size['height'], bg='black')
        self.screen.pack()
        self.screen.focus_set()
    '''
    Displays all units and projectiles.
    '''
    def draw(self, object):
        object.visual = self.screen.create_oval([object.x - object.r - self.camera.x,
                                                 object.y - object.r - self.camera.y],
                                                [object.x + object.r - self.camera.x,
                                                 object.y + object.r - self.camera.y],
                                                fill=object.fill, width=object.width, outline=object.colour)
    '''
    Displays of the game map borders.
    '''
    def draw_border_left(self):
        self.line = self.screen.create_line([world['x'] - self.camera.x, world['y'] - self.camera.y],
                                            [world['x'] - self.camera.x, world['height'] - self.camera.y],
                                            width=10, fill='#3d5b00')

    def draw_border_up(self):
        self.line = self.screen.create_line([world['x'] - self.camera.x, world['y'] - self.camera.y],
                                            [world['width'] - self.camera.x, world['y'] - self.camera.y],
                                            width=10, fill='#3d5b00')

    def draw_border_right(self):
        self.line = self.screen.create_line([world['width'] - self.camera.x, world['height'] - self.camera.y],
                                            [world['width'] - self.camera.x, world['y'] - self.camera.y],
                                            width=10, fill='#3d5b00')

    def draw_border_down(self):
        self.line = self.screen.create_line([world['width'] - self.camera.x, world['height'] - self.camera.y],
                                            [world['x'] - self.camera.x, world['height'] - self.camera.y],
                                            width=10, fill='#3d5b00')
    '''
    Checks the presence of the object in the camera's field of view.
    '''
    def insight(self, obj_list):
        for object in obj_list:
            if (object.x > self.camera.x - object.r and object.y > self.camera.y - object.r) and \
                    (object.x < self.camera.x + self.camera.w + object.r and
                             object.y < self.camera.y + self.camera.h + object.r):
                self.draw(object)
    '''
    Checks the presence of the game map borders in the camera's field of view
    '''
    def check_border(self):
        if world['y'] - self.camera.h // 2 <= self.camera.y:
            self.draw_border_left()
        if world['x'] - self.camera.w // 2 <= self.camera.x:
            self.draw_border_up()
        if world['width'] <= self.camera.x + self.camera.w:
            self.draw_border_right()
        if world['height'] <= self.camera.y + self.camera.h:
            self.draw_border_down()
    '''
    Interface counters.
    '''
    def print_enemy_counter(self):
        self.screen.create_text(40, 30, fill='gray', font='Times 30', anchor=NW,
                                text='Enemies: %s / %s' % (Enemy.limit_counter, ENEMY_LIMIT))
        self.screen.create_text(40, 75, fill='gray', font='Times 30', anchor=NW,
                                text='Killed: %s' % Enemy.killed_enemies_counter)
    '''
    Displays of the end game screens.
    '''
    def game_over(self):
        self.screen.create_text(450, 360, fill='red', font='Times 80', text='Game Over')
        self.screen.create_text(300, 420, fill='#A20E12', font='Times 30', anchor=NW,
                                text='Enemies killed: %s' % Enemy.killed_enemies_counter)

    def victory(self):
        self.screen.create_text(450, 360, fill='blue', font='Times 80', text='You Win!')
        self.screen.create_text(300, 420, fill='#170EA2', font='Times 30', anchor=NW,
                                text='Enemies killed: %s' % Enemy.killed_enemies_counter)
