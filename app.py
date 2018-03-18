from tkinter import *
from Icon import Icon
from DropdownMenus import DropdownMenus
from Toolbar import Toolbar


# ----- MAIN CLASS: main application windows
# -------- Load icons
# -------- Initialize dropdown menus
# -------- Initialize toolbar
# -------- Create left and right frames

class Library:
    def __init__(self, master):
        self.master = master
        self.master.title('Könyvtár')
        self.master.option_add('*tearOff', False)
        self.frames = {
            'left': Frame(master),
            'right': Frame(master)
        }

        # Load Software Icons
        Icon.create()

        # Initialize Dropdown Menus
        DropdownMenus(self, master)

        # Initialize Toolbar
        Toolbar(self, master)

    def frame(self, side):
        # RESET FRAMES
        self.frames['right'].destroy()
        self.frames[side].destroy()

        # CREATE NEW FRAME
        self.frames[side] = Frame(self.master)
        self.frames[side].pack(side=LEFT, fill=Y)

        # -- Set 30px Left and Right Margins on Right Frame
        if side == 'right':
            self.frames[side].config(padx=30)

        # RETURN FRAME
        return self.frames[side]


   
root = Tk()
library = Library(root)
root.mainloop()