from psychopy import visual#, event, core,gui ,data,  logging #import c
from numpy import sin, pi
import time

from psychopy import visual#, event, core,gui ,data,  logging #import c
from numpy import sin, pi
import time


class Rect:
    def __init__(self,position,win,flicker_frequency,phase):
        self.obj = visual.Rect(win,width=160, height=160,lineColor='white',fillColor='white',pos=position)
        self.phase = phase
        self.flicker_frequency = flicker_frequency


class Frame:
    def __init__(self,num,rect,simple_fs,text):
        self.Rect = []
        self.Text = []
        self.simple_fs = simple_fs
        self.num = num
        self.current_frame = 0
        for i in range(0,num):
            self.Rect.append(rect[i])
        for i in range(0,num):
            self.Text.append(text[i])

    # 获取i号方块在current_frame时的亮度
    def get_brightness(self,i):
        return (sin(self.Rect[i].flicker_frequency * (self.current_frame / self.simple_fs) * pi * 2 + self.Rect[i].phase))
        # return (1 + sin(self.Rect[i].flicker_frequency * (self.current_frame / self.simple_fs) * pi * 2 + self.Rect[i].phase)) / 2

    # 更新全部方块的亮度
    def update(self):
        for i in range (0,self.num):
            self.Rect[i].obj.contrast = self.get_brightness(i)
            self.Rect[i].obj.draw()
            self.Text[i].draw()
        win.flip()
        self.current_frame += 1


# 初始化窗口
win = visual.Window([1366,768], color='black', units='pix',fullscr=True)

# 初始化各个方框的文字
texts = []
texts.append(visual.TextStim(win,text='sw',pos=(0,300),color='black', height=40))
texts.append(visual.TextStim(win,text='C',pos=(300,0),color='black', height=40))
texts.append(visual.TextStim(win,text='H',pos=(0,-300),color='black', height=40))
texts.append(visual.TextStim(win,text='M',pos=(-300,0),color='black', height=40))

img = visual.ImageStim(win, '../data/landingPage.png')
img.draw()

# 初始化实验基本信息
rect = []
num = 4
time_last = 10
simple_fs = 60
last_frame = time_last * simple_fs
trial = 2
trial_frame = trial * last_frame

# 初始化每个方框的位置
pos1=(0,300)
pos2=(300,0)
pos3=(0,-300)
pos4=(-300,0)

# 初始化每个方框的频率
flicker_frequency_1 = 8
flicker_frequency_2 = 9
flicker_frequency_3 = 10
flicker_frequency_4 = 11

# 初始化每个方框的相位
phase_1 = 0
phase_2 = 0.5*pi
phase_3 = pi
phase_4 = 1.5*pi


# 实例化四个方框，并存入一个list
rect.append(Rect(pos1,win,flicker_frequency_1,phase_1))
rect.append(Rect(pos2,win,flicker_frequency_2,phase_2))
rect.append(Rect(pos3,win,flicker_frequency_3,phase_3))
rect.append(Rect(pos4,win,flicker_frequency_4,phase_4))

# 实例化Frame
frames = Frame(num,rect,simple_fs,texts)
start = time.time()
k = True
start_time = time.time()

# 开始刺激
while True:
    frames.update()
    now = time.time() - start_time  # 现在时刻
    # 每60帧打印一下当前系统时间
    if frames.current_frame % 60 == 0:
        print(frames.current_frame, now)
    if frames.current_frame > trial_frame:
        k = False
        win.close()




