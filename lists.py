from ItemsList import ItemsList
from ItemDetails import ItemDetails
from BorrowDetails import BorrowDetails
from dbmodels import Book, Magazine, Medium


class BooksList(ItemsList):
    def __init__(self, library):
        super().__init__(Book, library)
        super().listener(self.showDetails)

    def showDetails(self, event=None):
        frame = self.library.frame('right')
        
        itemDetails = ItemDetails(self, frame)
        itemDetails.heading(row=0, text='Adatlap')
        itemDetails.entry(row=1, key='code', label='Azonosító')
        itemDetails.entry(row=2, key='title', label='Cím')
        itemDetails.entry(row=3, key='value', label='Érték')
        itemDetails.entry(row=4, key='author', label='Szerző')
        itemDetails.entry(row=5, key='publisher', label='Kiadó')
        itemDetails.entry(row=6, key='isbn', label='ISBN')
        itemDetails.entry(row=7, key='category', label='Kategória')
        itemDetails.saveButton(row=8)

        self.borrow = BorrowDetails(self.getSelected(), frame, row=9, maxDays=7, maxExtend=3)


class MagazinesList(ItemsList):
    def __init__(self, library):
        super().__init__(Magazine, library)
        super().listener(self.showDetails)

    def showDetails(self, event=None):
        frame = self.library.frame('right')

        itemDetails = ItemDetails(self, frame)
        itemDetails.heading(row=0, text='Adatlap')
        itemDetails.entry(row=1, key='code', label='Azonosító')
        itemDetails.entry(row=2, key='title', label='Cím')
        itemDetails.entry(row=3, key='value', label='Érték')
        itemDetails.entry(row=4, key='publisher', label='Kiadó')
        itemDetails.entry(row=5, key='issue', label='Lapszám')
        itemDetails.entry(row=6, key='volume', label='Évfolyam')
        itemDetails.saveButton(row=7)

        self.borrow = BorrowDetails(self.getSelected(), frame, row=8, maxDays=5, maxExtend=2)


class MediaList(ItemsList):
    def __init__(self, library):
        super().__init__(Medium, library)
        super().listener(self.showDetails)

    def showDetails(self, event=None):
        disabled = super().getSelected().type=='DIA'
        frame = self.library.frame('right')

        itemDetails = ItemDetails(self, frame)
        itemDetails.heading(row=0, text='Adatlap')
        itemDetails.entry(row=1, key='code', label='Azonosító')
        itemDetails.optionMenu(row=2, key='type', options=('DIA', 'CD', 'DVD'), label='Típus')
        itemDetails.entry(row=3, key='title', label='Cím')
        itemDetails.entry(row=4, key='value', label='Érték')
        itemDetails.entry(row=5, key='release', label='Megjelenés')
        itemDetails.entry(row=6, key='length', label='Hossz', disabled=disabled)
        itemDetails.entry(row=7, key='color', label='Színezettség', disabled=not disabled)
        itemDetails.saveButton(row=8)

        self.borrow = BorrowDetails(self.getSelected(), frame, row=9, maxDays=3, maxExtend=2)