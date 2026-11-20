from maya import cmds
import random


class Animator:

    def __init__(self, ui):
        self.ui = ui

        


    def animate(self):
        cmds.undoInfo(openChunk=True)
        self.set_animation_duration()
        self.set_animation_key()

        cmds.undoInfo(closeChunk=True)


    def set_animation_duration(self):
        duration = self.ui.duration_spinbox.value()

        cmds.playbackOptions(
            minTime=0, maxTime=duration, animationStartTime=0, animationEndTime=duration,
        )

    def set_animation_key(self):
        first_value = None
        step = self.ui.step_spinbox.value()
        duration = self.ui.duration_spinbox.value()
        liste_objet = cmds.ls(selection=True)

        if (duration % step == 0):
            for selected in liste_objet:
                for i in range(0,duration,step):
                    value = random.uniform(-20,20)
                    print(value)

                    if first_value is None:
                        first_value = value

                    cmds.setKeyframe(selected, attribute="translateX", time=i, value=value)
                cmds.setKeyframe(selected, attribute="translateX", time=duration, value=first_value)
                        
        else:
            print("Erreur")