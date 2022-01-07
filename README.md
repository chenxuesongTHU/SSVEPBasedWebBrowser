# 展示页面 stimuli
包含两个窗口，即用 **psychopy.visual** 创建两个win或其他方法，需要尝试下。

## 页面展示区
在屏幕的左侧，占屏幕的大部分，用于展示页面
## 闪烁块展示区
在屏幕的右侧，占很小的比例，展示两个flicker，绑定上滑和下滑两个功能，可通过绑定向上、向下键盘按键实现。


# 模型部分 Models
CCA: 根据flicker的频率生成模版信号并进行计算
[参考链接](https://github.com/aaravindravi/PythonBox_OpenViBE_SSVEP_CCA/blob/master/4ClassCCA.py)

# 通信部分 Communication
与DSI24 的TCP/IP server进行通信
