from PySide6.QtWidgets import QWidget,QSpinBox, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from maya import cmds
from .animator import Animator
import maya.OpenMayaUI as omui
from shiboken6 import wrapInstance

#Fait que la window est devant maya en tout temps
def main_maya_window():
    pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(pointer), QWidget)

#Classe intié
class AnimationTool_UI(QWidget):
    def __init__(self):
        super().__init__(main_maya_window())
        self.setWindowTitle("Animation Tool")
        self.setWindowFlags(Qt.Window)
        self.build_ui()
        self.animator = Animator(self)

    #Fonction pour build le ui
    def build_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.create_labels()
        self.create_sub_layout()
        self.add_widgets()
        self.create_button()

    #Crée les sous layout qui seront dans le main layouts
    def create_sub_layout(self):
        self.timing_layout = QHBoxLayout()
        self.translate_parameters_layout = QHBoxLayout()
        self.rotate_parameters_layout = QHBoxLayout()
        self.scale_parameters_layout = QHBoxLayout()

    #Crée les labels
    def create_labels(self):
        self.timing_label = QLabel("Animation Timing")
        self.translate_label = QLabel("Translate Parameters")
        self.rotate_label = QLabel("Rotate Parameters")
        self.scale_label = QLabel("Scale Parameters")
        self.animation_duration_label = QLabel("Durations (Frames): ")
        self.step_label = QLabel("Step (Frames): ")

    #Fonction qui ajoute les widget aux layouts
    def add_widgets(self):

        #Timing Layout (Comment j'aurais pu optimiser plus?)
        self.create_duration_spinbox()
        self.create_step_spinbox()
        self.main_layout.addWidget(self.timing_label)
        self.main_layout.addLayout(self.timing_layout)
        self.timing_layout.addWidget(self.animation_duration_label)
        self.timing_layout.addWidget(self.duration_spinbox)
        self.timing_layout.addWidget(self.step_label)
        self.timing_layout.addWidget(self.step_spinbox)

        #Ajoute les widget au layout avec les spinbox (Fonction nouvelle que j'expérimente, donné des recommendations pour optimiser/améliorer)
        self.translate_layout, self.translate_spinbox = self.create_widget_layout(self.translate_label) #J'ai du rajouté mon layout et la spinbox = ... parce que ca crashait sinon.
        #Beaucoup d'essaie erreur, j'ai compris qu'il faut que j'intialiste mon layout et ma spinbox pour aller les chercher dans ma fonction 
        self.rotate_layout, self.rotate_spinbox = self.create_widget_layout(self.rotate_label)
        self.scale_layout, self.scale_spinbox = self.create_widget_layout(self.scale_label)

    #Créé le bouton qui confirme
    def create_button(self):
        self.confirm_animation_button = QPushButton("Confirm Animation")
        self.main_layout.addWidget(self.confirm_animation_button)
        self.confirm_animation_button.clicked.connect(self.animator.animate) #Lié a la fonction animate dans le fichier animator.py

    #Fonction qui crée le widget et l'ajoute au layout
    def create_widget_layout(self,label):
        layout, spinbox = self.create_parameter_layout() #Appel la fonction (Si je peux avoir des commentaires sur cette fonction parce que
        #j'ai utiliser beaucoup de resources en ligne pour arriver a ce resultat et je ne sais pas si c'est la facon optimiser de faire)
        self.main_layout.addWidget(label)
        self.main_layout.addLayout(layout)
        return layout,spinbox

    #Fonction qui crée tout les spinbox et label (J'ai essayer de le faire plus condenser possible, mais je ne sais pas comment faire pour faire tout les spinbox : translate,rotate,scale..)
    def create_parameter_layout(self):

        layout = QVBoxLayout() #on set le layout dès le début
        spinboxes = {} #Crée un dictionnaires de spinboxes pour aller get les values plus tard

        for parameter in ["min", "max"]: #Boucle for pour le min et le max 
            ligne = QHBoxLayout() # O fait une ligne pour le min et le max

            for axis in ["X", "Y", "Z"]: #Boucle pour faire le X, le Y et le Z
                label = QLabel(f"{parameter} {axis}:") #Label pouur chaque axe. Ex : minX,maxX
                spinbox = QSpinBox() #On crée une spinbox nommé spinbox

                ligne.addWidget(label) #On ajoute le label a la ligne
                ligne.addWidget(spinbox) #On ajoute la spinbox a la ligne
                spinbox.setRange(-100,100) #La range pour aller dans les négatifs

                spinboxes[f"{parameter}_{axis}"] = spinbox  #On stock notre nouvelle spinbox dans le dictionnaire  dans la boite "parametre_axis" ex : min_X spinboxes pour aller les cherchers après dans animator

            layout.addLayout(ligne) #On ajoute notre ligne au layout vertical

        return layout, spinboxes #Retourne layout et spinboxes sinon on peut pas aller les chercher dans des fonctions autres

    def create_duration_spinbox(self):
        self.duration_spinbox = QSpinBox()
        self.duration_spinbox.setRange(1,2000)

    def create_step_spinbox(self):
        self.step_spinbox = QSpinBox()
        self.step_spinbox.setRange(1,2000)