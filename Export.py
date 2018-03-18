import csv
from dbmodels import Reader, Book, Magazine, Medium, Borrow
from dbinit import session
from tkinter import filedialog


# ******** Export data from database to csv

class Export:
    @staticmethod
    def savefile():
        file = filedialog.asksaveasfilename(defaultextension=".csv")
        return file

    @staticmethod
    def write(model, callback, file=None, mode='w', count=None):
        # Open File
        filename = file or Export.savefile()

        with open(filename, mode, newline='', encoding='utf-8') as file:
            # All Readers
            results = session.query(model)
            # CSV Writer
            outcsv = csv.writer(file, delimiter=';')
            # Number of Rows in Total
            count != False and outcsv.writerow(count or [results.count()])
            # Write Rows to File
            [callback(outcsv, row) for row in results.all()]
            # Clode File Handler
            file.close()

        return filename

    @staticmethod
    def readers():
        # EXPORT READERS TABLE
        file = Export.write(Reader, Export._readers)

    @staticmethod
    def documents():
        # TOTAL NUMBER OF DOCUMENTS
        count = sum([session.query(model).count() for model in [Book, Magazine, Medium]])

        # EXPORT ALL DOCUMENT TYPES:
        # books, magazines, media
        file = Export.write(Book, Export._books, count=[count])
        file = Export.write(Magazine, Export._magazines, mode='a', count=False, file=file)
        file = Export.write(Medium, Export._media, mode='a', count=False, file=file)

    @staticmethod
    def _books(outcsv, book):
        outcsv.writerow([
            book.code,
            'K',
            book.title,
            book.value,
            book.author,
            book.publisher,
            book.isbn,
            book.category])

    @staticmethod
    def _magazines(outcsv, magazine):
        outcsv.writerow([
            magazine.code,
            'F',
            magazine.title,
            magazine.value,
            magazine.publisher,
            magazine.issue,
            magazine.volume])

    @staticmethod
    def _media(outcsv, medium):
        if medium.type == 'DIA':
            lengthOrColor = medium.color
        else:
            lengthOrColor = medium.length

        outcsv.writerow([
            medium.code,
            'M',
            medium.type,
            medium.title,
            medium.value,
            medium.release,
            lengthOrColor])

    @staticmethod
    def _readers(outcsv, reader):
        # Number of Borrowed Documents
        count = session.query(Borrow).filter_by(reader_id=reader.id).count()
        # Write Data Row
        outcsv.writerow([reader.code, reader.name, count])
