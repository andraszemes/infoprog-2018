from ItemDetails import ItemDetails
from tkinter import Button, messagebox, StringVar, W, E
from dbinit import session
from datetime import timedelta, datetime
from dbmodels import Borrow, Reader
from ReadersDialog import ReadersDialog


# ------ DOCUMENT BORROW SECTION
# ------ Details:
# --------- Borrower
# --------- Lending Period
# --------- Borrow, Extend, Return Buttons

class BorrowDetails(ItemDetails):
    def __init__(self, item, frame, row, maxDays, maxExtend):
        self.frame = frame
        self.maxDays = maxDays
        self.maxExtend = maxExtend
        self.item = item
        self.row = row
        self.reader = None
        self.entries = {}
        self.buttons = []
        self.entries['period'] = StringVar()
        self.heading(row=row, text='Kölcsönzés')
        self.borrowerField(row=self.row+1)
        self.selectPeriod()

        if self.get():
            self.extendButton()
        else:
            self.borrowButton()

    def selectPeriod(self):
        self.optionMenu(row=self.row+2, key='period', label='Kölcsönzési napok', options=range(1, self.maxDays+1))

    def buttonReset(self):
        # RESET BUTTONS
        [button.grid_forget() for button in self.buttons]
        self.buttons.clear()
            
    def borrowButton(self):
        self.buttonReset()
        # Create and Place Borrow Button
        self.buttons.append(self.button(self.row+3, 'Kölcsönzés', command=self.borrow))

    def extendButton(self):
        self.buttonReset()
        # Create and Place Extend Button
        self.buttons.append(self.button(self.row+3, 'Hosszabbítás', command=self.extend))
        # Create and Place Return Button
        self.buttons.append(self.button(self.row+4, 'Visszatérítés', command=self.returnItem))

    def borrowerField(self, row):
        # Create and Place Label
        self.label('Olvasó', row=row)

        # Fetch Borrower's Name
        try:
            borrower = self.get().readers.name
        except:
            borrower = '...'

        # CHOOSE BORROWER FIELD
        # Create Borrower Field
        self.borrower = Button(
            master=self.frame,
            text=borrower,
            command=self.select)

        # Place Borrower Field
        self.borrower.grid(row=row, column=1, sticky=W+E)

    def get(self):
        # Return Current Item's Borrow Record
        table = getattr(Borrow, self.item.__tablename__)
        return session.query(Borrow).filter(table.has(id=self.item.id)).join(Reader).first()

    def getDeadline(self):
        # RETURN DEADLINE DATE:
        # Current Date + Days to Borrow
        # If Extending: Date = Deadline on Record
        days = int(self.entries['period'].get() or 0)
        date = self.get().deadline if self.get() else datetime.now().date()

        return date + timedelta(days=days)

    def extend(self):
        # CURRENT ITEM'S BORROW RECORD
        borrow = self.get()
        period = self.entries['period']

        # UPDATE BORROW RECORD
        # Increase Extended Counter
        # Update BorrowDeadline
        update = Borrow(id=borrow.id, deadline=self.getDeadline(), extended=Borrow.extended+1)

        # Check If Maximum Number of Extensions Has Been Reached
        if borrow.extended <= self.maxExtend + 1:
            # Check If Lending Period Has Been Set
            if period.get():
                # Insert Data To DB
                session.merge(update)
                session.commit()
                messagebox.showinfo('Hosszabbítás', 'Sikeresen meghosszabbítva')
        else:
            messagebox.showwarning('Hosszabbítás', 'A kölcsönzés többet nem hosszabbítható.')

        # RESET SELECT PERIOD FIELD
        period.set('')

    def returnItem(self):
        # Remove Returned Item from Borrows List
        self.delete()

        # Reset Fields
        self.borrowButton()
        self.borrowerField(self.row+1)
        self.entries['period'].set('')

    def delete(self):
        # Remove Returned Item from Borrows List
        item = self.get()
        item and session.delete(item)
        session.commit()
        
    def borrow(self):
        # Delete Old Borrow
        self.delete()

        # Create New Borrow Record
        borrow = Borrow(readers=self.reader, deadline=self.getDeadline())

        # Set Borrowed Item
        setattr(borrow, self.item.__tablename__, self.item)

        # Number of Borrowed Items
        count = session.query(Borrow).filter_by(reader_id=self.reader.id).count()

        # Check If Number of Borrowed Items Less Than 5
        if count < 5:
            if self.reader:
                # Insert Data To DB
                session.merge(borrow)
                session.commit()
                self.extendButton() # Reset

            messagebox.showinfo('Kölcsönzés', 'Kikölcsönözve.')
        else:
            messagebox.showerror('Kölcsönzés', 'A maxiumum kölcsönözhető dokumentumok meghaladva.')

        # RESET SELECT PERIOD FIELD
        self.entries['period'].set('')

    def select(self):
        # Fetch Reader ID From Dialog
        readerId = ReadersDialog(self.frame).show()
        # Fetch Reader By ID
        self.reader = session.query(Reader).get(readerId)
        # Set Reader Name On Button
        self.borrower.config(text=self.reader.name)
        # Reset
        self.borrowButton()