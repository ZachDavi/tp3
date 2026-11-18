from PySide6.QtWidgets import QWidget,QSpinBox, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from maya import cmds
from .animator import animate
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
        self.create_labels()
        self.create_sub_layout()
        self.add_widgets()
        self.create_button()

    def create_sub_layout(self):
        self.timing_layout = QHBoxLayout()
        self.translate_parameters_layout = QHBoxLayout()
        self.rotate_parameters_layout = QHBoxLayout()
        self.scale_parameters_layout = QHBoxLayout()


    def create_labels(self):
        self.timing_label = QLabel("Animation Timing")
        self.translate_label = QLabel("Translate Parameters")
        self.rotate_label = QLabel("Rotate Parameters")
        self.scale_label = QLabel("Scale Parameters")
        self.animation_duration_label = QLabel("Durations (Frames): ")
        self.step_label = QLabel("Step (Frames): ")

    def add_widgets(self):

        #Timing Layout
        self.create_duration_spinbox()
        self.create_step_spinbox()
        self.main_layout.addWidget(self.timing_label)
        self.main_layout.addLayout(self.timing_layout)
        self.timing_layout.addWidget(self.animation_duration_label)
        self.timing_layout.addWidget(self.duration_spinbox)
        self.timing_layout.addWidget(self.step_label)
        self.timing_layout.addWidget(self.step_spinbox)

        #Translate Layout
        self.translate_layout, self.translate_spinbox = self.create_parameter_layout()
        self.main_layout.addWidget(self.translate_label)
        self.main_layout.addLayout(self.translate_layout)

        #Rotate Layout
        self.rotate_layout, self.rotate_spinbox = self.create_parameter_layout()
        self.main_layout.addWidget(self.rotate_label)
        self.main_layout.addLayout(self.rotate_layout)

        #Scale Layout
        self.scale_layout, self.scale_spinbox = self.create_parameter_layout()
        self.main_layout.addWidget(self.scale_label)
        self.main_layout.addLayout(self.scale_layout)



    def create_button(self):
        self.confirm_animation_button = QPushButton("Confirm Animation")
        self.main_layout.addWidget(self.confirm_animation_button)
        self.confirm_animation_button.clicked.connect(self.button_clicked)


    def button_clicked(self):
        animate()


    def create_parameter_layout(self):

        layout = QVBoxLayout()
        spinboxes = {}

        for parameter in ["min", "max"]:
            row = QHBoxLayout()

            for axis in ["x", "y", "z"]:
                label = QLabel(f"{parameter} {axis}:")
                spinbox = QSpinBox()

                row.addWidget(label)
                row.addWidget(spinbox)

                spinboxes[f"{parameter}_{axis}"] = spinbox


            layout.addLayout(row)

        return layout, spinboxes



    def create_duration_spinbox(self):
        self.duration_spinbox = QSpinBox()

    def create_step_spinbox(self):
        self.step_spinbox = QSpinBox()

def show_animation_tool():
    global animation_tool
    
    try:
        animation_tool.close()
        animation_tool.deleteLater()
    except:
        pass
    
    animation_tool = AnimationTool()
    animation_tool.show()
show_animation_tool()