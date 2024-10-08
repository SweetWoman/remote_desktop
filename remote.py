import struct
import socket
import numpy as np
from PIL import Image, ImageTk
import threading
import re
import cv2
import time
import sys
import platform
from remote_gui import ImageViewer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout

# socket缓冲区大小
bufsize = 1024
host = "192.168.1.157"
port = 8080

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((host, port))

# lenb: 接收图像类型和长度
lenb = soc.recv(5)
imtype, le = struct.unpack(">BI", lenb)
imb = b''
while le > bufsize:
    t = soc.recv(bufsize)
    imb += t
    le -= len(t)
while le > 0:
    t = soc.recv(le)
    imb += t
    le -= len(t)
data = np.frombuffer(imb, dtype=np.uint8)
img = cv2.imdecode(data, cv2.IMREAD_COLOR)# 返回图像为BGR

app = QApplication(sys.argv)
win = ImageViewer()
win.show()
# sys.exit(app.exec_())

while True:
    # cv2.imshow("main", img)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # cv2.imshow("main", img)
    win.setImage(img)
    lenb = soc.recv(5)
    imtype, le = struct.unpack(">BI", lenb)
    imb = b''
    while le > bufsize:
        t = soc.recv(bufsize)
        imb += t
        le -= len(t)
    while le > 0:
        t = soc.recv(le)
        imb += t
        le -= len(t)
    data = np.frombuffer(imb, dtype=np.uint8)
    ims = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if imtype == 1:
        # 全传
        img = ims
    else:
        # 差异传
        img = img ^ ims
    # img = img + ims
    # imsh = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
    cv2.waitKey(50)

