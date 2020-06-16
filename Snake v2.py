import pyglet
from pyglet.window import key
import random

move_time = 0.015  # should be in Menu() or Snake() later


def center_image(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


class Window(pyglet.window.Window):
    def __init__(self):
        super().__init__(1200, 800)
        self.set_caption("Snake v2")
        self.set_vsync(False)  # My snake wouldn't move fast enought without that
        self.set_mouse_visible(True)
        self.active_window = 1

        self.menu_on = False  # should be 'True' in the end so that I start with window
        self.menu = Menu()  # create a Menu instance
        self.play = Snake()  # create a Snake instance

        self.batch = pyglet.graphics.Batch()  # for main batch
        self.main_batch = []

    def on_draw(self):
        self.clear()
        if self.menu_on is True:  # if menu is on
            """ Maybe draw a menu batch """
            pass

        elif self.menu_on is False:  # if you start the game
            self.play.label.draw()  # score label
            grid.draw()  # grid
            self.batch.draw()  # main_batch

    def on_activate(self):  # just to pause the game if you click elsewhere
        if self.active_window == 0:
            self.active_window = 1
            self.play.label = pyglet.text.Label('{}'.format(self.play.food_count - 3), font_size=540, color=(255, 255, 255, 25))  # just reset the pause
            pyglet.clock.schedule_interval(self.play.move, move_time)

    def on_deactivate(self):  # just to pause the game if you click elsewhere
        self.active_window = 0
        self.play.label = pyglet.text.Label('PAUSE', font_size=265, color=(255, 255, 255, 25), x=0, y=268)  # just a pause
        pyglet.clock.unschedule(self.play.move)

    def on_key_press(self, symbol, modifiers):
        if self.play.game_state == 1:  # if you are in the game and alive
            if symbol == key.UP:
                self.play.new_step_direction = (0, 10)
            if symbol == key.DOWN:
                self.play.new_step_direction = (0, -10)
            if symbol == key.LEFT:
                self.play.new_step_direction = (-10, 0)
            if symbol == key.RIGHT:
                self.play.new_step_direction = (10, 0)

        elif self.play.game_state == 0:  # if you are in the game and dead
            if symbol == key.ENTER:
                self.play.reset()


class Menu:
    def __init__(self):
        """ There should be created and called menu """
        # window.set_mouse_visible(True)
        # window.play.game_state = -1


class Data:
    def __init__(self):
        """ This should save best scores and whatever else is needed """


class Snake:
    def __init__(self):
        """ There should be the game itself """
        self.food_count = 3
        self.growth = 0  # indication if the snake should grow
        self.snake_field = []  # snake Sprites live here
        self.food_position = (0, 0)

        self.circle_field = []  # coordinates of snake bodies live here
        self.circle_field.append((115, 475))  # this one is not drawn, but x+10 is

        self.block_coverage = 0  # to make sure snake doesn't change direction before it is in proper position
        self.new_step_direction = (10, 0)  # what is the new direction player gave TODO block size matters
        self.last_step_direction = (10, 0)  # where the snake moved last time TODO block size matters

        self.label = pyglet.text.Label('{}'.format(self.food_count-3), font_size=540, color=(255, 255, 255, 25))  # score label
        self.game_state = 1  # indication if you are alive or dead

        self.group_count = 0  # to set OrderGroups

    def start(self):

        for i in range(16):  # creates the starting snake TODO block size matters
            self.add_snake_body()

        self.spawn_food()
        pyglet.clock.schedule_interval(self.move, move_time)  # move with snake
        self.update_main_batch()
        window.set_mouse_visible(False)

    def add_snake_body(self):
        last_in_circle = self.circle_field[len(self.circle_field) - 1]  # take last coordinates of snake body
        self.circle_field.append((last_in_circle[0] + self.last_step_direction[0],
                                  last_in_circle[1] + self.last_step_direction[1]))  # append a new one acording to last_step_direction

        last_in_circle = self.circle_field[len(self.circle_field) - 1]  # take the new last coordinates
        self.snake_field.append(pyglet.sprite.Sprite(body, x=last_in_circle[0], y=last_in_circle[1], batch=window.batch,
                                                     group=self.group_count))  # add new snake_body to the snake_field

        self.group_count += 1  # HUGELY INEFFICIENT!
        """ According to docs you don't wanna have too many OrderGroups,
        but I need to hate it here in order to later design 'skins' for the snake 
        it makes the application hugely inefficient in a bit though... """

    def take_snake_body(self):  # pop the last snake body and coordinates
        self.circle_field.pop(0)
        self.snake_field.pop(0)

    def spawn_food(self):
        self.food_position = (25 + random.randint(0, 23) * 50, 25 + random.randint(0, 15) * 50)  # set a new random food position TODO window size matters

        try:  # check if it's valid
            self.circle_field.index(self.food_position)
            self.spawn_food()
        except ValueError:
            pass

    def update_main_batch(self):
        window.main_batch.clear()
        window.main_batch.append(pyglet.sprite.Sprite(food, x=self.food_position[0], y=self.food_position[1], batch=window.batch))
        # window.main_batch += self.snake_field

    def check_for_direction(self):  # check if the snake is in proper position to change it's direction
        if self.block_coverage == 0 and (self.last_step_direction != (-self.new_step_direction[0], -self.new_step_direction[1])):
            self.last_step_direction = self.new_step_direction
            self.block_coverage += 1

        elif self.block_coverage >= 4:
            self.block_coverage = 0

        else:
            self.block_coverage += 1

    def collision(self):  # checks for collisions with anything
        length_of_circle = len(self.circle_field) - 1
        last_in_circle = self.circle_field[length_of_circle]

        if not 0 < last_in_circle[0] < 1200:  # border collision check
            self.loss()
        if not 0 < last_in_circle[1] < 800:
            self.loss()

        try:  # bode collision check
            self.circle_field.index(last_in_circle, 0, length_of_circle-1)
            self.loss()
        except ValueError:
            pass

        if (self.food_position[0] - 35 < last_in_circle[0] < self.food_position[0] + 35) and \
                (self.food_position[1] - 35 < last_in_circle[1] < self.food_position[1] + 35):  # food collision check

            self.spawn_food()
            self.food_count += 1
            self.label = pyglet.text.Label('{}'.format(self.food_count-3), font_size=540, color=(255, 255, 255, 25))  # update label
            self.growth = 1
            pyglet.clock.schedule_once(self.stop_grow, move_time*5)  # start cutting it's tail again TODO block size matters

    def stop_grow(self, dt):
        self.growth = 0

    def move(self, dt):
        self.check_for_direction()
        self.add_snake_body()
        self.collision()
        if self.growth == 0:
            self.take_snake_body()

        self.update_main_batch()
        print(self.food_count, ":", pyglet.clock.get_fps())  # performance check

    def loss(self):  # what if you lose
        pyglet.clock.unschedule(self.move)
        self.game_state = 0
        window.set_mouse_visible(True)
        print("You died!")  # TODO make it appear on the screen

    def reset(self):  # restart the game
        self.__init__()
        pyglet.clock.unschedule(self.move)
        self.update_main_batch()
        self.start()  # TODO should head to Menu() later


if __name__ == '__main__':
    window = Window()

    """ This will be moved to Menu() later in order to provide in-menu changes to this """
    grid = pyglet.image.load('Sources/snake_grid.png')
    body = pyglet.image.load('Sources/snake_v2_body.png')
    food = pyglet.image.load('Sources/snake_food.png')
    lose_sign = pyglet.image.load('Sources/snake_lose.png')  # TODO not in place yet

    center_image(body), center_image(food), center_image(lose_sign)
    grid, lose_sign = pyglet.sprite.Sprite(grid, x=1, y=0), pyglet.sprite.Sprite(lose_sign)
    grid.opacity = 25


    Snake.start(window.play)  # TODO should be called from Menu() later

    pyglet.app.run()
