from datetime import datetime
from tkinter import ttk, messagebox, simpledialog
from tkinter import *
from dbmodels import Borrow
from dbinit import session


# ----- SHOW ALL BORROWED ITEMS IN A DIALOG
# -------- Reader
# -------- Expiration date (red if it has passed)
# -------- Extended

class BorrowsDialog(simpledialog.Dialog):
    def body(self, master):
        # Master Frame
        self.master = master

        # Show Treeview
        self.show(self.master)

        # Fill Treeview
        self.fill()

    def show(self, master):
        # CREATE TREEVIEW
        self.tree = ttk.Treeview(master, columns=('reader', 'deadline', 'extended'))

        # CONFIGURE SPECIAL ROW STYLES
        self.tree.tag_configure('expired', foreground='red')

        # TREEVIEW HEADINGS
        # --- Title
        self.tree.heading('#0', text='Cím')
        # --- Reader Name
        self.tree.heading('reader', text='Olvasó')
        # --- Return Deadline
        self.tree.heading('deadline', text='Lejárat')
        # --- Number of Deadline Postpones
        self.tree.heading('extended', text='Hosszabítások')

        # DISPLAY TREEVIEW
        self.tree.pack()

    def fill(self):
        # RESET TREEVIEW
        self.tree.delete(*self.tree.get_children())

        # GET ALL BORROWS
        borrows  = session.query(Borrow).order_by(Borrow.deadline.desc()).all()

        # INSERT BORROWED ITEMS INTO TREEVIEW
        if borrows:
            for borrow in borrows:
                # --- Borrowed Item Types
                types = [borrow.books, borrow.magazines, borrow.media]

                # --- Determine Borrowed Item Type
                title = next(x for x in types if x is not None).title

                # --- Determine If Borrow Deadline Has Passed
                tags = tuple()
                if borrow.deadline < datetime.now().date():
                    tags = ('expired')

                # --- Display Borrowed Item
                self.tree.insert('', 0, text=title, tags=tags, values=(
                        borrow.readers.name,
                        borrow.deadline,
                        borrow.extended
                    ))