from tkinter import *
from tkinter import messagebox
from dbinit import session

# ------ DISPLAY DOCUMENTS IN A LIST BY TYPE
# --------- get selected document (getSelected)
# --------- add document function (addVolume)
# --------- remove document function (removeVolume)

class ItemsList:
    def __init__(self, model, library):
        self.listbox = Listbox(library.frame('left'), width=70, height=50)
        self.listbox.pack(fill=Y, expand=True)
        self.library = library
        self.model = model
        self.query = ''
        self.show()

    def listener(self, callback):
        self.listbox.bind('<<ListboxSelect>>', callback)

    def reload(self, query=''):
        self.query = query
        # Empty Items List
        self.empty()
        # Refill Items List
        self.show()

    def empty(self):
        self.listbox.delete(0, END)

    def show(self):
        for item in self.getAll():
            self.listbox.insert(END, item[1])

    def noSelection(self):
        self.selected = None

    def _getSelectedIndex(self):
        try:
            self.selected = int(self.listbox.curselection()[0])
        except:
            pass
        return self.selected

    def getSelected(self):
        try:
            index = self._getSelectedIndex()
            id = self.getAll()[index][0]
            return session.query(self.model).filter(self.model.id==id).first()
        except:
            return self.model()

    def getAll(self):
        # GET ALL READERS
        result = session.query(self.model.id, self.model.title)
        result = result.filter(self.model.code.like('%{0}%'.format(self.query))).all()
        return result

    def addVolume(self):
        self.listbox.selection_clear(0, END)
        self.noSelection()
        self.showDetails()

    def removeVolume(self):
        volume = self.getSelected()
        message = 'Biztosan ki szeretné törölni:\n' + volume.title
        dialog = messagebox.askyesno('Törlés', message, icon='warning')

        if dialog:
            try:
                session.delete(volume)
                session.commit()
                self.library.frame('right')
                self.reload()
            except:
                session.rollback()
                messagebox.showerror('Törlés', 'Kölcsönzött dokumentum nem törölhető.')
