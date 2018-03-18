# Installation and Requirements
## Requirements
+ Python 3.1 or newer
+ TKinter
+ SQLAlchemy

## Installation
### Windows
[Download Python 3.6.4 for Windows](https://www.python.org/downloads/release/python-364/)
```
pip3 install SQLAlchemy
```

### Linux
```
apt-get install python3 python3-pip python3-tk
```
```
pip3 install SQLAlchemy
```

## Run Application
```
python(3) app.py
```

# Software Use
## How to import data
Use menu function: **File => Import CSV**
You can import three types of data:
+ *Documents list* [books, magazines, media]
+ *Readers list* [reader id, name]
+ *Event simulation* [borrow, extend lending period, return]
⋅⋅⋅ every event gets executed one by one and the changes are saved to the database

After selecting a csv file, please wait a few seconds for the data to import.

## How to export data
Use menu function: **File => Export CSV**
You can export two types of data:
+ *Documents list* [books, magazines, media]
+ *Readers list* [reader id, name]

## Add Reader
Use menu function: **Readers => New Reader**
Specify **UNIQUE** identification code and full name.

## Delete Reader
Use menu function: **Readers => All Readers**
Use the *search bar* to look up readers by their names.
Delete selected reader by clicking on the remove icon on the dialog's toolbar.

## Display Borrowed Titles
Use menu function: **Readers => Borrows**
The borrow records will be in descending order by their due dates.
Return deadlines that have passed will be highlighted in red.

## Toolbar
The toolbar includes several functions:
+ **Search documents by id**
+ **Add document** [specific category]
+ **Remove selected document**
+ **Switch between document categories** [books, magazines, media]
