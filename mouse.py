
import numpy as np
from pynput.mouse import Controller
import win32con 
import ctypes
from ctypes import wintypes


def is_right_button_pressed():
    
    VK_RBUTTON = 0x02  # 鼠标右键的虚拟键代码

    # 导入user32.dll中的GetAsyncKeyState函数
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    GetAsyncKeyState = user32.GetAsyncKeyState
    GetAsyncKeyState.argtypes = [wintypes.INT]
    GetAsyncKeyState.restype = wintypes.SHORT
    # 获取鼠标右键的状态
    state = GetAsyncKeyState(VK_RBUTTON)
    # 检查最高位是否被设置，如果设置则按键被按下
    return state & 0x8000 != 0


right_down=False#判断右键是否保持在按下状态
right_button_was_pressed = False

def monitor_right_button():
    global right_down,right_button_was_pressed
    right_button_pressed = is_right_button_pressed()

    if right_button_pressed and right_button_was_pressed:
        right_down=True
    if right_button_pressed and not right_button_was_pressed:
        True
    if not right_button_pressed and right_button_was_pressed:
        right_down=False
    if not right_button_pressed and not right_button_was_pressed:
        right_down=False
    right_button_was_pressed=right_button_pressed


def left_mouse_down():
    INPUT_MOUSE=0
    MOUSE_LEFTDOWN=win32con.MOUSEEVENTF_LEFTDOWN
    extra=ctypes.c_ulong(0)

    mi=MOUSEINPUT(0,0,0,MOUSE_LEFTDOWN,0,ctypes.pointer(extra))
    input=INPUT(INPUT_MOUSE,mi)

    ctypes.windll.user32.SendInput(1,ctypes.pointer(input),ctypes.sizeof(input))


def left_mouse_up():
    INPUT_MOUSE=0
    MOUSE_LEFTUP=win32con.MOUSEEVENTF_LEFTUP
    extra=ctypes.c_ulong(0)

    mi=MOUSEINPUT(0,0,0,MOUSE_LEFTUP,0,ctypes.pointer(extra))
    input=INPUT(INPUT_MOUSE,mi)

    ctypes.windll.user32.SendInput(1,ctypes.pointer(input),ctypes.sizeof(input))

    
def is_left_button_pressed():
    # 定义常量
    VK_RBUTTON = 0x01  # 鼠标左键的虚拟键代码

    # 导入user32.dll中的GetAsyncKeyState函数
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    GetAsyncKeyState = user32.GetAsyncKeyState
    GetAsyncKeyState.argtypes = [wintypes.INT]
    GetAsyncKeyState.restype = wintypes.SHORT
    # 获取鼠标左键的状态
    state = GetAsyncKeyState(VK_RBUTTON)
    # 检查最高位是否被设置，如果设置则按键被按下
    return state & 0x8000 != 0


left_down=False#判断左键是否保持在按下状态
left_button_was_pressed = False

def monitor_left_button():
    global left_down,left_button_was_pressed
    left_button_pressed = is_left_button_pressed()

    if left_button_pressed and left_button_was_pressed:
        left_down=True
    if left_button_pressed and not left_button_was_pressed:
        True
    if not left_button_pressed and left_button_was_pressed:
        left_down=False
    if not left_button_pressed and not left_button_was_pressed:
        left_down=False
    left_button_was_pressed=left_button_pressed



#定义input结构体
class MOUSEINPUT(ctypes.Structure):
        _fields_=[
            ("dx",ctypes.c_long),
            ("dy",ctypes.c_long),
            ("mouseData",ctypes.c_ulong),
            ("dwFlags",ctypes.c_ulong),
            ("time",ctypes.c_ulong),
            ("dwExtraInfo",ctypes.POINTER(ctypes.c_ulong))
        ]
class INPUT(ctypes.Structure):
        _fields_=[
            ("type",ctypes.c_ulong),
            ("mi",MOUSEINPUT)
        ]


def send_input(dx,dy,dwFlags):

    extra=ctypes.c_ulong(0)
    mi=MOUSEINPUT(dx,dy,0,dwFlags,0,ctypes.pointer(extra))
    inp=INPUT(ctypes.c_ulong(0),mi)
    ctypes.windll.user32.SendInput(1,ctypes.pointer(inp),ctypes.sizeof(inp))