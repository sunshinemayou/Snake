#! -*- coding:utf-8 -*-

#import win32api
#import win32con
import time
from PIL import ImageGrab

left = 300
top = 248
img_w = 589
img_h = 385
w = 31
h = 35
rows = 11
cols = 19
diff = 0.996
di = [0, -1, 0, 1]
dj = [1, 0, -1, 0]
blank = [0 for i in xrange(768)]

def hist_similar(lh, rh):
    return sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) for l, r in zip(lh, rh)) / len(lh)

def get_id(i, j):
    return i * cols + j

def is_direct_connected(images, i1, j1, i2, j2):
    if i1 == i2:
        if j1 > j2:
            j1, j2 = j2, j1
        for j in xrange(j1 + 1, j2):
            if images[i1][j]:
                return False
        return True
    else:
        if i1 > i2:
            i1, i2 = i2, i1
        for i in xrange(i1 + 1, i2):
            if images[i][j1]:
                return False
        return True

def is_connected(images, i1, j1, i2, j2):
    if j1 > j2:
        i1, i2 = i2, i1
        j1, j2 = j2, j1

    if i1 == i2 or j1 == j2:
        if is_direct_connected(images, i1, j1, i2, j2):
            return True

    for i in xrange(0, rows):
        if i == i1:
            if not images[i][j2] and is_direct_connected(images, i1, j1, i, j2) and is_direct_connected(images, i, j2, i2, j2):
                return True
        elif i == i2:
            if not images[i][j1] and is_direct_connected(images, i1, j1, i, j1) and is_direct_connected(images, i, j1, i2, j2):
                return True
        else:
            if not images[i][j1] and not images[i][j2] and is_direct_connected(images, i1, j1, i, j1) and is_direct_connected(images, i, j1, i, j2) and is_direct_connected(images, i, j2, i2, j2):
                return True

    for j in xrange(0, cols):
        if j == j1:
            if not images[i2][j] and is_direct_connected(images, i1, j1, i2, j) and is_direct_connected(images, i2, j, i2, j2):
                return True
        elif j == j2:
            if not images[i1][j] and is_direct_connected(images, i1, j1, i1, j) and is_direct_connected(images, i1, j, i2, j2):
                return True
        else:
            if not images[i1][j] and not images[i2][j] and is_direct_connected(images, i1, j1, i1, j) and is_direct_connected(images, i1, j, i2, j) and is_direct_connected(images, i2, j, i2, j2):
                return True

    return False

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    time.sleep(0.1)

def connect(i1, j1, i2, j2):
    click(left + j1 * w + 10, top + i1 * h + 10)
    click(left + j2 * w + 10, top + i2 * h + 10)

def main():
    img = ImageGrab.grab((left, top, left + img_w, top + img_h))
    images = []
    g = [[False for j in xrange(rows * cols)] for i in xrange(rows * cols)]
    cnt = rows * cols
    for i in xrange(rows):
        tmp = []
        for j in xrange(cols):
            tmp.append(img.crop((j * w + 3, i * h + 2, (j + 1) * w - 7, (i + 1) * h - 4)).histogram())
        images.append(tmp)

    for i in xrange(rows):
        for j in xrange(cols):
            if hist_similar(images[i][j], blank) > diff:
                images[i][j] = None
                cnt -= 1

    for i1 in xrange(rows):
        for j1 in xrange(cols):
            for i2 in xrange(rows):
                for j2 in xrange(cols):
                    if images[i1][j1] and images[i2][j2] and hist_similar(images[i1][j1], images[i2][j2]) > diff:
                        g[get_id(i1, j1)][get_id(i2, j2)] = True

    while cnt:
        for i1 in xrange(rows):
            for j1 in xrange(cols):
                for i2 in xrange(rows):
                    for j2 in xrange(cols):
                        if not (i1 == i2 and j1 == j2) and images[i1][j1] and images[i2][j2] and g[get_id(i1, j1)][get_id(i2, j2)] and is_connected(images, i1, j1, i2, j2):
                            connect(i1, j1, i2, j2)
                            images[i1][j1] = images[i2][j2] = None
                            cnt -= 2

if __name__ == '__main__':
    main()