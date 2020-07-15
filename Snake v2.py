import pyglet
from tkinter import *
from pyglet.window import key
import random


def center_image(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


class Window(pyglet.window.Window):
    def __init__(self):
        super().__init__(1200, 800)
        self.set_caption("Snake v2")
        self.set_vsync(False)  # My snake wouldn't move fast enough without this
        self.set_mouse_visible(True)
        self.active_window = 1

        self.screen_function = ""  # TODO should be 'Menu' in the end so that I start with Menu

        self.batch = pyglet.graphics.Batch()  # for main batch
        self.main_batch = []

    """ These should be called to initiate a different window """
    def call_menu(self):  # TODO should be called after you die
        self.screen_function = "Menu"

    def call_snake(self):
        self.screen_function = "Snake"
        snake.start()

    def call_options(self):
        self.screen_function = "Options"

    def call_store(self):
        self.screen_function = "Store"


    def on_draw(self):
        self.clear()
        if self.screen_function == "Menu":
            pass

        elif self.screen_function == "AskForName":
            pass

        elif self.screen_function == "Snake":
            snake.label.draw()
            grid.draw()
            self.batch.draw()

        elif self.screen_function == "Options":
            pass

        elif self.screen_function == "Shop":
            pass

    # def on_activate(self):  # just to pause the game if you click elsewhere
    #     if self.active_window == 0 and self.screen_function == "Snake":
    #         self.active_window = 1
    #         snake.label = pyglet.text.Label('{}'.format(snake.food_count - 3), font_size=540, color=(255, 255, 255, 25))  # just reset the pause
    #
    #         print("on_activate activated")
    #         if snake.game_state == 1:
    #             pyglet.clock.schedule_interval(snake.move, snake.move_time)
    #
    # def on_deactivate(self):  # just to pause the game if you click elsewhere
    #     if self.screen_function == "Snake":
    #         self.active_window = 0
    #         snake.label = pyglet.text.Label('PAUSE', font_size=265, color=(255, 255, 255, 25), x=0, y=268)  # just a pause
    #         pyglet.clock.unschedule(snake.move)

    def on_key_press(self, symbol, modifiers):  # TODO more functions
        if self.screen_function == "Snake":
            snake.keyboard_functions(symbol=symbol)


class Menu:  # TODO Menu()
    def __init__(self):
        """ There should be created and called menu """
        self.data = Data()
        # print(self.data.data)
        # snake.game_state = -1
        # window.set_mouse_visible(True)


class Data:
    def __init__(self):
        """ This should save best scores and whatever else is needed """
        self.data = self.read_data()  # because I know where every data lays I will just look for it under an index

    def read_data(self):
        try:
            with open("common/dat.txt", "r") as file:
                return file.readlines()

        # if you start the snake for the first time
        except FileNotFoundError:
            return self.add_new_account(self.ask_for_name())


    """ This is a mess, but that's what tkinter does :) """
    def tkinter_shit(self, *args):
        self.return_your_name = self.e.get()
        self.root.destroy()

    def ask_for_name(self):
        self.root = Tk()
        self.root.geometry("350x120")

        lab = Label(self.root, text="", font=65)
        lab.pack()
        label = Label(self.root, text="Enter your name:", font=65)
        label.pack()
        self.e = Entry(self.root, width=30, font=65)
        self.e.pack()

        self.root.bind('<Return>', self.tkinter_shit)

        self.root.mainloop()
        return self.return_your_name
    """ The end of the tkinter mess, have a nice day :)  """


    @staticmethod
    def add_new_account(account_name):
        with open("common/dat.txt", "a") as file:
            template = ["account\n", "{}\n".format(account_name),
                        "easy\n", "0\n", "normal\n", "0\n", "hard\n", "0\n", "impossible\n", "0\n",
                        "playtime\n", "0\n", "games\n", "0\n" "snakies\n", "0\n",
                        "bodies\n", "0\n", "foods\n", "0\n", "backgrounds\n", "0\n"]
            for i in template:
                file.write(i)

            return template

    def store_data_addition(self, position, new_value):
        self.data[position] = str(int(self.data[position].strip("\n")) + new_value) + "\n"

        with open("common/dat.txt", "w") as file:
            for i in self.data:
                file.write(i)

    def store_data_append(self, position, new_value):
        self.data[position] = self.data[position].strip("\n") + ", " + str(new_value) + "\n"

        with open("common/dat.txt", "w") as file:
            for i in self.data:
                file.write(i)

    def store_data_score(self, difficulty, score):
        position = self.data.index(difficulty + "\n")

        if int(self.data[position+1].strip("\n")) < score:
            self.data[position+1] = str(score) + "\n"

            with open("common/dat.txt", "w") as file:
                for i in self.data:
                    file.write(i)


class Snake:
    def __init__(self):
        """ There should be the game itself """
        self.food_count = 3
        self.time_played = 0
        self.difficulty = "normal"  # this will be changed by Menu()
        self.move_time = 0.015  # this as well

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

    def start(self):
        for i in range(16):  # creates the starting snake TODO block size matters
            self.add_snake_body()

        self.spawn_food()
        pyglet.clock.schedule_interval(self.move, self.move_time)  # move with snake
        self.update_main_batch()
        window.set_mouse_visible(False)

    def add_snake_body(self):
        last_in_circle = self.circle_field[len(self.circle_field) - 1]  # take last coordinates of snake body
        self.circle_field.append((last_in_circle[0] + self.last_step_direction[0],
                                  last_in_circle[1] + self.last_step_direction[1]))  # append a new one acording to last_step_direction

        last_in_circle = self.circle_field[len(self.circle_field) - 1]  # take the new last coordinates
        self.snake_field.append(pyglet.sprite.Sprite(body, x=last_in_circle[0], y=last_in_circle[1], batch=window.batch))  # add new snake_body to the snake_field

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

        try:  # body collision check
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
            pyglet.clock.schedule_once(self.stop_grow, self.move_time*5)  # start cutting it's tail again TODO block size matters

    def stop_grow(self, dt):
        self.growth = 0

    def move(self, dt):
        self.check_for_direction()
        self.add_snake_body()
        self.collision()
        if self.growth == 0:
            self.take_snake_body()

        self.update_main_batch()
        self.time_played += self.move_time
        if pyglet.clock.get_fps() < 200:
            print(self.food_count - 3, ":", pyglet.clock.get_fps())  # performance check

    def loss(self):  # what if you lose
        pyglet.clock.unschedule(self.move)
        self.game_state = 0
        menu.data.store_data_addition(11, int(self.time_played))
        menu.data.store_data_addition(13, 1)
        menu.data.store_data_score(self.difficulty, self.food_count - 3)
        window.set_mouse_visible(True)
        print("You died!")  # TODO make it appear on the screen

    def reset(self):  # restart the game
        self.__init__()
        pyglet.clock.unschedule(self.move)
        self.update_main_batch()
        self.start()  # TODO should head to Menu() later


    def keyboard_functions(self, symbol):
        if self.game_state == 1:  # if you are in the game and alive
            if symbol == key.UP:
                self.new_step_direction = (0, 10)
            if symbol == key.DOWN:
                self.new_step_direction = (0, -10)
            if symbol == key.LEFT:
                self.new_step_direction = (-10, 0)
            if symbol == key.RIGHT:
                self.new_step_direction = (10, 0)

            if symbol == key.ESCAPE and window.active_window == 1:
                window.active_window = 0
                self.label = pyglet.text.Label('PAUSE', font_size=265, color=(255, 255, 255, 25), x=0, y=268)  # just a pause
                window.set_mouse_visible(True)
                pyglet.clock.unschedule(snake.move)

            elif symbol == key.ESCAPE and window.active_window == 0:
                window.active_window = 1
                self.label = pyglet.text.Label('{}'.format(snake.food_count - 3), font_size=540, color=(255, 255, 255, 25))  # just reset the pause
                window.set_mouse_visible(False)

                if snake.game_state == 1:
                    pyglet.clock.schedule_interval(snake.move, snake.move_time)

        elif self.game_state == 0:  # if you are in the game and dead
            if symbol == key.ENTER:
                self.reset()



if __name__ == '__main__':
    window = Window()
    menu = Menu()
    snake = Snake()

    """ This will be moved to Menu() later in order to provide in-menu changes to this """
    body = pyglet.resource.image('textures/body/basic.png')
    food = pyglet.resource.image('textures/food/basic.png')
    grid = pyglet.resource.image('textures/interface/grid.png')
    lose_sign = pyglet.resource.image('textures/interface/lose_sign.png')

    center_image(body), center_image(food), center_image(lose_sign)
    grid, lose_sign = pyglet.sprite.Sprite(grid, x=1, y=0), pyglet.sprite.Sprite(lose_sign)
    grid.opacity = 25

    window.call_snake()  # TODO should be called from Menu() later

    pyglet.app.run()
