from PySide6.QtWidgets import QWidget,QSlider, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from maya import cmds
import maya.OpenMayaUI as omui
from shiboken6 import wrapInstance


def main_maya_window():
    pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(pointer), QWidget)


class AnimationTool(QWidget):
    def __init__(self):
        super().__init__(main_maya_window())
        self.setWindowTitle("Animation Tool")
        self.setWindowFlags(Qt.Window)
        self.build_ui()

    def build_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.create_sub_layout()
        self.create_labels()
        self.create_slider()
        self.create_button()

    def create_sub_layout(self):
        self.timing_layout = QHBoxLayout()
        self.translate_parameters_layout = QHBoxLayout()
        self.rotate_parameters_layout = QHBoxLayout()
        self.scale_parameters_layout = QHBoxLayout()
        self.main_layout.addLayout(self.timing_layout)
        self.main_layout.addLayout(self.translate_parameters_layout)
        self.main_layout.addLayout(self.rotate_parameters_layout)
        self.main_layout.addLayout(self.scale_parameters_layout)


    def create_labels(self):
        self.timing_label = QLabel("Animation Timing")
        self.timing_layout.addWidget(self.timing_label)
        self.translate_label = QLabel("Translate Parameters")
        self.translate_parameters_layout.addWidget(self.translate_label)
        self.rotate_label = QLabel("Rotate Parameters")
        self.rotate_parameters_layout.addWidget(self.rotate_label)
        self.scale_label = QLabel("Scale Parameters")
        self.scale_parameters_layout.addWidget(self.scale_label)


    def create_button(self):
        self.confirm_animation_button = QPushButton("Confirm Animation")
        self.main_layout.addWidget(self.confirm_animation_button)
        self.confirm_animation_button.clicked.connect(self.apply_scale)



    def create_slider(self):
        self.scale_slider = QSlider() 
        self.scale_slider.setOrientation(Qt.Horizontal)
        self.scale_slider.setRange(1, 300)
        self.scale_slider.setValue(50)
        self.timing_layout.addWidget(self.scale_slider)

    def update_label(self,scale_factor):
        self.scale_label.setText(f"{self.label_text_template} {scale_factor}")


    def apply_scale(self):
        scale_factor = self.scale_slider.value()/100.0
        self.update_label(scale_factor)
        selection = cmds.ls(selection=True, transforms=True)
        for obj in selection:
            cmds.setAttr(f"{obj}.scale", scale_factor, scale_factor, scale_factor)

def show_live_scale():
    global live_scale
    try:
        live_scale.close()
    except:
        pass
    live_scale = AnimationTool()
    live_scale.show()

show_live_scale()