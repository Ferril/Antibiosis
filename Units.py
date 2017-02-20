from World import world, SLAM_RATE


class Unit:
    def __init__(self, x, y, r=50, visual=True, colour='yellow'):
        self.x = x
        self.y = y
        self.r = r
        self.group = self.__class__.__name__
        self.visual = visual
        self.colour = colour
        self.fill = '#18212F'  # fill colour
        self.width = 8

    def move_away(self, another_object):
        if self.x > another_object.x and self.x + self.r + SLAM_RATE <= world['width']:
            self.x += SLAM_RATE
        elif self.x < another_object.x and self.x - self.r - SLAM_RATE >= world['x']:
            self.x -= SLAM_RATE
        if self.y > another_object.y and self.y + self.r + SLAM_RATE <= world['height']:
            self.y += SLAM_RATE
        elif self.y < another_object.y and self.y - self.r - SLAM_RATE >= world['y']:
            self.y -= SLAM_RATE
