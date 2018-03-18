from tkinter import *
from Import import Import
from Export import Export
from ReadersDialog import ReadersDialog
from AddReaderDialog import AddReaderDialog
from BorrowsDialog import BorrowsDialog


# ----- DROPDOWN MENUS
# ---------- Main menu: File, Readers
# -------------- File menu: Import, Export, Exit
# ------------------ Import menu: Documents, Readers
# ------------------ Export menu: Documents, Readers
# -------------- Readers menu: New, All Readers, Borrows

class DropdownMenus:
    def __init__(self, library, master):
        # MAIN MENU
        menu = Menu(master)
        self.library = library
        self.master = master
        self.master.config(menu=menu)

        # MAIN MENU => FILE MENU
        fileMenu = Menu(menu)

        # MAIN MENU => FILE MENU => IMPORT
        importMenu = Menu(fileMenu)
        importMenu.add_command(label='Dokumentumok', command=self.importDocuments)
        importMenu.add_command(label='Olvasók', command=Import.readers)
        importMenu.add_command(label='Történések', command=Import.events)

        # MAIN MENU => FILE MENU => EXPORT
        exportMenu = Menu(fileMenu)
        exportMenu.add_command(label='Dokumentumok', command=Export.documents)
        exportMenu.add_command(label='Olvasók', command=Export.readers)

        # MAIN MENU => FILE MENU
        fileMenu.add_cascade(label='Import CSV', menu=importMenu)
        fileMenu.add_cascade(label='Export CSV', menu=exportMenu)
        fileMenu.add_separator()
        fileMenu.add_command(label='Kilépés', command=master.destroy)

        # MAIN MENU => READER MENU
        readerMenu = Menu(menu)
        readerMenu.add_command(label='Új olvasó', command=self.addReader)
        readerMenu.add_command(label='Összes olvasó', command=self.listReaders)
        readerMenu.add_command(label='Kölcsönzések', command=self.listBorrows)

        # MAIN MENU OPTIONS
        menu.add_cascade(label='Fájl', menu=fileMenu)
        menu.add_cascade(label='Olvasók', menu=readerMenu)

    def importDocuments(self):
        Import.documents()
        self.library.list.reload()
        
    def addReader(self):
        AddReaderDialog(self.master)

    def listReaders(self):
        ReadersDialog(self.master)

    def listBorrows(self):
        BorrowsDialog(self.master)