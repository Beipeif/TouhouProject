import time
import ctypes
import win32gui
import cv2
import numpy as np
import pyautogui
from PIL import Image

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def get_window_pos(name):
    name = name
    win_handle = win32gui.FindWindow(0, name)
    # 获取窗口句柄
    if win_handle == 0:
        return None
    else:
        return win32gui.GetWindowRect(win_handle), win_handle


def pause():
    PressKey(1)  # 按ESC键选择继续
    time.sleep(0.2)
    ReleaseKey(1)
    reset_key()


def reset_key():
    key = (0x48, 0x50, 0x4D, 0x4B, 0x2C, 0x2D, 0x2A)
    actions = [0, 0, 0, 0, 0, 0, 0]
    activates(actions, key)
    return 'reset_success'


def activates(act, key):
    #print(act, key)
    press = [key[i] for i, e in enumerate(act) if e == 1]
    if len(press) != 0:
        for i in press:
            PressKey(i)
        time.sleep(0.02)
        for i in press:
            ReleaseKey(i)
    else:
        time.sleep(0.02)


def activate(acts, key, imgz):
    press = [key[i] for i, e in enumerate(acts) if e == 1]
    if len(press) != 0:
        for i in range(len(acts)):
            if int(acts[i]):
                PressKey(key[i])
            else:
                ReleaseKey(key[i])
    else:
        pass
    time.sleep(0.05)
    img = (
        getimage(imgz[0], imgz[1], imgz[2], imgz[3]),
        getimage(imgz[0], imgz[1], imgz[2], imgz[3]),
        getimage(imgz[0], imgz[1], imgz[2], imgz[3]),
    )
    temp = Image.fromarray(img[1].astype('uint8')).convert('RGB')
    temp.save('./1img_temp.jpg')
    #temp = Image.fromarray(img[2].astype('uint8')).convert('RGB')
    #temp.save('./2img_temp.jpg')
    #temp = Image.fromarray(img[0].astype('uint8')).convert('RGB')
    #temp.save('./img_temp.jpg')
    img = np.hstack((img[0], img[1], img[2]))

    return img


def getimage(x1, y1, wi, hi):
    img = pyautogui.screenshot(
        region=(x1, y1, wi, hi)
    )
    img = cv2.resize(np.asarray(img), (wi, hi))
    return img


def getimage3(imgz):
    img = (
        getimage(imgz[0], imgz[1], imgz[2], imgz[3]),
        getimage(imgz[0], imgz[1], imgz[2], imgz[3]),
        getimage(imgz[0], imgz[1], imgz[2], imgz[3]),
    )
    "采集多帧数据使用, 将多帧图像整合"
    #out_img = img[0]
    #out_img = Image.fromarray(out_img.astype('uint8')).convert('RGB')
    #out_img.save('./0out_temp.jpg')
    #out_img = img[1]
    #out_img = Image.fromarray(out_img.astype('uint8')).convert('RGB')
    #out_img.save('./1out_temp.jpg')
    #out_img = img[2]
    #out_img = Image.fromarray(out_img.astype('uint8')).convert('RGB')
    #out_img.save('./2out_temp.jpg')

    img = np.hstack((img[0], img[1], img[2]))

    return img


def restart_key():
    reset_key()
    time.sleep(0.4)
    PressKey(0x50)  # 按下键选择继续
    time.sleep(0.2)
    ReleaseKey(0x50)
    time.sleep(0.4)
    PressKey(0x50)  # 按下键选择继续
    time.sleep(0.2)
    ReleaseKey(0x50)
    time.sleep(0.4)
    PressKey(0x1C)  # 按回车选择继续
    time.sleep(0.2)
    ReleaseKey(0x1C)
    time.sleep(0.4)
    PressKey(0x48)  # 按上键选择继续
    time.sleep(0.2)
    ReleaseKey(0x48)
    time.sleep(0.4)
    PressKey(0x1C)  # 按回车选择继续
    time.sleep(0.2)
    ReleaseKey(0x1C)
    time.sleep(0.4)
    return 0
