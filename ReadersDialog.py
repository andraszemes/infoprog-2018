from ReadersDialogToolbar import ReadersDialogToolbar
from tkinter import ttk, messagebox, simpledialog
from tkinter import *
from dbmodels import Reader
from dbinit import session


class ReadersDialog(simpledialog.Dialog):
    def __init__(self, master):
        Toplevel.__init__(self, master)

        #self.top = Toplevel(master)
        self.reader = StringVar()

        # Create Search Bar
        self.search = ReadersDialogToolbar(
            label='Név',
            master=self,
            reload=self.load,
            searchCommand=self.fill,
            selectedReader=self.selected)

        # Initialize Treeview
        self.load()

    def _selectedId(self):
        return self.tree.item(self.tree.focus())['values'][0]

    def setSelectedReader(self, event):
        self.reader.set(self._selectedId())

    def selected(self):
        return session.query(Reader).filter(Reader.id==self._selectedId()).first()

    def load(self):
        # Show Treeview
        self.treeview()
        # Fill Treeview
        self.fill()

    def show(self):
        # Wait For Window To Close
        self.wm_deiconify()
        self.wait_window()
        # Return Reader ID
        return self.reader.get()

    def ok(self):
        self.destroy()

    def treeview(self):
        # CREATE TREEVIEW
        self.tree = ttk.Treeview(self, columns=('id', 'name'), displaycolumns=('name'))

        # BIND SELECTION CHANGE LISTENER
        self.tree.bind('<<TreeviewSelect>>', self.setSelectedReader)

        # TREEVIEW HEADINGS
        # --- Identifier
        self.tree.heading('#0', text='Azonosító')
        # --- First Name
        self.tree.heading('name', text='Név')

        # DISPLAY TREEVIEW
        self.tree.grid(row=1)

        # CONFIRM BUTTON
        Button(self, text="OK", command=self.ok).grid(row=3, pady=3)

    def fill(self):
        # RESET TREEVIEW
        self.tree.delete(*self.tree.get_children())

        # SEARCH QUERY
        query = self.search.getQuery()

        # GET ALL READERS
        readers = session.query(Reader.id, Reader.code, Reader.name)
        readers = readers.filter(Reader.name.like('%{0}%'.format(query))).all()

        # Insert Readers into Treeview
        if readers:
            for reader in readers:
                self.tree.insert('', 0, text=reader.code, values=(reader.id, reader.name))