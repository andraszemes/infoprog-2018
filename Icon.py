from tkinter import PhotoImage


# ------- ICON IMAGE IMPORTS

class Icon:
    @classmethod
    def create(cls):
        cls.add = PhotoImage(file='icon/add.png')
        cls.delete = PhotoImage(file='icon/delete.png')
        cls.search = PhotoImage(file='icon/search.png')
        cls.userEdit = PhotoImage(file='icon/user-edit.png')
        cls.userInfo = PhotoImage(file='icon/user-info.png')
        cls.userAdd = PhotoImage(file='icon/user-add.png')
        cls.userRemove = PhotoImage(file='icon/user-remove.png')