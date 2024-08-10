import threading 
import torch
import mss
import numpy as np
from pynput.mouse import Controller
from ctypes import wintypes
import mouse
import  queue
import time
screenshot_queue=queue.Queue(maxsize=1)

model_path="E:\\cs_add_data\\cv3\\model\\cs2_2_halfps_640_384.engine"
workspace="E:\\cs_add_data\\cv3\\yolov5"
model=torch.hub.load(workspace,"custom",path=model_path,source="local")

model.conf=0.4
model.iou=0.35

def screen_shot():
    monitor = {"top": 432, "left": 768, "width": 1024, "height": 576}
    x=0
    last_time=0
    start=time.time()
    while True:
       
        x+=1
        if x%21==0:
            end=time.time()
            print("screen"+str((end-last_time)*50)+"ms")
            last_time=end
        with mss.mss() as sct:
            
            screenshot=sct.grab(monitor)
            if screenshot:
                img=np.array(screenshot)
                img_bgr=img[:,:,:3]
                
                if screenshot_queue.full():
                    screenshot_queue.get()
                screenshot_queue.put(img_bgr)

def distance(x1,y1,x2,y2):
    return x1*x1+y1*y1>x2*x2+y2*y2


def detect():
    current_mouse=Controller()
    x=0
    last_time=0
    start=time.time()
    while True:
        x+=1
        if x%21==0:
            end=time.time()
            print("detect"+str((end-last_time)*50.0)+"ms")
            last_time=end
        mouse.monitor_right_button()
        dx=0
        dy=0
        min_dx=1000
        min_dy=800
        try:
            img_bgr=screenshot_queue.get(timeout=1)
            result=model(img_bgr)
            if len(result.pandas().xywhn[0])!=0 and mouse.right_down:
                info=result.pandas().xywhn[0]
                current_x,current_y=current_mouse.position
                for index,target in info.iterrows():
                    aim_height=target['height']*1440
                    aim_x=target['xcenter']*1024+768
                    aim_y=target['ycenter']*576+432
                    dx=aim_x-current_x
                    dy=aim_y-current_y-aim_height*0.13
                    if distance(min_dx,min_dy,dx,dy):
                        min_dx=dx
                        min_dy=dy
                mouse.send_input(int(min_dx),int(min_dy),mouse.win32con.MOUSEEVENTF_MOVE)
        except queue.Empty:
            continue


def get_screen_size():
    user32=mouse.ctypes.windll.user32
    screeen_width=user32.GetSystemMetrics(0)
    screeen_height=user32.GetSystemMetrics(1)
    print(screeen_width,screeen_height)
    
get_screen_size()

thread_screen_shot = threading.Thread(target=screen_shot)
thread_detect = threading.Thread(target=detect)

thread_screen_shot.start()
thread_detect.start()

thread_screen_shot.join()
thread_detect.join()