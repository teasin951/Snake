import pyglet
from tkinter import *
from pyglet.window import key, mouse
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

        self.screen_function = ""

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
        options.show()

    def call_shop(self):
        self.screen_function = "Shop"
        shop.show()

    def call_stats(self):
        self.screen_function = "Stats"
        stats.show()

    def on_draw(self):
        self.clear()
        if self.screen_function == "Menu":
            blank.draw()
            menu_left.draw()
            menu_arrow1.draw()

            if menu.play_state:
                menu_difficulty.draw()
                menu_arrow2.draw()

        elif self.screen_function == "Snake":
            snake.label.draw()
            grid.draw()
            self.batch.draw()

            if self.active_window == 0:
                pause.draw()

            if snake.game_state == 0:
                death.draw()
                death_desc.draw()

        elif self.screen_function == "Options":
            pass

        elif self.screen_function == "Shop":
            pass

        elif self.screen_function == "Stats":
            pass

    def on_deactivate(self):  # just to pause the game if you click elsewhere
        if self.screen_function == "Snake" and snake.game_state == 1:
            self.active_window = 0
            pyglet.clock.unschedule(snake.move)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.screen_function == "Menu":
            menu.mouse_function(x, y, button)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.screen_function == "Menu":
            menu.mouse_function(x, y, button=None)

    def on_key_press(self, symbol, modifiers):
        if self.screen_function == "Snake":
            snake.keyboard_functions(symbol)

        elif self.screen_function == "Menu":
            menu.keyboard_function(symbol)


class Menu:  # TODO Menu()
    def __init__(self):
        """ There should be created and called menu """
        self.play_state = False
        self.highlighted_option = 0
        self.time = 0
        self.last_difficulty = -1

        # snake.game_state = -1

    def play(self):
        self.highlighted_option = 1
        menu_arrow2.position = (800, 500)
        pyglet.clock.schedule_interval(self.rotate1, 0.01)

        self.play_state = True

    def rotate1(self, dt):
        menu_arrow1.rotation += 10
        self.time += 1
        if self.time >= 6:
            pyglet.clock.unschedule(self.rotate1)

    def rotate2(self, dt):
        menu_arrow1.rotation -= 10
        self.time -= 1
        if self.time <= 0:
            pyglet.clock.unschedule(self.rotate2)

    def snake_time(self, difficulty):
        snake.difficulty = difficulty

        self.__init__()
        menu_arrow1.rotation = 180
        window.call_snake()

    def mouse_function(self, x, y, button):
        # """ if in menu and not clicked anything yet """
        if not self.play_state:
            if 0 < x < 356 and 360 < y < 440:
                menu_arrow1.position = (377, 405)
                self.highlighted_option = 0
                if button == mouse.LEFT:
                    self.play()

            elif 0 < x < 356 and 260 < y < 340:
                menu_arrow1.position = (377, 300)
                self.highlighted_option = 1
                if button == mouse.LEFT:
                    window.call_shop()

            elif 0 < x < 356 and 150 < y < 230:
                menu_arrow1.position = (377, 195)
                self.highlighted_option = 2
                if button == mouse.LEFT:
                    window.call_stats()

            elif 0 < x < 356 and 40 < y < 120:
                menu_arrow1.position = (377, 90)
                self.highlighted_option = 3
                if button == mouse.LEFT:
                    window.call_options()

        # """ if clicked on play """
        else:
            if 395 < x < 780 and 557 < y < 635:
                menu_arrow2.position = (800, 595)
                self.highlighted_option = 0
                if button == mouse.LEFT:
                    self.snake_time(0)

            elif 395 < x < 780 and 462 < y < 540:
                menu_arrow2.position = (800, 500)
                self.highlighted_option = 1
                if button == mouse.LEFT:
                    self.snake_time(1)

            elif 395 < x < 780 and 365 < y < 445:
                menu_arrow2.position = (800, 405)
                self.highlighted_option = 2
                if button == mouse.LEFT:
                    self.snake_time(2)

            elif 395 < x < 780 and 270 < y < 348:
                menu_arrow2.position = (800, 310)
                self.highlighted_option = 3
                if button == mouse.LEFT:
                    self.snake_time(3)

            # """ if clicked back on the left """
            if 0 < x < 356 and 0 < y < 440 and button == mouse.LEFT:
                pyglet.clock.schedule_interval(self.rotate2, 0.01)
                self.play_state = False
                self.highlighted_option = 0

    def keyboard_function(self, symbol):
        if not self.play_state:
            if symbol == key.ENTER:
                if self.highlighted_option == 0:
                    self.play()
                elif self.highlighted_option == 1:
                    window.call_shop()
                elif self.highlighted_option == 2:
                    window.call_stats()
                elif self.highlighted_option == 3:
                    window.call_options()

            elif symbol == key.UP:
                if self.highlighted_option > 0:
                    self.highlighted_option -= 1
                    menu_arrow1.y += 105

            elif symbol == key.DOWN:
                if self.highlighted_option < 3:
                    self.highlighted_option += 1
                    menu_arrow1.y -= 105

            elif symbol == key.SPACE and self.last_difficulty != -1:
                self.snake_time(self.last_difficulty)

            elif symbol == key.RIGHT:
                self.play()
        else:
            if symbol == key.ENTER:
                if self.highlighted_option == 0:
                    self.snake_time(0)
                elif self.highlighted_option == 1:
                    self.snake_time(1)
                elif self.highlighted_option == 2:
                    self.snake_time(2)
                elif self.highlighted_option == 3:
                    self.snake_time(3)

            if symbol == key.UP:
                if self.highlighted_option > 0:
                    self.highlighted_option -= 1
                    menu_arrow2.y += 95

            elif symbol == key.DOWN:
                if self.highlighted_option < 3:
                    self.highlighted_option += 1
                    menu_arrow2.y -= 95

            elif symbol == key.LEFT:
                pyglet.clock.schedule_interval(self.rotate2, 0.01)
                self.play_state = False
                self.highlighted_option = 0


