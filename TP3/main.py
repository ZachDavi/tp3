import importlib

from . import animator, ui

# Recharge les modules à chaque exécution pour prendre en compte les modifications
importlib.reload(animator)
importlib.reload(ui)

#Fait apparaître le tool
def show_animation_tool():
    global animation_tool
    
    try:
        animation_tool.close()
        animation_tool.deleteLater()
    except:
        pass
    
    animation_tool = ui.AnimationTool_UI()
    animation_tool.show()
show_animation_tool()