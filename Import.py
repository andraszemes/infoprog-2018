import csv
from dbmodels import Reader, Book, Magazine, Medium, Borrow
from dbinit import session
from tkinter import filedialog, messagebox
from datetime import timedelta, datetime


# ******** Import data from csv

class Import(object):
    # Return records as a list from file
    @staticmethod
    def readcsv(file):
        with open(file, 'r', encoding="utf8") as csvfile:                    # Open CSV file for reading
            reader = csv.reader(csvfile, delimiter=';')     # File reader, defining delimiter character
            next(reader, None)                              # Skip headers
            return [map(str.strip, row) for row in reader]  # Strip whitespaces and save entries

    @staticmethod
    def openfile():
        return filedialog.askopenfilename(
                initialdir  = '/~',
                title       = 'Fájl megnyitása.',
                filetypes   = (('csv files', '*.csv'), ('all files', '*.*')))

    # ----- IMPORT READERS
    @staticmethod
    def readers():
        for row in Import.readcsv(Import.openfile()):
            code, name, *_ = row
            reader = Reader(code=code, name=name)
            try:
                session.merge(reader)
                session.commit()
            except:
                session.rollback()

        messagebox.showinfo('Importálás', 'Adatok beolvasva.')


    # ---- IMPORT EVENTS
    @staticmethod
    def events():
        for row in Import.readcsv(Import.openfile()):
            day, type, readerCode, documentCode, *_ = row

            # Borrow deadline
            deadline = datetime.now().date() + timedelta(days=int(day))

            # Borrowing reader
            reader = session.query(Reader).filter(Reader.code==readerCode).first()

            # Borrowed document
            documents = Import.getDocuments(documentCode)

            # Simulate borrow
            if type == 'KOLCSONZES':
                borrow = Borrow(deadline=deadline, readers=reader, **documents)
                Import.add(borrow)

            # Simulate extend
            if type == 'HOSSZABBITAS':
                borrow = Import.getBorrow(documents, documentCode)
                borrow.deadline = deadline
                borrow.extended = Borrow.extended+1
                Import.add(borrow)

            # Simulate return
            if type == 'VISSZA':
                borrow = Import.getBorrow(documents, documentCode)
                Import.delete(borrow)

        # Simulation complete message
        messagebox.showinfo('Történések', 'Szimuláció kész.')

    @staticmethod
    def add(borrow):
        try:
            session.merge(borrow)
            session.commit()
        except:
            session.rollback()

    @staticmethod
    def delete(borrow):
        try:
            session.delete(borrow)
        except:
            session.rollback()

    @staticmethod
    def getDocuments(documentCode):
        documents = {}
        for model in [Book, Magazine, Medium]:
            documents[model.__tablename__] = session.query(model).filter(model.code==documentCode).first()
        filter(None, documents)
        return documents

    @staticmethod
    def getBorrow(documents, documentCode):
        condition = getattr(Borrow, next(iter(documents))).has(code=documentCode)
        return session.query(Borrow).filter(condition).first()


    # ----- IMPORT DOCUMENTS
    @staticmethod
    def documents():
        for row in Import.readcsv(Import.openfile()):
            code, tag, *params = row

            params = list(params) + [None]*6

            if tag == 'K':
                title, value, author, publisher, isbn, category, *_ = params

                volume = Book(
                        code        = code,
                        title       = title,
                        value       = value,
                        author      = author,
                        publisher   = publisher,
                        isbn        = isbn,
                        category    = category
                    )

            if tag == 'F':
                title, value, publisher, issue, volume, *_ = params
                volume = Magazine(
                        code        = code,
                        title       = title,
                        value       = value,
                        publisher   = publisher,
                        issue       = issue,
                        volume      = volume
                    )

            if tag == 'M':
                type, title, value, release, lengthOrColor, *_ = params
                volume = Medium(
                        code        = code,
                        type        = type,
                        title       = title,
                        value       = value,
                        release     = release,
                        length      = type != 'DIA' and lengthOrColor,
                        color       = type == 'DIA' and lengthOrColor
                    )

            try:
                session.merge(volume)
                session.commit()
            except:
                session.rollback()

        messagebox.showinfo('Importálás', 'Adatok beolvasva.')