class Shop:
    def __init__(self):
        pass

    def show(self):
        print("Shop")


class Stats:
    def __init__(self):
        self.data = Data()

    def show(self):
        print("Stats")


class Options:
    def __init__(self):
        pass

    def show(self):
        print("Options")


class Data:
    def __init__(self):
        """ This should save best scores and whatever else is needed """
        self.data = self.read_data()  # because I know where every data lays I will just look for it under an index

    def read_data(self):
        try:
            with open("common/statistics.dat", "r") as file:
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
        with open("common/statistics.dat", "a") as file:
            template = [
                        "{}\n".format(account_name),
                        "0\n", "0\n", "0\n", "0\n",
                        "0\n", "0\n", "0\n", "0\n",
                        "0\n", "0\n", "0\n", "0\n",
                        "0\n", "0\n", "0\n", "0\n",
                        "0\n",
                        "0\n", "0\n", "0\n", "0\n"
                        ]
            for i in template:
                file.write(i)

            return template

    def write_data_addition(self, position, new_value):
        self.data[position] = str(int(self.data[position].strip("\n")) + new_value) + "\n"

    def write_data_append(self, position, new_value):
        self.data[position] = self.data[position].strip("\n") + ", " + str(new_value) + "\n"

    def write_data_score(self, position, score):
        if int(self.data[position]) < score:
            self.data[position] = str(score) + "\n"

    def store_data(self):
        with open("common/statistics.dat", "w") as file:
            for i in self.data:
                file.write(i)


