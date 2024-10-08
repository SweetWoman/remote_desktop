from PIL import ImageGrab
import cv2
import numpy as np
import mouse
import socket
import struct
import time

IDLE = 0.05

#图像质量
IMQUALITY = 90

# 创建socket
host = ('0.0.0.0', 8080)
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind(host)
soc.listen(1)
conn, addr = soc.accept()


imorg = np.asarray(ImageGrab.grab()) # 截取桌面并编码
_, imbyt = cv2.imencode(".jpg", imorg, [cv2.IMWRITE_JPEG_QUALITY, IMQUALITY])#将图像数据编码成jpg，最后一个参数是编码质量
imnp = np.asarray(imbyt, np.uint8)# 将编码后的图像数据imbyt转换为一个NumPy数组，数据类型为np.uint8
img = cv2.imdecode(imnp, cv2.IMREAD_COLOR)# 将上一步得到的NumPy数组imnp解码回图像数据

lenb = struct.pack(">BI", 1, len(imbyt)) # 图像长度
conn.sendall(lenb)
conn.sendall(imbyt)

while True:
    # fix for linux
    time.sleep(IDLE)
    imgnpn = np.asarray(ImageGrab.grab()) # 截取桌面，图像转为numpy数组
    #将图像数据编码成jpg，最后一个参数是编码质量
    # 返回值：第一个为bool，第二个：编码后图像
    _, timbyt = cv2.imencode(".jpg", imgnpn, [cv2.IMWRITE_JPEG_QUALITY, IMQUALITY])
    imnp = np.asarray(timbyt, np.uint8) # 将编码后的图像数据timbyt转换为一个NumPy数组，数据类型为np.uint8。这是因为图像数据通常以8位无符号整数的形式存储
    imgnew = cv2.imdecode(imnp, cv2.IMREAD_COLOR) # 将上一步得到的NumPy数组imnp解码回图像数据
    # 计算图像差值
    imgs = imgnew ^ img
    if (imgs != 0).any():
        # 画质改变
        pass
    else:
        continue
    # imbyt = timbyt
    img = imgnew
    # 无损压缩
    _, imb = cv2.imencode(".jpg", imgs)
    l1 = len(timbyt)  # 原图像大小
    l2 = len(imb)  # 差异图像大小
    if l1 > l2:
        # 传差异化图像
        print("差异化图像")
        lenb = struct.pack(">BI", 0, l2)
        conn.sendall(lenb)
        conn.sendall(imb)
    else:
        # 传原编码图像
        print("原编码图像")        
        # cv2.imwrite("./orgin.jpg", imgnew)
        # cv2.imwrite("./contract.jpg", imgs)
        # cv2.waitKey(1000)
        # exit()
        lenb = struct.pack(">BI", 1, l1)
        conn.sendall(lenb)
        conn.sendall(timbyt)
        

