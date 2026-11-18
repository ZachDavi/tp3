class Animator:

    def __init__(self, ui):
        self.ui = ui

    def animate(self):
        for key, spinbox in self.ui.translate_spinbox.items():
            print(key, spinbox.value())