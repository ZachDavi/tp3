from maya import cmds
import random
from PySide6.QtWidgets import QMessageBox

class Animator():

    def __init__(self, ui):
        self.ui = ui
        
    #Fait apparaître une fenêtre d'erreur si la durée nest pas divisible par le step
    def create_error_window(self):
        QMessageBox.warning(self.ui, "Erreur", "Erreur : la durée doit être divisible par le step.")
        
    #Logique derrière les animations
    def animate(self):
        cmds.undoInfo(openChunk=True)
        try:
            self.set_animation_duration()
            self.set_animation_key()
        finally:
            cmds.undoInfo(closeChunk=True)

    #Met la durée de l'animation
    def set_animation_duration(self):
        duration = self.ui.duration_spinbox.value() #Va chercher la valeur dans la spinbox
        cmds.playbackOptions(minTime=0, maxTime=duration, animationStartTime=0, animationEndTime=duration)

    #Fonction pour set les clés d'animations
    def set_animation_key(self):
        #Set les values à none (je voulais mettre 0, mais vu que desfois la valeur peut être égal a 0)
        first_translate_values = None
        first_rotate_values = None
        first_scale_values = None

        step = self.ui.step_spinbox.value()
        duration = self.ui.duration_spinbox.value()
        liste_objet = cmds.ls(selection=True)

        #Main logic derriere le placement des keys
        if (duration % step == 0):
            for selected in liste_objet: #On regarde dans la liste
                cmds.cutKey(selected,clear = True)
                for i in range(0,duration,step): # Nouveau truc que j'ai trouvé le in range a un debut une fin et un step inclus
                    
                    #Utilise la fonction axis parameters pour get les values des spinbox (Peut être optimisé)
                    translate_values = self.axis_parameters(self.ui.translate_spinbox)
                    rotate_values = self.axis_parameters(self.ui.rotate_spinbox)
                    scale_values = self.axis_parameters(self.ui.scale_spinbox)
                    #Stock la première valeur pour la réutiliser (Peut être opti)
                    if first_translate_values == None or first_rotate_values == None or first_scale_values == None:
                        first_translate_values = translate_values
                        first_rotate_values = rotate_values
                        first_scale_values = scale_values

                    #Met la keyframe
                    self.set_keyframe_to_values(selected,'translate',i,translate_values)
                    self.set_keyframe_to_values(selected,'rotate',i,rotate_values)
                    self.set_keyframe_to_values(selected,'scale',i,scale_values)

                #Met la keyframe avec les valeurs de première frame
                self.set_keyframe_to_values(selected,'translate',duration, first_translate_values)
                self.set_keyframe_to_values(selected,'rotate',duration, first_rotate_values)
                self.set_keyframe_to_values(selected,'scale',duration, first_scale_values)

                #Après ca je reset les valeurs a none pour que si j'ai plusieurs objets ca n'utilise pas ma première valeur
                first_translate_values = None
                first_rotate_values = None
                first_scale_values = None
                        
        else:
            self.create_error_window()
            
    #Fonction qui get les valeurs des spinbox
    def axis_parameters(self, spinbox):
        values = {} #Stock les valeurs dans liste values, méthode que j'ai trouvé pour trouver les valeurs en étant optimisé
        for axis in ["X","Y","Z"]: #For loop pour chaque axe
            min_value = spinbox[f"min_{axis}"].value() #Get la valeur minimum
            max_value = spinbox[f"max_{axis}"].value() #Get la valeur max
            values[axis] = random.uniform(min_value, max_value) #Stock la valeur de chaque axe dans values
        return values

    def set_keyframe_to_values(self,selection_group,parameter,current_time,value_group):        
        for axis in ["X","Y","Z"]:
            cmds.setKeyframe(selection_group, attribute=f"{parameter}{axis}", time=current_time, value=value_group[axis])