class Snake:
    def __init__(self):
        """ There should be the game itself """
        self.food_count = 3
        self.time_played = 0
        self.difficulty = 0  # this will be changed by Menu(); 0 - easy, 1 - normal, 2 - hard, 3 - impossible
        self.move_time = 0.02

        self.growth = 0  # indication if the snake should grow
        self.snake_field = []  # snake Sprites live here
        self.food_position = (0, 0)

        self.circle_field = []  # coordinates of snake bodies live here
        self.circle_field.append((115, 475))  # this one is not drawn, but x+10 is

        self.block_coverage = 0  # to make sure snake doesn't change direction before it is in proper position
        self.new_step_direction = (10, 0)  # what is the new direction player gave TODO block size matters
        self.last_step_direction = (10, 0)  # where the snake moved last time TODO block size matters

        self.label = pyglet.text.Label('{}'.format(self.food_count-3), font_size=540, color=(255, 255, 255, 25))  # score label
        self.game_state = -1  # indication if you are alive or dead
        self.time_in_fade = 0



    def start(self):
        for i in range(16):  # creates the starting snake TODO block size matters
            self.add_snake_body()

        self.game_state = 1
        self.move_time = 0.02 - (self.difficulty*5)/1000
        self.spawn_food()
        pyglet.clock.schedule_interval(self.move, self.move_time)  # move with snake
        self.update_main_batch()
        window.set_mouse_visible(False)

        death.opacity, death_desc.opacity = 0, 0  # just to reset death screen

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

        stats.data.write_data_score(1 + self.difficulty, self.food_count - 3)  # best score
        stats.data.write_data_addition(5 + self.difficulty, 1)  # games played
        stats.data.write_data_addition(9 + self.difficulty, self.food_count - 3)  # food eaten
        stats.data.write_data_addition(13 + self.difficulty, int(self.time_played))  # playtime
        # TODO in-game currency
        stats.data.store_data()

        window.set_mouse_visible(True)
        pyglet.clock.schedule_interval(self.fade_in, 1/85)

    def fade_in(self, dt):  # animation for death screen
        death.opacity += 1
        if self.time_in_fade >= 2.98:
            pyglet.clock.unschedule(self.fade_in)
            pyglet.clock.schedule_once(self.appear, 0.8)
        else:
            self.time_in_fade += 1/85

    @staticmethod
    def appear(dt):  # animation for death description
        death_desc.opacity = 255

    def reset(self, call_menu=True):  # restart the game
        menu.last_difficulty = self.difficulty
        pyglet.clock.unschedule(self.fade_in)  # if you reset and die before the animation ends, this takes care of it

        self.__init__()
        pyglet.clock.unschedule(self.move)
        self.update_main_batch()

        if call_menu:
            window.call_menu()
        else:
            self.difficulty = menu.last_difficulty
            self.start()

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
                window.set_mouse_visible(True)
                pyglet.clock.unschedule(snake.move)

            elif symbol == key.ESCAPE and window.active_window == 0:
                window.active_window = 1
                window.set_mouse_visible(False)

                if snake.game_state == 1:
                    pyglet.clock.schedule_interval(snake.move, snake.move_time)

        elif self.game_state == 0:  # if you are in the game and dead
            if symbol == key.SPACE:
                self.reset(call_menu=False)

            elif symbol == key.ENTER:
                self.reset()

            elif symbol == key.ESCAPE:
                self.reset()


if __name__ == '__main__':
    window = Window()
    menu = Menu()
    shop = Shop()
    stats = Stats()
    options = Options()
    snake = Snake()

    """ Snake things """
    body = pyglet.resource.image('textures/body/basic.png')
    food = pyglet.resource.image('textures/food/basic.png')
    grid = pyglet.resource.image('textures/interface/grid.png')
    pause = pyglet.resource.image('textures/interface/pause.png')
    lose_sign = pyglet.resource.image('textures/interface/lose_sign.png')

    center_image(body), center_image(food), center_image(lose_sign)
    grid, pause, lose_sign = pyglet.sprite.Sprite(grid, x=1, y=0), pyglet.sprite.Sprite(pause, x=0, y=0), pyglet.sprite.Sprite(lose_sign)
    grid.opacity = 25

    """ Menu things """
    blank = pyglet.resource.image('textures/interface/blank.png')
    menu_left = pyglet.resource.image('textures/interface/menu_left.png')
    menu_arrow = pyglet.resource.image('textures/interface/menu_arrow.png')
    menu_difficulty = pyglet.resource.image('textures/interface/menu_difficulty.png')
    death = pyglet.resource.image('textures/interface/death.png')
    death_desc = pyglet.resource.image('textures/interface/death_description.png')

    center_image(menu_arrow)
    blank = pyglet.sprite.Sprite(blank)
    menu_left = pyglet.sprite.Sprite(menu_left, x=0, y=0)
    menu_arrow1, menu_arrow2 = pyglet.sprite.Sprite(menu_arrow, x=377, y=405), pyglet.sprite.Sprite(menu_arrow, x=800, y=500)
    menu_difficulty = pyglet.sprite.Sprite(menu_difficulty, x=396, y=255)
    death = pyglet.sprite.Sprite(death)
    death_desc = pyglet.sprite.Sprite(death_desc)

    menu_arrow1.rotation, menu_arrow2.rotation = 180, 180

    """ Start things """
    window.call_menu()  # TODO should be called from Menu() later

    pyglet.app.run()
