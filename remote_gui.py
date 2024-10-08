import cv2
import sys
from PyQt5 import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout

class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setUI()
        # self.setImage()

    #设置ui界面
    def setUI(self):
        self.resize(800, 600)
        self.setWindowTitle('picture')
        self.imgLabel = ImageLabel()
        self.imgLabel.resize(800, 600) #设置label的大小,图片会适配label的大小
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.imgLabel)
        self.setLayout(self.hbox)

    def setImage(self, img2):
        # img2 = cv2.imread('test.jpg') #opencv读取图片
        # img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB) #opencv读取的bgr格式图片转换成rgb格式
        _image = QtGui.QImage(img2, # 图像
                                img2.shape[1], # 宽度
                                img2.shape[0], # 高度
                                img2.shape[1] * 3, # 行字节数
                                QtGui.QImage.Format_RGB888) #pyqt5转换成自己能放的图片格式
        jpg_out = QtGui.QPixmap(_image).scaled(self.imgLabel.width(), self.imgLabel.height()) #设置图片大小
        self.imgLabel.setPixmap(jpg_out) #设置图片显示

class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        # self.image_path = image_path
        # self.load_image()

    def mousePressEvent(self, event):
        # 鼠标点击事件
        print("Mouse Press Event at", event.pos())
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # 鼠标移动事件
        print("Mouse Move Event at", event.pos())
        super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        # 键盘事件
        key = event.key()
        if key == Qt.Key_Left:
            print("Left arrow key pressed")
        elif key == Qt.Key_Right:
            print("Right arrow key pressed")
        else:
            print("Key", key, "pressed")
        super().keyPressEvent(event)