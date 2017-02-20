from math import sqrt
from random import randint
from Enemy import Enemy
from tkinter import mainloop
from World import world, ENEMIES, DELAY, FOOD, ENEMY_LIMIT
from Hero import Hero
from Animation import Animation
from Controls import Controls
from Camera import Camera
import time


def colliding(u1, u2):  # function for getting distance between units
    dist = sqrt((u1.x - u2.x)**2 + (u1.y - u2.y)**2)
    return dist <= u1.r + u2.r


def random_coords():  # random coordinates for units spawn
    x, y = randint(100, world['width']-100), randint(100, world['height']-100)
    return x, y


def ticks():  # frame action
    t = time.time()
    food_copy = food[:]
    projectiles_copy = projectiles[:]
    bad_units_copy = bad_units[:]

    '''animation'''
    animation.screen.delete('all')
    animation.check_border()
    animation.insight(food + projectiles + [hero] + bad_units)
    animation.print_enemy_counter()

    '''frame action for projectiles'''
    for shot in projectiles_copy:
        shot.tick()

    '''check units and projectiles collisions'''
    collide_checker = 1
    for unit_1 in bad_units_copy + food_copy:
        for unit_2 in (bad_units_copy + food_copy + projectiles_copy)[collide_checker:]:
            if abs(unit_1.x - unit_2.x) <= unit_1.vision_range >= abs(unit_1.y - unit_2.y):
                if unit_1.group == 'Enemy' and unit_2.group == 'Food':
                    if unit_1.level == 2:
                        unit_1.move_to(unit_2)
                if sqrt((unit_1.x - unit_2.x)**2 + (unit_1.y - unit_2.y)**2) < unit_1.r + unit_2.r:
                    unit_1.collide(unit_2)
                    unit_2.collide(unit_1)
        unit_1.tick()  # enemy frame action
        collide_checker += 1
        if abs(unit_1.x - hero.x) <= unit_1.r + hero.r >= abs(unit_1.y - hero.y):
            if sqrt((unit_1.x - hero.x)**2 + (unit_1.y - hero.y)**2) < unit_1.r + hero.r:
                unit_1.collide(hero)
                hero.collide(unit_1)

    t2 = int((time.time() - t) * 100)
    if Enemy.limit_counter == 0:
        animation.screen.delete('all')
        animation.victory()  # win screen
    elif Enemy.limit_counter <= ENEMY_LIMIT:
        animation.screen.after(DELAY - t2, ticks)  # repeat frame action after delay
    else:
        animation.screen.delete('all')
        animation.game_over()  # lose screen


good_units = []
bad_units = []
projectiles = []
food = []
bad_units.extend([Enemy(*random_coords(), bad_units, food, level=2) for x in range(ENEMIES)])  # spawn enemies
food.extend([Enemy(*random_coords(), food, level=1, group='Food') for y in range(FOOD)])  # spawn food

camera = Camera()
hero = Hero(camera)
animation = Animation(camera)
controls = Controls(camera, hero, animation.screen, projectiles)

ticks()

animation.screen.bind('<Key>', controls.key_pressed)
animation.screen.bind('<KeyRelease>', controls.key_release)
animation.screen.bind('<Button-1>', controls.click)

mainloop()
