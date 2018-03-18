from Icon import Icon
from tkinter import *
from dbinit import session
from AddReaderDialog import AddReaderDialog


# ---- TOOLBAR IN READERS DIALOG
# -------- Search Field and Button
# -------- Add Reader Button
# -------- Remove Reader Button

class ReadersDialogToolbar:
    def __init__(self, master, label, reload, searchCommand, selectedReader):
        self.master = master
        self.reload = reload
        self.selectedReader = selectedReader

        # SEARCH BAR FRAME
        frame = Frame(master)
        frame.grid(row=0, sticky=W+E, padx=2, pady=2)
        
        # PLACE SEARCH BAR ITEMS
        self.label(frame, label)
        self.entry(frame)
        self.buttons(frame, searchCommand)
        
    def buttons(self, frame, searchCommand):
        # Search Button
        Button(frame, image=Icon.search, command=searchCommand).pack(side=LEFT)
        # New User Button
        Button(frame, image=Icon.userAdd, command=self.addReader).pack(side=LEFT)
        # Delete User Button
        Button(frame, image=Icon.userRemove, command=self.removeReader).pack(side=LEFT)

    def label(self, frame, label):
        # Place Search Label
        Label(frame, text=label).pack(side=LEFT)

    def entry(self, frame):
        # Place Search Entry Field
        self.search = Entry(frame)
        self.search.pack(side=LEFT, fill=Y)

    def getQuery(self):
        return self.search.get()

    def addReader(self):
        AddReaderDialog(self.master)

    def removeReader(self):
        reader = self.selectedReader() 
        message = 'Biztosan ki szeretné törölni:\n' + reader.name
        dialog = messagebox.askyesno('Törlés', message, icon='warning')

        if dialog:
            try:
                session.delete(reader)
                session.commit()
                self.reload()
            except:
                session.rollback()
                messagebox.showerror('Hiba', 'Ennek az olvasónak még tartozása van.')