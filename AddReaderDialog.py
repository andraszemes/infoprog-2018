from tkinter import *
from tkinter import ttk, messagebox, simpledialog
from dbmodels import Reader
from dbinit import session


# ------ ADD NEW READER DIALOG
# ---------- Reader Code
# ---------- Reader Full Name

class AddReaderDialog(simpledialog.Dialog):
    def body(self, master):
        # Create and Place Labels
        codeLabel = Label(master, text='Azonosító').grid(row=0)
        nameLabel = Label(master, text='Teljes név').grid(row=1)

        # Create Entry Fields
        self.codeEntry = Entry(master)
        self.nameEntry = Entry(master)

        # Place Entry Fields in Grid
        self.codeEntry.grid(row=0, column=1)
        self.nameEntry.grid(row=1, column=1)
       

    def apply(self):
        try:
            # Create New Reader
            reader = Reader(code=self.codeEntry.get(), name=self.nameEntry.get())
            # Add New Reader to Session
            session.add(reader)
            # Commit Changes
            session.commit()
            # Display Info Message
            messagebox.showinfo('Mentés', 'Új olvasó hozzáadva: ' + reader.name)
        except:
            # Roll Back Session Error
            session.rollback()
            # Display Error Message if ID Already Exists
            messagebox.showerror('Hibajelentés', 'Ez az azonosító már létezik!')