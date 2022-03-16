from PIL import Image
import numpy as np
from subprocess import Popen, PIPE
import json

f = open('config.json')
config = json.load(f)

BIT_SIZE = config['BIT_SIZE']
COL_1 = (*config['ONE_BIT_COLOR'], )
COL_0 = (*config['ZERO_BIT_COLOR'], )
COL_DELIM = (*config['DELIMITER_COLOR'], )
WIDTH = config['FRAME_WIDTH']
HEIGHT = config['FRAME_HEIGHT']
ENCODED_VIDEO = config['ENCODED_VIDEO']

f.close()

FRAME_NUM = 0

p = Popen(
    [
        "ffmpeg",
        "-y",
        "-f",
        "image2pipe",
        "-vcodec",
        "png",
        "-r",
        "24",
        "-i",
        "-",
        "-vcodec",
        "mpeg4",
        "-qscale",
        "5",
        "-r",
        "24",
        ENCODED_VIDEO,
    ],
    stdin=PIPE,
)


def get_new_frame(default_col=COL_0):
    global FRAME_NUM
    if FRAME_NUM > 0:
        array = np.array(frame, dtype=np.uint8)
        new_image = Image.fromarray(array)
        # new_image.save(f"frame_{FRAME_NUM}.png")
        new_image.save(p.stdin, "PNG")
        print(f"fed frame_{FRAME_NUM}")
    FRAME_NUM += 1
    return [[default_col] * WIDTH for _ in range(HEIGHT)]


frame = get_new_frame()


def read_in_chunks(file_object, chunk_size=1024):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def paint_pixel(x, y, col):
    for j in range(BIT_SIZE):
        for k in range(BIT_SIZE):
            frame[y + j][x + k] = col


def encode_bytes(x, y, bytes, col=COL_1):
    for byte in bytes:
        for i in range(8):
            if ((byte >> (7 - i)) & 1) == 1:
                paint_pixel(x, y, col)
            x += BIT_SIZE

            if x > WIDTH:
                y += BIT_SIZE
                x = 0

            if y + BIT_SIZE > HEIGHT:
                print("NEW FRAME!")  # Should create a new frame here
    return x, y


def check_create_frame(x, y):
    if x + BIT_SIZE > WIDTH:
        y += BIT_SIZE
        x = 0
    if y + BIT_SIZE > HEIGHT:
        x = 0
        y = 0
        global frame
        frame = get_new_frame()
    return x, y


def encode_file_name(x, y, file_name):
    x, y = check_create_frame(x, y)
    paint_pixel(x, y, COL_DELIM)
    x, y = check_create_frame(x + BIT_SIZE, y)
    x, y = encode_bytes(x, y, str.encode(file_name))
    x, y = check_create_frame(x, y)
    paint_pixel(x, y, COL_DELIM)
    return check_create_frame(x + BIT_SIZE, y)


def encode_file(file_name, frame_x=0, frame_y=0):
    frame_x, frame_y = encode_file_name(frame_x, frame_y, file_name)
    with open(file_name, "rb") as f:
        for piece in read_in_chunks(f):
            for byte in piece:
                for i in range(8):
                    val = (byte >> (7 - i)) & 1
                    col = COL_0 if val == 0 else COL_1

                    paint_pixel(frame_x, frame_y, col)
                    frame_x += BIT_SIZE

                    if frame_x + BIT_SIZE > WIDTH:
                        frame_y += BIT_SIZE
                        frame_x = 0

                    if frame_y + BIT_SIZE > HEIGHT:
                        global frame
                        frame = get_new_frame()
                        frame_x = 0
                        frame_y = 0
    frame_x, frame_y = check_create_frame(frame_x, frame_y)
    paint_pixel(frame_x, frame_y, COL_DELIM)  # to denote end of file
    get_new_frame()  # just to trigger frame save since currently only encoding 1 file


encode_file("encode_this.txt")

p.stdin.close()
p.wait()
