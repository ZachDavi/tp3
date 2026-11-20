import importlib

from . import animator, ui

# Recharge les modules à chaque exécution pour prendre en compte les modifications
importlib.reload(animator)
importlib.reload(ui)



ui.show_animation_tool()