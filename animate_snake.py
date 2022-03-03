"""

This creates the beautiful animation of snake in the shop :)

"""


import pyglet
import numpy as np

batch = pyglet.graphics.Batch()
array = np.zeros(30, dtype='object')
body = None

phase = 0
step = 0
last_x = 0
last_y = 0
last_body = 0

scale_factor = 1
body_scale_factor = 0.7
correction_factor = 5


def center_image(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


def create(body_file, x, y):
    """ Fill the array with given snake body """
    global body, phase, step, last_x, last_y, last_body, array
    body = pyglet.resource.image(body_file)
    center_image(body)

    last_x = x
    last_y = y

    for i in range(30):
        perform_operation(i)


def switch(body_file):
    global body, last_body, last_x, phase
    body = pyglet.resource.image(body_file)
    center_image(body)

    for i in range(30):
        move(i)


def move(dt):
    """ Move the snake """
    global last_body, last_x
    perform_operation(last_body)
    last_body += 1

    if last_body > 29:
        last_body = 0

    for obj in array:
        obj.x -= correction_factor

    last_x -= correction_factor


def perform_operation(index):
    global phase, step, last_x, last_y, array

    if phase == 0:
        last_x = last_x + 10*scale_factor
        array[index] = pyglet.sprite.Sprite(body, x=last_x, y=last_y, batch=batch)
        array[index].scale = body_scale_factor

    elif phase == 1:
        last_y = last_y + 10*scale_factor
        array[index] = pyglet.sprite.Sprite(body, x=last_x, y=last_y, batch=batch)
        array[index].scale = body_scale_factor

    elif phase == 2:
        last_x = last_x + 10*scale_factor
        array[index] = pyglet.sprite.Sprite(body, x=last_x, y=last_y, batch=batch)
        array[index].scale = body_scale_factor

    elif phase == 3:
        last_y = last_y - 10*scale_factor
        array[index] = pyglet.sprite.Sprite(body, x=last_x, y=last_y, batch=batch)
        array[index].scale = body_scale_factor

    step += 1

    if step > 4:
        step = 0
        phase += 1

    if phase > 3:
        phase = 0


if __name__ == '__main__':
    pass
