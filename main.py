import time
import pyglet
from tkinter import messagebox, Tk, Label, Entry
from pyglet.window import key, mouse
from cryptography.fernet import Fernet
import numpy as np
import random
import json

import Create_Json
import animate_snake


def alert(title, message, kind='warning'):
    if kind not in ('error', 'warning', 'info'):
        raise ValueError('Unsupported alert kind.')

    show_method = getattr(messagebox, 'show{}'.format(kind))
    show_method(title, message)


def yes_no(title, message):
    show_method = getattr(messagebox, 'askquestion')
    return show_method(title, message)


def center_image(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


def outline_label(text, x, y, outline_distance, text_font, font_size, text_color, outline_color, batch):
    textArray = np.zeros(10, dtype='object')
    index = 0

    main = pyglet.graphics.OrderedGroup(1)
    outlining = pyglet.graphics.OrderedGroup(0)

    for i in range(-1, 2):
        for j in range(-1, 2):
            textArray[index] = pyglet.text.Label(text=text, x=x + i * outline_distance, y=y + j * outline_distance,
                                                 font_name=text_font, font_size=font_size,
                                                 color=outline_color, batch=batch, group=outlining,
                                                 anchor_x='center', anchor_y='center')
            index += 1

    textArray[index] = pyglet.text.Label(text=text, x=x, y=y, font_name=text_font,
                                         font_size=font_size, color=text_color, batch=batch, group=main,
                                         anchor_x='center', anchor_y='center')

    return textArray


def outline_label_right(text, x, y, outline_distance, text_font, font_size, text_color, outline_color, batch):
    textArray = np.zeros(10, dtype='object')
    index = 0

    main = pyglet.graphics.OrderedGroup(1)
    outlining = pyglet.graphics.OrderedGroup(0)

    for i in range(-1, 2):
        for j in range(-1, 2):
            textArray[index] = pyglet.text.Label(text=text, x=x + i * outline_distance, y=y + j * outline_distance,
                                                 font_name=text_font, font_size=font_size,
                                                 color=outline_color, batch=batch, group=outlining,
                                                 anchor_x='right', anchor_y='center')
            index += 1

    textArray[index] = pyglet.text.Label(text=text, x=x, y=y, font_name=text_font,
                                         font_size=font_size, color=text_color, batch=batch, group=main,
                                         anchor_x='right', anchor_y='center')

    return textArray


class Window(pyglet.window.Window):
    def __init__(self):
        super().__init__(1200, 800)
        self.set_caption("Snake v2")
        self.set_vsync(False)
        self.set_mouse_visible(True)
        self.active_window = 1

        self.screen_function = ""
        self.sound = True

        self.batch = pyglet.graphics.Batch()  # for main batch
        self.main_batch = []

    def update(self, dt):
        pass

    """ These should be called to initiate a different window """

    def call_menu(self):
        shop.background.prepare_movement(-200, -200)
        pyglet.clock.schedule_interval(shop.background.move, shop.background.call_time)
        self.screen_function = "Menu"

    def call_snake(self):
        shop.background.amount = -0.0085
        shop.background.prepare_movement(-150, 0)
        pyglet.clock.schedule_interval(shop.background.move, shop.background.call_time)
        pyglet.clock.schedule_interval(shop.background.scale, shop.background.call_time)
        self.screen_function = "Snake"

        snake.start()

    def call_options(self):
        shop.background.prepare_movement(-300, -100)
        pyglet.clock.schedule_interval(shop.background.move, shop.background.call_time)
        self.screen_function = "Options"

    def call_shop(self):
        shop.background.prepare_movement(-50, -250)
        shop.refresh()
        pyglet.clock.schedule_interval(shop.background.move, shop.background.call_time)
        self.screen_function = "Shop"
        shop.update()

    def call_stats(self):
        shop.background.prepare_movement(-350, -220)
        pyglet.clock.schedule_interval(shop.background.move, shop.background.call_time)
        self.screen_function = "Stats"
        stats.show()

    def on_draw(self):
        self.clear()
        shop.background.object.draw()
        if self.screen_function == "Menu":
            menu_left.draw()
            menu_arrow_1.object.draw()

            if menu.play_state:
                menu_difficulty.draw()
                menu_arrow2.draw()

            if menu.play_state and stats.data.data['relative_mode']:
                cross_relative.draw()

        elif self.screen_function == "Snake":
            snake.label.draw()
            grid.draw()
            snake.food_for_draw.draw()
            self.batch.draw()
            pyglet.text.Label("{}".format(stats.calculate_snakies(delte=True)),
                              font_name="Calisto MT", font_size=12, x=600, y=16, anchor_x='center').draw()

            if self.active_window == 0:
                pause.draw()

            if snake.game_state == 0:
                death.object.draw()
                death_desc.object.draw()

        elif self.screen_function == "Options":
            options.optionsBatch.draw()
            options.labelBatch.draw()

        elif self.screen_function == "Shop":
            shop.highlights[shop.selection_position].draw()

            if shop.display_body:
                animate_snake.batch.draw()
            else:
                shop.food_for_draw.draw()

            shop.background_icons[shop.draw_background_index].draw()
            shop.shopBatch.draw()
            for i in shop.out_label_batch:
                for j in i:
                    j.draw()

        elif self.screen_function == "Stats":
            stats.statsBatch.draw()

    def on_deactivate(self):  # just to pause the game if you click elsewhere
        if self.screen_function == "Snake" and snake.game_state == 1:
            snake.pause()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.screen_function == "Menu":
            menu.mouse_function(x, y, button)

        elif self.screen_function == "Shop":
            shop.mouse_function(x, y, button)

        elif self.screen_function == "Stats":
            stats.mouse_function(x, y, button)

        elif self.screen_function == "Options":
            options.mouse_function(x, y, button)

        elif self.screen_function == "Snake" and self.active_window == 0:
            snake.mouse_function(x, y, button)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.screen_function == "Options" and (260 - options.scroll_value < y < 640 - options.scroll_value or
                                                  -100 - options.scroll_value < y < 240 - options.scroll_value):
            if button == mouse.LEFT:
                options.redraw_labels()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.screen_function == "Menu":
            menu.mouse_function(x, y, button=None)

        elif self.screen_function == "Options":
            options.mouse_function(x, y, button=None)

        elif self.screen_function == "Shop":
            shop.mouse_function(x, y, button=None)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self.screen_function == "Options":
            options.scroll(scroll_y)

        if self.screen_function == "Stats":
            stats.scroll(scroll_y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.screen_function == "Options":
            options.drag(x, y, dx, buttons)

    def on_key_press(self, symbol, modifiers):
        if self.screen_function == "Snake":
            snake.keyboard_functions(symbol)

        elif self.screen_function == "Menu":
            menu.keyboard_function(symbol)

        elif self.screen_function == "Options":
            options.keyboard_function(symbol)

        elif self.screen_function == "Shop":
            shop.keyboard_function(symbol)

        elif self.screen_function == "Stats":
            stats.keyboard_function(symbol)

    def on_key_release(self, symbol, modifiers):
        if self.screen_function == "Stats":
            stats.button_release()

        if self.screen_function == "Options":
            pyglet.clock.unschedule(options.move_knob_by_keyboard)
            pyglet.clock.unschedule(options.knob_set_delay)

    def on_close(self):
        window.close()
        if self.screen_function == "Options":
            options.leave_options()

        media.player.delete()
        effect.player.delete()


class Menu:
    def __init__(self):
        """ There should be created and called menu """
        self.play_state = False  # if play button was pressed
        self.highlighted_option = 0
        self.time = 0
        self.last_difficulty = -1
        self.last_highlighted_option = 0

        # snake.game_state = -1

    def play(self):
        self.highlighted_option = 1
        menu_arrow2.position = (800, 500)
        menu_arrow_1.prepare_animation(amount=10)
        pyglet.clock.schedule_interval(menu_arrow_1.rotate, menu_arrow_1.call_time)

        self.play_state = True

    def snake_time(self, difficulty):
        snake.difficulty = difficulty

        self.__init__()
        menu_arrow_1.object.rotation = 180
        window.call_snake()

    def make_a_sound(self):
        if self.highlighted_option != self.last_highlighted_option:
            effect.play(effect.choose)
        self.last_highlighted_option = self.highlighted_option

    def mouse_function(self, x, y, button):
        if not self.play_state:
            if 0 < x < 356 and 365 < y < 445:
                menu_arrow_1.object.position = (377, 405)
                self.highlighted_option = 0
                self.make_a_sound()
                if button == mouse.LEFT:
                    self.play()
                    effect.play(effect.enter)

            elif 0 < x < 356 and 260 < y < 340:
                menu_arrow_1.object.position = (377, 300)
                self.highlighted_option = 1
                self.make_a_sound()
                if button == mouse.LEFT:
                    window.call_shop()
                    effect.play(effect.enter)

            elif 0 < x < 356 and 155 < y < 235:
                menu_arrow_1.object.position = (377, 195)
                self.highlighted_option = 2
                self.make_a_sound()
                if button == mouse.LEFT:
                    window.call_stats()
                    effect.play(effect.enter)

            elif 0 < x < 356 and 50 < y < 130:
                menu_arrow_1.object.position = (377, 90)
                self.highlighted_option = 3
                self.make_a_sound()
                if button == mouse.LEFT:
                    window.call_options()
                    effect.play(effect.enter)

        # """ if clicked on play """
        else:
            if 395 < x < 780 and 557 < y < 635:
                menu_arrow2.position = (800, 595)
                self.highlighted_option = 0
                self.make_a_sound()
                if button == mouse.LEFT:
                    self.snake_time(0)
                    effect.play(effect.enter)

            elif 395 < x < 780 and 462 < y < 540:
                menu_arrow2.position = (800, 500)
                self.highlighted_option = 1
                self.make_a_sound()
                if button == mouse.LEFT:
                    self.snake_time(1)
                    effect.play(effect.enter)

            elif 395 < x < 780 and 365 < y < 445:
                menu_arrow2.position = (800, 405)
                self.highlighted_option = 2
                self.make_a_sound()
                if button == mouse.LEFT:
                    self.snake_time(2)
                    effect.play(effect.enter)

            elif 395 < x < 780 and 270 < y < 348:
                menu_arrow2.position = (800, 310)
                self.highlighted_option = 3
                self.make_a_sound()
                if button == mouse.LEFT:
                    self.snake_time(3)
                    effect.play(effect.enter)

            elif 395 < x < 780 and 175 < y < 253:
                menu_arrow2.position = (800, 215)
                self.highlighted_option = 4
                self.make_a_sound()
                if button == mouse.LEFT:
                    stats.data.data['relative_mode'] = not stats.data.data['relative_mode']
                    stats.data.store_data()
                    effect.play(effect.enter)

            # """ if clicked back on the left """
            if 0 < x < 356 and 0 < y < 440 and button == mouse.LEFT:
                menu_arrow_1.prepare_animation(amount=-10)
                pyglet.clock.schedule_interval(menu_arrow_1.rotate, menu_arrow_1.call_time)
                self.play_state = False
                self.highlighted_option = 0
                self.last_highlighted_option = 0

                effect.play(effect.enter)

    def keyboard_function(self, symbol):
        if not self.play_state:
            if symbol == key.ENTER or symbol == key.RIGHT:
                effect.play(effect.enter)

                if self.highlighted_option == 0:
                    self.play()
                elif self.highlighted_option == 1:
                    window.call_shop()
                elif self.highlighted_option == 2:
                    window.call_stats()
                elif self.highlighted_option == 3:
                    window.call_options()

            elif symbol == key.UP:
                effect.play(effect.choose)

                if self.highlighted_option > 0:
                    self.highlighted_option -= 1
                    menu_arrow_1.object.y += 105

            elif symbol == key.DOWN:
                effect.play(effect.choose)

                if self.highlighted_option < 3:
                    self.highlighted_option += 1
                    menu_arrow_1.object.y -= 105

            elif symbol == key.SPACE and self.last_difficulty != -1:
                menu_arrow_1.object.position = (377, 405)
                self.highlighted_option = 0
                self.snake_time(self.last_difficulty)

            elif symbol == key.RIGHT:
                if self.highlighted_option == 0:
                    effect.play(effect.enter)

                    self.play()

            elif symbol == key.ESCAPE:
                window.close()

        else:
            if symbol == key.ENTER or symbol == key.RIGHT:
                effect.play(effect.enter)

                if self.highlighted_option == 0:
                    self.snake_time(0)
                elif self.highlighted_option == 1:
                    self.snake_time(1)
                elif self.highlighted_option == 2:
                    self.snake_time(2)
                elif self.highlighted_option == 3:
                    self.snake_time(3)
                elif self.highlighted_option == 4:
                    stats.data.data['relative_mode'] = not stats.data.data['relative_mode']
                    stats.data.store_data()

            if symbol == key.UP:
                effect.play(effect.choose)

                if self.highlighted_option > 0:
                    self.highlighted_option -= 1
                    menu_arrow2.y += 95

            elif symbol == key.DOWN:
                effect.play(effect.choose)

                if self.highlighted_option < 4:
                    self.highlighted_option += 1
                    menu_arrow2.y -= 95

            elif symbol == key.LEFT or symbol == key.NUM_0:
                effect.play(effect.enter)

                menu_arrow_1.prepare_animation(amount=-10)
                pyglet.clock.schedule_interval(menu_arrow_1.rotate, menu_arrow_1.call_time)
                self.play_state = False
                self.highlighted_option = 0
                self.last_highlighted_option = 0

            elif symbol == key.ESCAPE:
                effect.play(effect.enter)

                menu_arrow_1.prepare_animation(amount=-10)
                pyglet.clock.schedule_interval(menu_arrow_1.rotate, menu_arrow_1.call_time)
                self.play_state = False
                self.highlighted_option = 0
                self.last_highlighted_option = 0


class Shop:
    def __init__(self):
        self.json = self.load_shopsheet()

        self.last_click = 0

        self.shopBatch = pyglet.graphics.Batch()
        self.out_label_batch = []
        self.shopBatchField = []

        self.selection_position = 0  # position of cursor
        self.highlights = [pyglet.sprite.Sprite(pyglet.resource.image('textures/interface/Skins-highlight.png')),
                           pyglet.sprite.Sprite(pyglet.resource.image('textures/interface/Background-highlight.png')),
                           pyglet.sprite.Sprite(pyglet.resource.image('textures/interface/Audio-highlight.png'))]

        self.equipped = pyglet.resource.image('textures/interface/highlight.png')
        self.equipped_audio = pyglet.resource.image('textures/interface/highlightAudio.png')

        self.tick = pyglet.resource.image('textures/interface/tick.png')

        self.draw_skin_index = 0  # where are we in the skins section
        self.draw_background_index = 0
        self.draw_music_index = 0
        self.display_body = True

        self.background_icons = []
        self.audio_labels = []

        self.load_icons()

        self.interface = self.create_shop_object("textures/interface/Shop.png")
        self.snakiesLabel = None

        self.body = pyglet.resource.image('textures/body/{}.png'.format(stats.data.data['body_in_use']))
        center_image(self.body)

        self.food = pyglet.resource.image('textures/food/{}.png'.format
                                          (stats.data.data['food_in_use']))
        center_image(self.food)
        self.food_for_draw = pyglet.sprite.Sprite(self.food, x=546, y=490)
        self.scale_food = 0.5
        self.food_for_draw.scale = self.scale_food

        self.background = Animation('textures/background/{}.jpg'.format
                                    (stats.data.data['background_in_use']),
                                    -200, -200, call_time=0.01, duration=0.3, center=False)

    def display_new_skin(self):
        new_skin = list(self.json['skins'])[self.draw_skin_index]
        if new_skin[0] == 'B':  # if we are supposed to draw snake
            self.display_body = True
            animate_snake.switch('textures/body/{}.png'.format(new_skin))

        else:
            self.display_body = False
            self.food_for_draw = pyglet.sprite.Sprite(
                pyglet.resource.image('textures/food/{}.png'.format(new_skin)), x=546, y=490)
            self.food_for_draw.scale = self.scale_food

    def move_skins_left(self):
        if self.draw_skin_index > 0:
            self.draw_skin_index -= 1
            self.display_new_skin()

            self.update()

    def move_skins_right(self):
        if self.draw_skin_index < len(list(self.json['skins'])) - 1:
            self.draw_skin_index += 1
            self.display_new_skin()

            self.update()

    def move_background_left(self):
        if self.draw_background_index > 0:
            self.draw_background_index -= 1
            self.update()

    def move_background_right(self):
        if self.draw_background_index < len(self.background_icons) - 1:
            self.draw_background_index += 1
            self.update()

    def move_audio_left(self):
        if self.draw_music_index > 0:
            self.draw_music_index -= 1
            self.update()

    def move_audio_right(self):
        if self.draw_music_index < len(list(self.json['music'])) - 1:
            self.draw_music_index += 1
            self.update()

    def display_tick(self, pos_index, code_name):
        """ Display ownership of a given item """
        order = pyglet.graphics.OrderedGroup(1)
        if pos_index == 0:
            tick = pyglet.sprite.Sprite(self.tick, x=670, y=460, batch=self.shopBatch, group=order)
            tick.scale = 0.1
        elif pos_index == 1:
            tick = pyglet.sprite.Sprite(self.tick, x=700, y=175, batch=self.shopBatch, group=order)
            tick.scale = 0.12
        else:
            tick = pyglet.sprite.Sprite(self.tick, x=760, y=15, batch=self.shopBatch, group=order)
            tick.scale = 0.1

            self.out_label_batch.append(outline_label("{}".format(self.json["music"][code_name]["branding"]),
                                                      x=610, y=68,
                                                      text_font="Copperplate Gothic Bold", font_size=26,
                                                      outline_color=(255, 255, 255, 255), text_color=(0, 0, 0, 255),
                                                      outline_distance=1, batch=None))  # display music without price

        self.shopBatchField.append(tick)

    def display_price(self, pos_index, code_name):
        """ Display price for current item """
        if pos_index == 0:
            self.out_label_batch.append(outline_label(str(self.json['skins'][code_name]), x=600, y=460,
                                                      text_font="Copperplate Gothic Bold", font_size=26,
                                                      outline_color=(255, 255, 255, 255), text_color=(0, 0, 0, 255),
                                                      outline_distance=1, batch=None))

        elif pos_index == 1:
            self.out_label_batch.append(outline_label(str(self.json['background'][code_name]), x=600, y=210,
                                                      text_font="Copperplate Gothic Bold", font_size=26,
                                                      outline_color=(255, 255, 255, 255), text_color=(0, 0, 0, 255),
                                                      outline_distance=1, batch=None))

        elif pos_index == 2:
            self.out_label_batch.append(outline_label("{} - {}".format(self.json["music"][code_name]["branding"],
                                                                       self.json['music'][code_name]['price']),
                                                      x=610, y=68,
                                                      text_font="Copperplate Gothic Bold", font_size=26,
                                                      outline_color=(255, 255, 255, 255), text_color=(0, 0, 0, 255),
                                                      outline_distance=1, batch=None))

    def display_highlight(self, pos_index):
        """ Highlighting current shop group """
        if pos_index == 0:
            high = pyglet.sprite.Sprite(self.equipped, x=450, y=450, batch=self.shopBatch)
            high.scale = 0.28
            self.shopBatchField.append(high)

        elif pos_index == 1:
            high = pyglet.sprite.Sprite(self.equipped, x=452, y=182, batch=self.shopBatch)
            high.scale = 0.302
            self.shopBatchField.append(high)

        elif pos_index == 2:
            high = pyglet.sprite.Sprite(self.equipped_audio, x=335, y=40, batch=self.shopBatch)
            high.scale = 0.55
            high.scale_y = 0.55
            self.shopBatchField.append(high)

    def update(self):
        """ update shop with current info """
        self.shopBatchField = []  # clear what is shown
        self.out_label_batch = []
        self.refresh()

        skin_code = list(self.json["skins"])[self.draw_skin_index]
        bckg_code = list(self.json["background"])[self.draw_background_index]
        audio_code = list(self.json["music"])[self.draw_music_index]

        body_data = stats.data.data['bodies']
        food_data = stats.data.data['foods']
        bckg_data = stats.data.data['backgrounds']
        audio_data = stats.data.data['soundtracks']

        ebody_data = stats.data.data['body_in_use']
        efood_data = stats.data.data['food_in_use']
        ebckg_data = stats.data.data['background_in_use']
        eaudio_data = stats.data.data['soundtrack_in_use']

        try:
            body_data.index(skin_code)
            self.display_tick(0, skin_code)

        except ValueError:
            try:
                food_data.index(skin_code)
                self.display_tick(0, skin_code)

            except ValueError:
                self.display_price(0, skin_code)

        try:
            bckg_data.index(bckg_code)
            self.display_tick(1, bckg_code)

        except ValueError:
            self.display_price(1, bckg_code)

        try:
            audio_data.index(audio_code)
            self.display_tick(2, audio_code)

        except ValueError:
            self.display_price(2, audio_code)

        try:
            ebody_data.index(skin_code)
            self.display_highlight(0)

        except ValueError:
            try:
                efood_data.index(skin_code)
                self.display_highlight(0)

            except ValueError:
                pass

        try:
            ebckg_data.index(bckg_code)
            self.display_highlight(1)

        except ValueError:
            pass

        try:
            eaudio_data.index(audio_code)
            self.display_highlight(2)

        except ValueError:
            pass

    def confirm(self):
        """ Seek confirmation from user """
        result = yes_no('Buy skin', 'Do you want to buy this skin?')
        window.activate()

        if result == 'yes':
            return True
        else:
            return False

    def buy_item(self):
        """ buy or equip selected item """
        skin_code = list(self.json["skins"])[self.draw_skin_index]
        bckg_code = list(self.json["background"])[self.draw_background_index]
        audio_code = list(self.json["music"])[self.draw_music_index]

        body_data = stats.data.data['bodies']
        food_data = stats.data.data['foods']
        bckg_data = stats.data.data['backgrounds']
        audio_data = stats.data.data['soundtracks']

        if self.selection_position == 0:
            try:  # equip body
                body_data.index(skin_code)
                stats.data.data['body_in_use'] = skin_code
                stats.data.store_data()
                self.body = pyglet.resource.image('textures/body/{}.png'.format
                                                  (stats.data.data['body_in_use']))
                center_image(self.body)

            except ValueError:
                try:  # equip food
                    food_data.index(skin_code)
                    stats.data.data['food_in_use'] = skin_code
                    stats.data.store_data()
                    self.food = pyglet.resource.image('textures/food/{}.png'.format
                                                      (stats.data.data['food_in_use']))
                    center_image(self.food)

                except ValueError:  # if we do not own the skin
                    price = self.json['skins'][skin_code]  # load price
                    if skin_code[0] == 'B':  # if it's a body skin
                        if price < stats.data.data['snakies']:  # if we can afford it
                            if self.confirm():  # ask again if the user wants to buy the item
                                stats.data.data['snakies'] -= price
                                stats.data.data['bodies'].append(skin_code)
                                stats.data.store_data()

                    elif skin_code[0] == 'F':
                        if price < stats.data.data['snakies']:  # if we can afford it
                            if self.confirm():  # ask again if the user wants to buy the item
                                stats.data.data['snakies'] -= price
                                stats.data.data['foods'].append(skin_code)
                                stats.data.store_data()

        elif self.selection_position == 1:
            try:  # equip background
                bckg_data.index(bckg_code)
                stats.data.data['background_in_use'] = bckg_code
                stats.data.store_data()
                self.background = Animation('textures/background/{}.jpg'.format
                                            (stats.data.data['background_in_use']),
                                            -200, -200, call_time=0.01, duration=0.3, center=False)
                shop.background.prepare_movement(-50, -250)
                pyglet.clock.schedule_interval(shop.background.move, shop.background.call_time)

            except ValueError:  # buy background
                price = self.json['background'][bckg_code]  # load price
                if price < stats.data.data['snakies']:  # if we can afford it
                    if self.confirm():  # ask again if the user wants to buy the item
                        stats.data.data['snakies'] -= price
                        stats.data.data['backgrounds'].append(bckg_code)
                        stats.data.store_data()

        elif self.selection_position == 2:
            try:  # equip audio
                audio_data.index(audio_code)
                stats.data.data['soundtrack_in_use'] = audio_code
                stats.data.store_data()

                media.MenuM = pyglet.resource.media('resources/music/{} M.wav'.format
                                                    (stats.data.data['soundtrack_in_use']))
                media.GameM = pyglet.resource.media('resources/music/{} G.wav'.format
                                                    (stats.data.data['soundtrack_in_use']))
                media.DeathM = pyglet.resource.media('resources/music/{} D.wav'.format
                                                     (stats.data.data['soundtrack_in_use']))
                media.play()

            except ValueError:  # buy audio
                price = self.json['music'][audio_code]['price']  # load price
                if price < stats.data.data['snakies']:  # if we can afford it
                    if self.confirm():  # ask again if the user wants to buy the item
                        stats.data.data['snakies'] -= price
                        stats.data.data['soundtracks'].append(audio_code)
                        stats.data.store_data()

        self.update()

    def load_icons(self):
        """

        Load all background icons mentioned in shopsheet.json into self.background_icons, and load snake

        """

        animate_snake.create('textures/body/BBS.png', 500, 500)
        pyglet.clock.schedule_interval(animate_snake.move, 1/30)

        for obj in list(self.json["background"]):
            bckg = pyglet.sprite.Sprite(pyglet.resource.image('textures/background/{}.jpg'.format(obj)),
                                        x=460, y=190)
            bckg.scale = 0.15
            self.background_icons.append(bckg)

    @staticmethod
    def load_shopsheet():
        """ Load info from json """
        with open("resources/shopsheet.json", 'rb') as jFile:
            encrypted = jFile.read()

        fernet = Fernet(stats.data.key)
        decrypted = fernet.decrypt(encrypted).decode()
        return json.loads(decrypted)

    def check_price(self, tag):
        """ Look up price of a given tag """
        if "B" == tag[0] or "F" == tag[0]:
            return self.json["skins"][tag]

        elif "I" == tag[0]:
            return self.json["background"][tag]

        elif "S" == tag[0]:
            return self.json["music"][tag]["price"]

    def refresh(self):
        """ refresh snakies label """
        self.out_label_batch.append(outline_label("Snakies: {}".format(stats.data.data['snakies']),
                                                  x=1000, y=760, text_font="Copperplate Gothic Bold", font_size=26,
                                                  outline_color=(255, 255, 255, 255), text_color=(0, 0, 0, 255),
                                                  outline_distance=1, batch=None))

    def create_shop_object(self, path, x=0, y=0):
        """ simplifying sprite creating """
        return pyglet.sprite.Sprite(pyglet.resource.image(path),
                                    x=x, y=y,
                                    batch=self.shopBatch)

    def doubleclick(self):
        """ Handling double-clicking """
        if self.last_click + 0.2 > time.perf_counter():
            return True

        else:
            self.last_click = time.perf_counter()
            return False

    def mouse_function(self, x, y, button):
        """ Handling mouse input for shop """
        if button == mouse.LEFT:
            if 25 < x < 195 and 735 < y < 780:  # clicking back button
                window.call_menu()
                effect.play(effect.enter)

            elif 440 < x < 770 and 450 < y < 650:  # double-clicking items
                if self.doubleclick():
                    self.buy_item()

            elif 440 < x < 770 and 150 < y < 370:
                if self.doubleclick():
                    self.buy_item()

            elif 400 < x < 850 and 0 < y < 110:
                if self.doubleclick():
                    self.buy_item()

            elif 0 < x < 260 and 450 < y < 650:  # clicking on arrows
                self.move_skins_left()
                effect.play(effect.choose)

            elif 940 < x < 1200 and 450 < y < 650:
                self.move_skins_right()
                effect.play(effect.choose)

            elif 0 < x < 260 and 150 < y < 370:
                self.move_background_left()
                effect.play(effect.choose)

            elif 940 < x < 1200 and 150 < y < 370:
                self.move_background_right()
                effect.play(effect.choose)

            elif 0 < x < 260 and 0 < y < 110:
                self.move_audio_left()
                effect.play(effect.choose)

            elif 940 < x < 1200 and 0 < y < 110:
                self.move_audio_right()
                effect.play(effect.choose)

        elif button is None:  # hovering over sections
            if 410 < y < 660:
                self.selection_position = 0

            if 160 < y < 410:
                self.selection_position = 1

            if 0 < y < 160:
                self.selection_position = 2

    def keyboard_function(self, symbol):
        """ Handling keyboard input for shop """
        if symbol == key.ESCAPE or symbol == key.NUM_0:
            window.call_menu()
            effect.play(effect.enter)
        elif symbol == key.DOWN and self.selection_position < 2:
            self.selection_position += 1
            effect.play(effect.choose)

        elif symbol == key.UP and self.selection_position > 0:
            self.selection_position -= 1
            effect.play(effect.choose)

        elif symbol == key.LEFT:
            if self.selection_position == 0:
                self.move_skins_left()

            elif self.selection_position == 1:
                self.move_background_left()

            elif self.selection_position == 2:
                self.move_audio_left()

            effect.play(effect.choose)

        elif symbol == key.RIGHT:
            if self.selection_position == 0:
                self.move_skins_right()

            elif self.selection_position == 1:
                self.move_background_right()

            elif self.selection_position == 2:
                self.move_audio_right()

            effect.play(effect.choose)

        elif symbol == key.ENTER or symbol == key.NUM_ENTER:
            self.buy_item()
            effect.play(effect.enter)


class Stats:
    def __init__(self):
        self.data = Data()

        self.statsBatch = pyglet.graphics.Batch()
        self.statsBatchField = []

        self.scroll_amount = 0
        self.scroll_value = 0

        self.memory = 0
        self.time_of_capcure = 0

    def show(self):
        self.statsBatch = pyglet.graphics.Batch()
        self.statsBatchField.clear()
        self.statsBatchField.append(self.create_stats_object("textures/interface/Stats.png",
                                                             y=-500 - self.scroll_value))
        self.draw_values()

    def security_check(self, dt):
        all_snakies = self.data.data['easy_snakies'] + self.data.data['normal_snakies'] + \
                      self.data.data['hard_snakies'] + self.data.data['impossible_snakies']
        all_item_prices = 0

        for i in range(4):
            for j in self.data.data[self.data.indexed_data[22 + i]]:
                all_item_prices += shop.check_price(j)
        if self.data.data['snakies'] != all_snakies - all_item_prices:
            alert('Data corrupted', 'How dare you alter the data of this game!')
            window.activate()

    def create_stats_object(self, path, x=0, y=0):
        return pyglet.sprite.Sprite(pyglet.resource.image(path),
                                    x=x, y=y,
                                    batch=self.statsBatch)

    def create_value(self, text, x, y, batch):
        value = outline_label_right("{}".format(text),
                                    x=x, y=y, text_font="Copperplate Gothic Bold", font_size=26,
                                    outline_color=(255, 255, 255, 255), text_color=(0, 0, 0, 255),
                                    outline_distance=1, batch=batch)

        self.statsBatchField.extend(value)

    def draw_values(self):
        o_y = 602
        all_snakies = self.data.data['easy_snakies'] + self.data.data['normal_snakies'] + \
                      self.data.data['hard_snakies'] + self.data.data['impossible_snakies']

        for i in range(4):
            best = self.data.data[self.data.indexed_data[1 + i]]
            games = self.data.data[self.data.indexed_data[5 + i]]
            food = self.data.data[self.data.indexed_data[9 + i]]
            playtime = self.data.data[self.data.indexed_data[13 + i]]
            snakies_count = self.data.data[self.data.indexed_data[17 + i]]

            self.create_value(best, 600, o_y - 287 * i - self.scroll_value, self.statsBatch)
            self.create_value(games, 600, o_y - 51 - 287 * i - self.scroll_value, self.statsBatch)
            self.create_value(food, 600, o_y - 51 * 2 - 287 * i - self.scroll_value, self.statsBatch)
            self.create_value(self.create_time(playtime), 600, o_y - 51 * 3 - 287 * i - self.scroll_value,
                              self.statsBatch)

            """ avg. score, avg. playtime, avg time / food, income percentage """
            if games != 0:
                self.create_value(round(food / games, 1),
                                  1160, o_y - 287 * i - self.scroll_value, self.statsBatch)
                self.create_value(self.create_time(playtime / games),
                                  1160, o_y - 51 - 287 * i - self.scroll_value, self.statsBatch)
            else:
                self.create_value(0,
                                  1160, o_y - 287 * i - self.scroll_value, self.statsBatch)
                self.create_value(self.create_time(0),
                                  1160, o_y - 51 - 287 * i - self.scroll_value, self.statsBatch)

            if food != 0:
                self.create_value("{} s".format(round(playtime / food, 1)),
                                  1160, o_y - 51 * 2 - 287 * i - self.scroll_value, self.statsBatch)
            else:
                self.create_value("0 s",
                                  1160, o_y - 51 * 2 - 287 * i - self.scroll_value, self.statsBatch)

            if all_snakies != 0:
                self.create_value("{} %".format(round((snakies_count / all_snakies) * 100, 1)),
                                  1160, o_y - 51 * 3 - 287 * i - self.scroll_value, self.statsBatch)
            else:
                self.create_value("0 %", 1160, o_y - 51 * 3 - 287 * i - self.scroll_value, self.statsBatch)

    def calculate_snakies(self, delte=False):
        if snake.difficulty == 0:
            multiplier = 1
            power = 1.35
        elif snake.difficulty == 2:
            multiplier = 1.5
            power = 1.4
        elif snake.difficulty == 3:
            multiplier = 2
            power = 1.8
        else:
            multiplier = 1.5
            power = 1.35

        snakies = (((snake.food_count - 3) ** power - snake.time_played) * multiplier)

        if snakies < 0:
            snakies = 0

        if delte:  # developer thingy, function will be static after deleting this
            if self.memory != snake.food_count:
                self.time_of_capcure = snake.time_played
                self.memory = snake.food_count

            return "{}    {}    {}".format(round(snakies, 2),

                                           round(((snake.food_count - 2) ** power -
                                                  (snake.food_count - 3) ** power -
                                                  snake.time_played + self.time_of_capcure) * multiplier, 2),

                                           round(((snake.food_count - 2) ** power -
                                                  (snake.food_count - 3) ** power) * multiplier, 2))
            # current snakies, snakies earning, next food value

        else:
            return int(snakies)

    @staticmethod
    def create_time(value):
        data_sec = int(value)
        hour = int(data_sec / 3600)
        mints = int(data_sec / 60) - hour * 60
        sec = data_sec - mints * 60 - hour * 3600

        if mints < 10:
            mints = "0{}".format(mints)
        if sec < 10:
            sec = "0{}".format(sec)

        return "{}:{}:{}".format(hour, mints, sec)

    def mouse_function(self, x, y, button):
        if button == mouse.LEFT:
            if 25 < x < 195 and 735 - self.scroll_value < y < 780 - self.scroll_value:
                window.call_menu()
                effect.play(effect.enter)

    def scroll(self, scroll):
        self.scroll_amount = scroll * 70
        if -501 < self.statsBatchField[0].y - self.scroll_amount < 0:
            for i in self.statsBatchField:
                i.y -= self.scroll_amount

            self.scroll_value += self.scroll_amount

    def keyboard_function(self, symbol):
        if symbol == key.ESCAPE or symbol == key.LEFT or symbol == key.NUM_0:
            window.call_menu()
            effect.play(effect.enter)

        if symbol == key.DOWN:
            self.button_scroll(0, -1)  # move it down
            effect.play(effect.choose)  # make a sound
            pyglet.clock.schedule_once(self.schedule, 0.3, direction=-1)  # after how long is holding triggered

        if symbol == key.UP:
            self.button_scroll(0, 1)  # move it up
            effect.play(effect.choose)  # make a sound
            pyglet.clock.schedule_once(self.schedule, 0.3, direction=1)  # after how long is holding triggered

    def button_release(self):  # button released, cancel every hold function
        pyglet.clock.unschedule(self.button_scroll)
        pyglet.clock.unschedule(self.schedule)

    def schedule(self, dt, direction):
        # effect.play(effect.enter)
        pyglet.clock.schedule_interval(self.button_scroll, 0.05, direction=direction)  # speed of scroll

    def button_scroll(self, dt, direction):
        self.scroll_amount = 70 * direction
        if -501 < self.statsBatchField[0].y - self.scroll_amount < 0:
            for i in self.statsBatchField:
                i.y -= self.scroll_amount

            self.scroll_value += self.scroll_amount


class Options:
    def __init__(self):
        self.optionsField = []
        self.optionsBatch = pyglet.graphics.Batch()
        self.labelField = []
        self.labelBatch = pyglet.graphics.Batch()
        self.backgroundGroup = pyglet.graphics.OrderedGroup(0)
        self.foregroundGroup = pyglet.graphics.OrderedGroup(1)

        self.scroll_value = 0
        self.position = 0

        """ The code NEEDS the first five objects to be in this order """
        self.create_options_object("textures/interface/Options.png", y=-1000,
                                   batch=self.optionsBatch, group=self.backgroundGroup)
        self.create_options_object("textures/interface/Options_knob.png",
                                   x=self.set_knob(stats.data.data['master_in_use']), y=562, center=True,
                                   batch=self.optionsBatch, group=self.foregroundGroup)
        self.create_options_object("textures/interface/Options_knob.png",
                                   x=self.set_knob(stats.data.data['music_in_use']), y=476, center=True,
                                   batch=self.optionsBatch, group=self.foregroundGroup)
        self.create_options_object("textures/interface/Options_knob.png",
                                   x=self.set_knob(stats.data.data['effects_in_use']), y=386, center=True,
                                   batch=self.optionsBatch, group=self.foregroundGroup)
        self.create_options_object("textures/interface/Options_knob.png",
                                   x=self.set_knob(stats.data.data['grid_opacity']), y=193, center=True,
                                   batch=self.optionsBatch, group=self.foregroundGroup)
        self.create_options_object("textures/interface/Options_knob.png",
                                   x=self.set_knob(stats.data.data['score_opacity']), y=106, center=True,
                                   batch=self.optionsBatch, group=self.foregroundGroup)

        self.create_options_object("textures/interface/Options_grid.png", y=-1000,
                                   batch=self.optionsBatch, group=self.backgroundGroup)
        self.create_options_object("textures/interface/Options_score.png", y=-1000,
                                   batch=self.optionsBatch, group=self.backgroundGroup)
        self.create_options_object("textures/interface/menu_arrow.png", x=90, y=562,
                                   batch=self.optionsBatch, group=self.foregroundGroup, center=True)

        self.draw_knob_values()
        self.optionsField[6].opacity = round(self.calculate_knob(3) * 255 / 100)
        self.optionsField[7].opacity = round(self.calculate_knob(4) * 255 / 100)

    def create_options_object(self, path, batch, group, x=0, y=0, center=False):
        if not center:
            self.optionsField.append(pyglet.sprite.Sprite(pyglet.resource.image(path),
                                                          x=x, y=y, batch=batch, group=group))
        else:
            image = pyglet.resource.image(path)
            center_image(image)
            self.optionsField.append(pyglet.sprite.Sprite(image, x=x, y=y, batch=batch, group=group))

    def create_knob_value(self, x, y, knob_number, batch):
        value = outline_label("{} %".format(self.calculate_knob(knob_number)),
                              x=x, y=y, text_font="Copperplate Gothic Bold", font_size=26,
                              outline_color=(255, 255, 255, 255), text_color=(0, 0, 0, 255),
                              outline_distance=1, batch=batch)

        self.labelField.extend(value)

    def redraw_labels(self):
        self.labelBatch = pyglet.graphics.Batch()
        self.labelField.clear()
        self.draw_knob_values()

        self.optionsField[6].opacity = round(self.calculate_knob(3) * 255 / 100)
        grid.opacity = round(self.calculate_knob(3) * 255 / 100)
        self.optionsField[7].opacity = round(self.calculate_knob(4) * 255 / 100)
        snake.label.color = (255, 255, 255, round(self.calculate_knob(4) * 255 / 100))

        media.adjust_music_volume()
        media.adjust_music_volume()
        effect.adjust()

    def draw_knob_values(self):
        self.create_knob_value(1080, 564 - self.scroll_value, 0, batch=self.labelBatch)
        self.create_knob_value(1080, 478 - self.scroll_value, 1, batch=self.labelBatch)
        self.create_knob_value(1080, 390 - self.scroll_value, 2, batch=self.labelBatch)
        self.create_knob_value(1080, 196 - self.scroll_value, 3, batch=self.labelBatch)
        self.create_knob_value(1080, 110 - self.scroll_value, 4, batch=self.labelBatch)

    @staticmethod
    def set_knob(value):
        return round(int(value) * 6.3 + 368)

    def calculate_knob(self, knob_number):
        return round((self.optionsField[1 + knob_number].x - 368) // 6.3)

    def leave_options(self):
        window.call_menu()
        self.update_and_store_data()

    def update_and_store_data(self):
        for i in range(5):
            set = {0: 'master_in_use', 1: 'music_in_use', 2: 'effects_in_use', 3: 'grid_opacity', 4: 'score_opacity'}
            stats.data.data[set.get(i)] = self.calculate_knob(i)
        stats.data.store_data()

    def mouse_function(self, x, y, button):
        if button == mouse.LEFT:
            if 25 < x < 195 and 735 - self.scroll_value < y < 780 - self.scroll_value:
                if snake.game_state == -1:
                    window.screen_function = "Snake"
                    media.adjust(0.01)
                    snake.game_state = 1
                    self.update_and_store_data()

                else:
                    self.leave_options()
                    effect.play(effect.enter)

            # click the first knob
            elif 370 < x < 1000 and 547 - self.scroll_value < y < 578 - self.scroll_value:
                self.optionsField[1].x = x

            # click the second knob
            elif 370 < x < 1000 and 460 - self.scroll_value < y < 493 - self.scroll_value:
                self.optionsField[2].x = x

            # click the third knob
            elif 370 < x < 1000 and 370 - self.scroll_value < y < 403 - self.scroll_value:
                self.optionsField[3].x = x

            # click the fourth knob
            elif 370 < x < 1000 and 176 - self.scroll_value < y < 208 - self.scroll_value:
                self.optionsField[4].x = x

            # click the fifth knob
            elif 370 < x < 1000 and 90 - self.scroll_value < y < 122 - self.scroll_value:
                self.optionsField[5].x = x

        if button is None:
            # hover over the first knob
            if 100 < x < 1100 and 520 - self.scroll_value < y < 605 - self.scroll_value:
                self.position = 0
                self.optionsField[8].y = 562 - self.scroll_value

            # hover over the second knob
            elif 100 < x < 1100 and 432 - self.scroll_value < y < 520 - self.scroll_value:
                self.position = 1
                self.optionsField[8].y = 476 - self.scroll_value

            # hover over the third knob
            elif 100 < x < 1100 and 343 - self.scroll_value < y < 432 - self.scroll_value:
                self.position = 2
                self.optionsField[8].y = 386 - self.scroll_value

            # hover over the fourth knob
            elif 100 < x < 1100 and 149 - self.scroll_value < y < 235 - self.scroll_value:
                self.position = 3
                self.optionsField[8].y = 193 - self.scroll_value

            # hover over the fifth knob
            elif 100 < x < 1100 and 63 - self.scroll_value < y < 149 - self.scroll_value:
                self.position = 4
                self.optionsField[8].y = 106 - self.scroll_value

    def drag(self, x, y, dx, button):
        if button == mouse.LEFT:
            # drag the first knob
            if 370 < x < 1000 and 547 - self.scroll_value < y < 578 - self.scroll_value and self.position == 0:
                if 370 < self.optionsField[1].x + dx < 1000:
                    self.optionsField[1].x = x

            # drag the second knob
            elif 370 < x < 1000 and 460 - self.scroll_value < y < 493 - self.scroll_value and self.position == 1:
                if 370 < self.optionsField[2].x + dx < 1000:
                    self.optionsField[2].x = x

            # drag the third knob
            elif 370 < x < 1000 and 370 - self.scroll_value < y < 403 - self.scroll_value and self.position == 2:
                if 370 < self.optionsField[3].x + dx < 1000:
                    self.optionsField[3].x = x

            # drag the fourth knob
            elif 370 < x < 1000 and 176 - self.scroll_value < y < 208 - self.scroll_value and self.position == 3:
                if 370 < self.optionsField[4].x + dx < 1000:
                    self.optionsField[4].x = x

            # drag the fifth knob
            elif 370 < x < 1000 and 90 - self.scroll_value < y < 122 - self.scroll_value and self.position == 4:
                if 370 < self.optionsField[5].x + dx < 1000:
                    self.optionsField[5].x = x

    def scroll(self, scroll):
        scroll_amount = scroll * 80
        if -1001 < self.optionsField[0].y - scroll_amount < 0:
            for i in self.optionsField:
                i.y -= scroll_amount
            for i in self.labelField:
                i.y -= scroll_amount

            self.scroll_value += scroll_amount

    def set_scroll(self, scroll_value):
        scroll_amount = self.scroll_value - scroll_value

        for i in self.optionsField:
            i.y += scroll_amount
        for i in self.labelField:
            i.y += scroll_amount

        self.scroll_value -= scroll_amount

    def move_knob_by_keyboard(self, dt, knob_number, movement_value, max_value):  # to move with a knob
        if 367 < self.optionsField[knob_number].x + movement_value < 999:
            self.optionsField[knob_number].x += movement_value
        else:
            self.optionsField[knob_number].x = max_value
        self.redraw_labels()

    def keyboard_function(self, symbol):
        if symbol == key.ESCAPE or symbol == key.NUM_0:
            if snake.game_state == -1:
                window.screen_function = "Snake"
                media.adjust(0.01)
                snake.game_state = 1
                self.update_and_store_data()

            else:
                self.leave_options()
                effect.play(effect.enter)

        if symbol == key.UP:
            if self.position == 1:
                self.position = 0
                self.optionsField[8].y = 562 - self.scroll_value

            elif self.position == 2:
                self.position = 1
                self.optionsField[8].y = 476 - self.scroll_value

            elif self.position == 3:
                self.set_scroll(0)  # scroll to the top
                self.position = 2
                self.optionsField[8].y = 386 - self.scroll_value

            elif self.position == 4:
                self.position = 3
                self.optionsField[8].y = 193 - self.scroll_value

            elif self.position == 5:  # if you are scrolled down to binding
                self.set_scroll(-480)
                self.position = 4
                self.optionsField[8].y = 106 - self.scroll_value

            effect.play(effect.choose)

        if symbol == key.DOWN:
            if self.position == 0:
                self.position = 1
                self.optionsField[8].y = 476 - self.scroll_value

            elif self.position == 1:
                self.position = 2
                self.optionsField[8].y = 386 - self.scroll_value

            elif self.position == 2:
                self.set_scroll(-480)
                self.position = 3
                self.optionsField[8].y = 193 - self.scroll_value

            elif self.position == 3:
                self.position = 4
                self.optionsField[8].y = 106 - self.scroll_value

            elif self.position == 4:
                self.set_scroll(-960)
                self.position = 5

            effect.play(effect.choose)

        delay = 0.3
        if symbol == key.RIGHT:
            if self.position == 0:
                self.move_knob_by_keyboard(0, 1, 31.5, 998)
                pyglet.clock.schedule_once(self.knob_set_delay, delay,
                                           knob_number=1, movement_value=31.5, max_value=998)

            if self.position == 1:
                self.move_knob_by_keyboard(0, 2, 31.5, 998)
                pyglet.clock.schedule_once(self.knob_set_delay, delay,
                                           knob_number=2, movement_value=31.5, max_value=998)

            if self.position == 2:
                self.move_knob_by_keyboard(0, 3, 31.5, 998)
                pyglet.clock.schedule_once(self.knob_set_delay, delay,
                                           knob_number=3, movement_value=31.5, max_value=998)

            if self.position == 3:
                self.move_knob_by_keyboard(0, 4, 6.3, 998)
                pyglet.clock.schedule_once(self.knob_set_delay, delay,
                                           knob_number=4, movement_value=6.3, max_value=998)

            if self.position == 4:
                self.move_knob_by_keyboard(0, 5, 6.3, 998)
                pyglet.clock.schedule_once(self.knob_set_delay, delay,
                                           knob_number=5, movement_value=6.3, max_value=998)

        if symbol == key.LEFT:
            if self.position == 0:
                self.move_knob_by_keyboard(0, 1, -31.5, 368)
                pyglet.clock.schedule_once(self.knob_set_delay, delay,
                                           knob_number=1, movement_value=-31.5, max_value=368)

            if self.position == 1:
                self.move_knob_by_keyboard(0, 2, -31.5, 368)
                pyglet.clock.schedule_once(self.knob_set_delay, delay,
                                           knob_number=2, movement_value=-31.5, max_value=368)

            if self.position == 2:
                self.move_knob_by_keyboard(0, 3, -31.5, 368)
                pyglet.clock.schedule_once(self.knob_set_delay, delay,
                                           knob_number=3, movement_value=-31.5, max_value=368)

            if self.position == 3:
                self.move_knob_by_keyboard(0, 4, -6.3, 368)
                pyglet.clock.schedule_once(self.knob_set_delay, delay,
                                           knob_number=4, movement_value=-6.3, max_value=368)

            if self.position == 4:
                self.move_knob_by_keyboard(0, 5, -6.3, 368)
                pyglet.clock.schedule_once(self.knob_set_delay, delay,
                                           knob_number=5, movement_value=-6.3, max_value=368)

    def knob_set_delay(self, dt, knob_number, movement_value, max_value):  # for making delay before calling move
        pyglet.clock.schedule_interval(self.move_knob_by_keyboard, 0.05,
                                       knob_number=knob_number, movement_value=movement_value, max_value=max_value)  #


class Data:
    def __init__(self):
        """ This should save best scores and whatever else is needed """
        self.key = 'tNXSr3w1v29_cBJhhN16BXNh_nVu7pmtD61KYnfmwK4='

        self.data = self.read_data()  # because I know where every data lays I will just look for it under an index
        self.indexed_data = list(self.data)

    def read_data(self):
        try:
            with open("common/statistics.json", "rb") as jFile:
                en_file = jFile.read()

            fernet = Fernet(self.key)
            decrypted = fernet.decrypt(en_file).decode()
            return json.loads(decrypted)

        # if you start the snake for the first time
        except FileNotFoundError:
            self.add_new_account(self.ask_for_name())
            window.activate()
            return self.read_data()

    def store_data(self):
        fernet = Fernet(self.key)
        original = json.dumps(self.data)
        encrypted = fernet.encrypt(bytes(original, 'utf-8'))

        with open("common/statistics.json", "wb") as file:
            file.write(encrypted)

    """ This is a mess, but that's what tkinter does :) """  # TODO tidy this up

    def tkinter_shit(self, *args):
        self.return_your_name = self.e.get()
        self.root.destroy()

    def ask_for_name(self):
        self.root = Tk()
        self.root.title('Account Creation')
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

    def add_new_account(self, account_name):
        Create_Json.add_new_account(account_name, self.key)

    def write_data_score(self, position, score):  # for storing the best score
        if self.data[position] < score:
            self.data[position] = score


class Media:
    def __init__(self):
        self.player = pyglet.media.Player()

        self.MenuM = pyglet.resource.media('resources/music/{} M.wav'.format
                                           (stats.data.data['soundtrack_in_use']))
        self.GameM = pyglet.resource.media('resources/music/{} G.wav'.format
                                           (stats.data.data['soundtrack_in_use']))
        self.DeathM = pyglet.resource.media('resources/music/{} D.wav'.format
                                            (stats.data.data['soundtrack_in_use']))

    def play(self):
        self.player.next_source()
        self.player.queue(self.pick())

        self.player.volume = stats.data.data['master_in_use'] * stats.data.data['music_in_use'] / 10000
        self.player.play()

    def pick(self):
        if window.screen_function == "Snake" and snake.game_state == 1:
            self.player.loop = True
            yield self.GameM

        elif window.screen_function == "Snake" and snake.game_state == 0:
            self.player.loop = False
            yield self.DeathM

        else:
            self.player.loop = True
            yield self.MenuM

    def adjust(self, value):
        self.player.volume = self.player.volume * value

    def adjust_music_volume(self):
        self.player.volume = (options.calculate_knob(0) * options.calculate_knob(1)) / 10000


class Effects:
    def __init__(self):
        self.player = pyglet.media.Player()

        # self.eat = pyglet.media.load(file, streaming=False)
        self.choose = pyglet.resource.media("resources/sounds/choose #1.wav", streaming=False)
        self.enter = pyglet.resource.media("resources/sounds/enter #1.wav", streaming=False)

        self.player.volume = stats.data.data['master_in_use'] * stats.data.data['effects_in_use'] / 10000

    def play(self, effect):
        self.player.next_source()
        self.player.queue(effect)
        self.player.play()

    def adjust(self):
        self.player.volume = (options.calculate_knob(0) * options.calculate_knob(2)) / 10000
        self.play(self.choose)


class Animation:
    def __init__(self, path, cordx, cordy, call_time=0.0, duration=0.0, amount=0, center=True):
        self.object = pyglet.resource.image(path)
        if center:
            # noinspection PyTypeChecker
            center_image(self.object)
        self.object = pyglet.sprite.Sprite(self.object, x=cordx, y=cordy)

        self.time = 0  # keeps track of how long we were doing an animation
        self.call_time = call_time  # how often will pyglet call a function
        self.duration = duration  # total time an animation should take
        self.amount = amount  # an amount given to an object every pyglet call

        # for movement and calculations
        self.x_amount = 0
        self.y_amount = 0
        self.time2 = 0

    def prepare_movement(self, new_x, new_y):  # to calculate how to move, mainly for background
        self.x_amount = (new_x - self.object.x) / (self.duration / self.call_time)
        self.y_amount = (new_y - self.object.y) / (self.duration / self.call_time)

    def move(self, dt):
        self.object.x += self.x_amount
        self.object.y += self.y_amount

        self.time += self.call_time
        if self.time >= self.duration:
            pyglet.clock.unschedule(self.move)
            self.time = 0

    def scale(self, dt):
        self.object.scale += self.amount

        self.time2 += self.call_time
        if self.time2 >= self.duration:
            pyglet.clock.unschedule(self.scale)
            self.time2 = 0

    def prepare_animation(self, amount=None, duration=None):
        if amount is not None:
            self.amount = amount
        if duration is not None:
            self.duration = duration

    def rotate(self, dt):
        self.object.rotation += self.amount
        self.time += self.call_time
        if self.time >= self.duration:
            pyglet.clock.unschedule(self.rotate)
            self.time = 0

    def fade(self, dt):
        self.object.opacity += self.amount
        self.time += self.call_time
        if self.time >= self.duration:
            pyglet.clock.unschedule(self.fade)
            self.time = 0

    def appear(self, dt):
        self.object.opacity = self.amount

    def reset(self):
        self.time = 0
        self.object.opacity = 0


class Snake:
    def __init__(self):
        """ There should be the game itself """
        self.food_count = 3
        self.time_played = 0
        self.difficulty = 0  # this will be changed by Menu(); 0 - easy, 1 - normal, 2 - hard, 3 - impossible
        self.move_time = 0.02
        self.last_body = 0  # where the last sprite is drawn
        self.snake_length = 0

        self.food_for_draw = 0
        self.relative_mode = False

        self.growth = 0  # indication if the snake should grow
        self.snake_field = np.zeros(2000, dtype='object')  # snake Sprites live here
        self.food_position = (0, 0)

        self.circle_field = []  # coordinates of snake bodies live here TODO numpy array
        self.circle_field.append((115, 475))  # this one is not drawn, but x+10 is

        self.block_coverage = 0  # to make sure snake doesn't change direction before it is in proper position
        self.new_step_direction = (10, 0)  # what is the new direction player gave TODO block size matters
        self.last_step_direction = (10, 0)  # where the snake moved last time TODO block size matters

        self.label = pyglet.text.Label('{}'.format(self.food_count - 3),
                                       font_size=540,
                                       color=(
                                           255, 255, 255, round(options.calculate_knob(4) * 255 / 100)))  # score label
        self.game_state = 0  # indication if you are alive or dead

    def start(self):
        self.relative_mode = stats.data.data['relative_mode']

        for i in range(16):  # creates the starting snake TODO block size matters
            self.add_snake_body()

        self.game_state = 1
        self.move_time = 0.02 - (self.difficulty * 5) / 1000
        self.spawn_food()
        pyglet.clock.schedule_interval(self.move, self.move_time)  # move with snake
        # self.update_main_batch()
        window.set_mouse_visible(False)

        media.adjust(1.05)
        media.play()

    def pause(self):
        window.active_window = 0
        window.set_mouse_visible(True)
        pyglet.clock.unschedule(snake.move)

        media.adjust(0.01)

    def play(self):
        window.active_window = 1
        window.set_mouse_visible(False)
        media.adjust(100)

        if self.game_state == 1:
            pyglet.clock.schedule_interval(self.move, self.move_time)

    def gen_nums_for_draw(self):
        for i in range(self.last_body, self.last_body + self.snake_length):
            if i < 2000:
                yield i

            else:
                yield i - 2000

    def add_snake_body(self):
        last_in_circle = self.circle_field[len(self.circle_field) - 1]  # take last coordinates of snake body
        self.circle_field.append((last_in_circle[0] + self.last_step_direction[0],
                                  last_in_circle[1] + self.last_step_direction[1]))  # append a new one

        last_in_circle = self.circle_field[len(self.circle_field) - 1]  # take the new last coordinates
        snake_field_position = self.last_body + self.snake_length

        if snake_field_position > 1999:
            snake_field_position -= 2000
        self.snake_field[snake_field_position] = pyglet.sprite.Sprite(shop.body, x=last_in_circle[0],
                                                                      y=last_in_circle[1], batch=window.batch)
        self.snake_length += 1

    def take_snake_body(self):  # pop the last snake body and coordinates
        self.circle_field.pop(0)

        if self.last_body > 1999:
            self.last_body -= 2000
            self.snake_field[self.last_body] = 0
            self.last_body += 1
        else:
            self.snake_field[self.last_body] = 0
            self.last_body += 1

        self.snake_length -= 1

    def spawn_food(self):
        self.food_position = (25 + random.randint(0, 23) * 50,
                              25 + random.randint(0, 15) * 50)  # set a new food position TODO window size matters

        try:  # check if it's valid
            self.circle_field.index(self.food_position)
            self.spawn_food()
        except ValueError:
            self.food_for_draw = pyglet.sprite.Sprite(shop.food, x=self.food_position[0], y=self.food_position[1])
            self.food_for_draw.scale = 0.21

    def check_for_direction(self):  # check if the snake is in proper position to change its direction
        if self.block_coverage == 0 and \
                (self.last_step_direction != (-self.new_step_direction[0], -self.new_step_direction[1])):
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
            self.circle_field.index(last_in_circle, 0, length_of_circle - 1)
            self.loss()
        except ValueError:
            pass

        if (self.food_position[0] - 35 < last_in_circle[0] < self.food_position[0] + 35) and \
                (self.food_position[1] - 35 < last_in_circle[1] < self.food_position[1] + 35):  # food collision check

            self.spawn_food()
            self.food_count += 1
            self.label = pyglet.text.Label('{}'.format(self.food_count - 3),
                                           font_size=540,
                                           color=(255, 255, 255,
                                                  round(options.calculate_knob(4) * 255 / 100)))  # update label
            self.growth = 1
            pyglet.clock.schedule_once(self.stop_grow, self.move_time * 5)  # start cutting tail TODO block size matters

    def stop_grow(self, dt):
        self.growth = 0

    def move(self, dt):
        repeat = int(dt / {0: 0.02, 1: 0.015, 2: 0.01, 3: 0.005}.get(self.difficulty))  # calculate compensation
        for i in range(repeat):  # to try to make it dependent on dt, it is not ideal though
            self.collision()
            self.check_for_direction()
            self.add_snake_body()
            if self.growth == 0:
                self.take_snake_body()

        # self.update_main_batch()
        self.time_played += dt

    def loss(self):  # what if you lose
        pyglet.clock.unschedule(self.move)
        self.game_state = 0

        stats.data.write_data_score(stats.data.indexed_data[1 + self.difficulty], self.food_count - 3)  # best score
        stats.data.data[stats.data.indexed_data[5 + self.difficulty]] += 1  # games played
        stats.data.data[stats.data.indexed_data[9 + self.difficulty]] += self.food_count - 3  # food eaten
        stats.data.data[stats.data.indexed_data[13 + self.difficulty]] += int(self.time_played)  # playtime

        snakies = stats.calculate_snakies()
        stats.data.data['snakies'] += snakies
        stats.data.data[stats.data.indexed_data[17 + self.difficulty]] += snakies

        stats.data.store_data()

        window.set_mouse_visible(True)
        pyglet.clock.schedule_interval(death.fade, death.call_time)
        pyglet.clock.schedule_once(death_desc.appear, death_desc.call_time)

        media.play()

    def reset(self, call_menu=True):  # restart the game
        menu.last_difficulty = self.difficulty
        pyglet.clock.unschedule(death.fade)  # if you reset and die before the animation ends, this takes care of it
        pyglet.clock.unschedule(death_desc.appear)
        death.reset(), death_desc.reset()

        self.__init__()
        pyglet.clock.unschedule(self.move)

        if call_menu:
            shop.background.amount = 0.0085
            pyglet.clock.schedule_interval(shop.background.scale, shop.background.call_time)

            window.call_menu()
            media.play()
        else:
            self.difficulty = menu.last_difficulty

            self.start()
            media.play()

    def set_new_direction_from_relative(self, side):
        if side == "LEFT":
            self.new_step_direction = {(10, 0): (0, 10), (0, 10): (-10, 0),
                                       (-10, 0): (0, -10), (0, -10): (10, 0)}.get(self.last_step_direction)

        elif side == "RIGHT":
            self.new_step_direction = {(10, 0): (0, -10), (0, -10): (-10, 0),
                                       (-10, 0): (0, 10), (0, 10): (10, 0)}.get(self.last_step_direction)

    def mouse_function(self, x, y, button):
        if button == mouse.LEFT and 1100 < x < 1200 and 0 < y < 90:
            self.game_state = -1
            window.screen_function = "Options"
            media.adjust(100)

    def keyboard_functions(self, symbol):
        if self.game_state == 1:  # if you are in the game and alive
            if window.active_window == 1:
                if not self.relative_mode:
                    if symbol == key.UP or symbol == key.W:
                        self.new_step_direction = (0, 10)
                    elif symbol == key.DOWN or symbol == key.S:
                        self.new_step_direction = (0, -10)
                    elif symbol == key.LEFT or symbol == key.A:
                        self.new_step_direction = (-10, 0)
                    elif symbol == key.RIGHT or symbol == key.D:
                        self.new_step_direction = (10, 0)

                else:
                    if symbol == key.J:
                        self.set_new_direction_from_relative("LEFT")
                    elif symbol == key.K:
                        self.set_new_direction_from_relative("RIGHT")

                if symbol == key.ESCAPE:
                    self.pause()

            elif symbol == key.ESCAPE and window.active_window == 0:
                self.play()

        elif self.game_state == 0:  # if you are in the game and dead
            if symbol == key.SPACE or symbol == key.R or symbol == key.NUM_0:
                self.reset(call_menu=False)

            elif symbol == key.ENTER:
                self.reset()

            elif symbol == key.ESCAPE:
                self.reset()


if __name__ == '__main__':
    window = Window()
    menu = Menu()
    stats = Stats()
    shop = Shop()
    options = Options()
    snake = Snake()
    media = Media()

    effect = Effects()

    """ Snake things """
    grid = pyglet.resource.image('textures/interface/grid.png')
    pause = pyglet.resource.image('textures/interface/pause.png')

    grid = pyglet.sprite.Sprite(grid, x=1, y=0)
    pause = pyglet.sprite.Sprite(pause)
    grid.opacity = round(options.calculate_knob(3) * 255 / 100)

    """ Menu things """
    menu_left = pyglet.resource.image('textures/interface/menu_left.png')
    menu_arrow = pyglet.resource.image('textures/interface/menu_arrow.png')
    menu_difficulty = pyglet.resource.image('textures/interface/menu_difficulty.png')

    cross_relative = pyglet.resource.image('textures/interface/cross.png')
    cross_relative = pyglet.sprite.Sprite(cross_relative, x=420, y=190)

    center_image(menu_arrow)
    menu_left = pyglet.sprite.Sprite(menu_left, x=0, y=0)
    menu_arrow2 = pyglet.sprite.Sprite(menu_arrow, x=800, y=500)
    menu_difficulty = pyglet.sprite.Sprite(menu_difficulty, x=396, y=175)

    menu_arrow_1 = Animation('textures/interface/menu_arrow.png',
                             377, 405, call_time=0.01, duration=0.06)
    death = Animation('textures/interface/death.png',
                      0, 0, call_time=1 / 84, duration=3, amount=1, center=False)
    death_desc = Animation('textures/interface/death_description.png',
                           0, 0, call_time=3.5, amount=255, center=False)

    death.object.opacity, death_desc.object.opacity = 0, 0
    menu_arrow_1.object.rotation, menu_arrow2.rotation = 180, 180

    """ Start things """
    Tk().withdraw()
    window.call_menu()
    media.play()
    pyglet.clock.schedule_once(stats.security_check, 0.01)  # security check
    pyglet.clock.schedule_interval(window.update, 1 / 360)  # TODO temporary fix
    pyglet.app.run()
