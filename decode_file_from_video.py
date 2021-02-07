import cv2
import numpy as np

BIT_SIZE = 2  # 2x2
COL_0 = (0, 0, 255)
COL_1 = (0, 255, 0)
COL_DELIM = (255, 0, 0)


def compare_pixels(p1, p2, i):
    return p2[i] - p1[i] < 50
    # return sum(np.absolute(np.subtract(p1, p2))) < 150


vid = cv2.VideoCapture("encoded/video.mp4")
success, frame = vid.read()
count = 1

all_bytes = []
file_name = []
reading_file_name = False

byte = np.uint8(0)
i = 7

while success:
    height, width, _ = frame.shape
    print("frame%d" % count)
    # cv2.imwrite("frame%d.png" % count, frame)

    for y in range(0, height, BIT_SIZE):
        for x in range(0, width, BIT_SIZE):
            (b, g, r) = frame[y, x]
            col = (r, g, b)

            if compare_pixels(col, COL_1, 1):
                byte = byte | 1 << i
            elif compare_pixels(col, COL_DELIM, 0):
                print(f"found delim... x:{x}, y:{y}")
                if not file_name:
                    reading_file_name = True
                elif reading_file_name:
                    print(f"decoding file: {str(bytes(file_name), 'utf-8')}")
                    reading_file_name = False
                else:
                    print("Finished reading file.")
                    f = open(f"decoded/{str(bytes(file_name), 'utf-8')}", "wb")
                    f.write(bytes(all_bytes))
                    f.close()
                    all_bytes = []
                    file_name = []
                continue

            i -= 1
            if i < 0:
                if reading_file_name:
                    file_name.append(byte)
                else:
                    all_bytes.append(byte)
                i = 7
                byte = np.uint8(0)

    success, frame = vid.read()
    count += 1
