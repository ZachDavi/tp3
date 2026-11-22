from maya import cmds
import random
from PySide6.QtWidgets import QMessageBox

class Animator():

    def __init__(self, ui):
        self.ui = ui
        
        
    def create_error_window(self):
        QMessageBox.warning(
        self.ui,
        "Erreur",
        "Erreur : la durée doit être divisible par le step.",
    )
        

    def animate(self):
        cmds.undoInfo(openChunk=True)
        self.set_animation_duration()
        self.set_animation_key()

        cmds.undoInfo(closeChunk=True)

    def set_animation_duration(self):
        duration = self.ui.duration_spinbox.value()
        cmds.playbackOptions(minTime=0, maxTime=duration, animationStartTime=0, animationEndTime=duration)

    def set_animation_key(self):
        first_translate_values = None
        first_rotate_values = None
        first_scale_values = None
        step = self.ui.step_spinbox.value()
        duration = self.ui.duration_spinbox.value()
        liste_objet = cmds.ls(selection=True)
        print(f"{duration%step}")

        if (duration % step == 0):
            for selected in liste_objet:
                for i in range(0,duration,step):
                    translate_values = self.axis_parameters(self.ui.translate_spinbox)
                    rotate_values = self.axis_parameters(self.ui.rotate_spinbox)
                    scale_values = self.axis_parameters(self.ui.scale_spinbox)
                    if first_translate_values == None or first_rotate_values == None or first_scale_values == None:
                        first_translate_values = translate_values
                        first_rotate_values = rotate_values
                        first_scale_values = scale_values

                    self.set_keyframe_to_values(selected,'translate',i,translate_values)
                    self.set_keyframe_to_values(selected,'rotate',i,rotate_values)
                    self.set_keyframe_to_values(selected,'scale',i,scale_values)
                self.set_keyframe_to_values(selected,'translate',duration, first_translate_values)
                self.set_keyframe_to_values(selected,'rotate',duration, first_rotate_values)
                self.set_keyframe_to_values(selected,'scale',duration, first_scale_values)
                first_translate_values = None
                first_rotate_values = None
                first_scale_values = None
                        
        else:
            self.create_error_window()
            

    def axis_parameters(self, spinboxes):
        values = {}
        for axis in ["X","Y","Z"]:
            min_value = spinboxes[f"min_{axis}"].value()
            max_value = spinboxes[f"max_{axis}"].value()
            values[axis] = random.uniform(min_value, max_value)
        return values

    def set_keyframe_to_values(self,selection_group,parameter,current_time,value_group):
        parameter_group = {"translate": self.ui.translate_spinbox,"rotate":self.ui.rotate_spinbox,"scale":self.ui.scale_spinbox}
        
        for axis in ["X","Y","Z"]:
            cmds.setKeyframe(selection_group, attribute=f"{parameter}{axis}", time=current_time, value=value_group[axis])

