import torch
import cv2
import mss
import numpy as np
from pynput.mouse import Controller
from ctypes import wintypes
import mouse
#导入模型
model_path="D:\\cs2_yolov5\\model\\cs2_2_halfps_640_384.engine"
workspace="D:\\cs2_yolov5\\yolov5"#工作区目录
model =torch.hub.load(workspace,"custom",path=model_path,source="local")


model.conf=0.3
model.iou=0.45
#model.names={"ct","t"}

def screen_shot():
    #截取屏幕中心长宽为分辨率2/5倍的画面（因游戏里分辨率为2560*1440，所以截取如下画面），在游戏外，如果电脑分辨率为2560*1440，但可能会因为电脑里设置的屏幕缩放而出现问题，如果想在游戏外检测效果，应该关掉屏幕缩放
    monitor = {"top": 432, "left": 768, "width": 1024, "height": 576}
    with mss.mss()as sct:

        screenshot=sct.grab(monitor)
        if screenshot:
            img = np.array(screenshot)
            img_bgr = img[:,:,:3]

            # 模型推理
            result = model(img_bgr)
            print(result.pandas().xywhn)
            if len(result.pandas().xywhn[0])!=0:
                return result.pandas().xywhn
            return None
        
def mouse_move():
    current_Mouse=Controller()
    while True:
        info=screen_shot()
        mouse.monitor_right_button()
        dx=0
        dy=0
        min_dx=2000
        min_dy=1000
        if info is not None and mouse.right_down:#检测到目标并且右键保存在按下状态
            for target in info:
                aim_height=target.iloc[0]['height']*1440
                aim_x=target.iloc[0]['xcenter']*1024+768
                aim_y=target.iloc[0]['ycenter']*576+432
                current_x,current_y=current_Mouse.position
                dx=aim_x-current_x
                dy=aim_y-current_y-aim_height*0.13
                min_dx=min(min_dx,dx)
                min_dy=min(min_dy,dy)
            mouse.send_input(int(min_dx),int(min_dy),mouse.win32con.MOUSEEVENTF_MOVE)


def get_screen_size():
    user32=mouse.ctypes.windll.user32
    screeen_width=user32.GetSystemMetrics(0)
    screeen_height=user32.GetSystemMetrics(1)
    print(screeen_width,screeen_height)
    
get_screen_size()#查看分辨率

mouse_move()


