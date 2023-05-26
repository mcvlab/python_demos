#encoding: utf-8

import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton

class ImageDisplay(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle('Image Display')
        self.setGeometry(100, 100, 400, 400)

        # 创建标签和布局
        self.label = QLabel(self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)

        # 创建按钮并添加到布局
        self.button = QPushButton('Switch Image', self)
        self.layout.addWidget(self.button)

        # 设置第一张图片
        self.image_index = 1
        self.set_image()

        # 将布局应用到窗口
        self.setLayout(self.layout)

        # 连接按钮信号与槽函数
        self.button.clicked.connect(self.switch_image)

    def set_image(self):
        # 根据当前图片索引设置图片
        if self.image_index == 1:
            self.pixmap = QPixmap('image1.png')
        elif self.image_index == 2:
            self.pixmap = QPixmap('image2.png')
        else:
            self.pixmap = QPixmap('image3.png')

        # 将图片显示在标签上
        self.label.setPixmap(self.pixmap)

    def switch_image(self):
        # 切换图片索引并设置新的图片
        if self.image_index == 3:
            self.image_index = 1
        else:
            self.image_index += 1

        self.set_image()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageDisplay()
    window.show()
    sys.exit(app.exec_())

