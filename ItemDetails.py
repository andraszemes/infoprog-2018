from tkinter import *
from tkinter import messagebox
from dbinit import session


# -------- DISPLAY DETAILS OF THE SELECTED ITEM
# ----------- components: entry, option menu, save button, label
# ----------- save changes function (saveDetails)

class ItemDetails:
    def __init__(self, itemsList, frame):
        self.itemsList = itemsList
        self.item = itemsList.getSelected()
        self.frame = frame
        self.entries = {}
        self.entries['type'] = StringVar()
        self.entries['period'] = StringVar()

    def entry(self, label, key, row, disabled=False):
        # Create and Place Label
        self.label(label, row)

        # ENTRY FIELD
        # Entry State: NORMAL or DISABLED
        state = disabled and 'disabled' or 'normal'

        # Create Entry Object
        entry = Entry(self.frame, width=30, state=state)

        # Place Entry Object
        entry.grid(row=row, column=1)

        # If Specified, Fill in Entry Field Text
        value = getattr(self.item, key)
        value and entry.insert(END, value)

        # Save Entry Field
        self.entries[key] = entry

    def optionMenu(self, label, key, options, row):
        # Create and Place Label
        self.label(label, row)

        # Set Selected Option
        try:
            self.entries[key].set(getattr(self.item, key))
        except: pass

        # OPTIONS MENU
        # Create Menu
        menu = OptionMenu(self.frame, self.entries[key], *options, command=self.mediaType)
        # Place Menu
        menu.grid(row=row, column=1, sticky=E+W)

    # Trigger Disabled Status of Color and Length Entries in Media
    def mediaType(self, event):
        try:
            if self.entries['type'].get() == 'DIA':
                self.entries['color'].config(state='normal')
                self.entries['length'].config(state='disabled')
                self.entries['length'].delete(0, END)
            else:
                self.entries['color'].config(state='disabled')
                self.entries['color'].delete(0, END)
                self.entries['length'].config(state='normal')
        except: pass

    def button(self, row, text, command):
        # SAVE BUTTON
        # Create Save Button
        button = Button(
            text=text,
            command=command,
            master=self.frame,
            bg='blue4',
            fg='white')

        # Place Save Button
        button.grid(row=row, columnspan=2, sticky=E)

        return button

    def saveButton(self, row):
        self.button(row, text='Mentés', command=self.saveDetails)

    def label(self, text, row, options={}, sticky=E):
        # Create and Place Label
        Label(self.frame, text=text, **options).grid(row=row, sticky=sticky)

    def heading(self, text ,row):
        self.label(text=text, row=row, sticky=W, options={
            'font': ("Helvetica", 16),
            'fg': 'blue4',
            'height': 2
            })

    def getDetails(self):
        [setattr(self.item, k, v.get() or None) for k, v in self.entries.items()]
        return self.item

    def saveDetails(self):
        try:
            session.merge(self.getDetails())
            session.commit()
            self.itemsList.reload()
            messagebox.showinfo('Mentés', 'Mentés sikeres.')
        except:
            session.rollback()
            messagebox.showinfo('Mentés', 'Hiba lépett fel a mentésnél. Ne használjon ismétlődő azonosítókat.')
