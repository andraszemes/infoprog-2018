from tkinter import *
from lists import BooksList, MagazinesList, MediaList
from Icon import Icon


# ----- MAIN TOOLBAR
# --------- Search Documents By Code
# --------- Add Document Button
# --------- Remove Document Button
# --------- Switch: books, magazines, media

class Toolbar:
    def __init__(self, library, master):
        self.master = master
        self.library = library

        # TOOLBAR FRAME
        toolbar = Frame(master)
        toolbar.pack(fill=X, padx=2, pady=2)

        # TOOLBAR SEARCH
        # Search Entry Field
        self.searchEntry = Entry(toolbar)
        # Place Search Entry
        self.searchEntry.pack(side=LEFT, fill=Y)
        # Search Button
        Button(toolbar, image=Icon.search, command=self.search).pack(side=LEFT)

        # TOOLBAR BUTTONS
        # Add New Volume Button
        addButton = Button(toolbar, image=Icon.add, command=self.addVolume)
        addButton.pack(side=LEFT)

        # Remove Volume Button
        delButton = Button(toolbar, image=Icon.delete, command=self.removeVolume)
        delButton.pack(side=LEFT)

        # TOOLBAR SWITCH
        self.switch = StringVar(None, 'books')
        self.initRadio(toolbar)
        self.showBooks()

    def search(self):
        self.library.list.reload(self.searchEntry.get())
       
    def initRadio(self, toolbar):
        Radiobutton(toolbar, 
            text='Könyvek',
            variable=self.switch,
            indicatoron=0,
            command=self.showBooks,
            value='books').pack(side=LEFT, fill=Y)

        Radiobutton(toolbar, 
            text='Folyóiratok',
            variable=self.switch,
            indicatoron=0,
            command=self.showMagazines,
            value='magazines').pack(side=LEFT, fill=Y)

        Radiobutton(toolbar, 
            text='Média',
            variable=self.switch,
            indicatoron=0,
            command=self.showMedia,
            value='media').pack(side=LEFT, fill=Y)

    def showBooks(self):
        self.library.list = BooksList(self.library)

    def showMagazines(self):
        self.library.list = MagazinesList(self.library)

    def showMedia(self):
        self.library.list = MediaList(self.library)

    def removeVolume(self):
        self.library.list.removeVolume()

    def addVolume(self):
        self.library.list.addVolume()