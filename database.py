from model.book import Book
from model.lender import Lender
from model.record import Record
from datetime import datetime

class Database():

    def __init__(self):
        self.Books = []
        self.Lenders = []
        self.Records = []
        self.uuid = 1000
        
    def bookExists(self, isbn):
        for i in range(len(self.Books)):
            if self.Books[i].getIsbn() == isbn:
                return i
        return None

    def addBook(self, book):
        isbn = book['isbn']
        author = book['author']
        title = book['title']
        year = book['year']
        no_copies = book['no_copies']
        no_available_copies = book['no_available_copies']
        nuevoLibro = Book(int(isbn), author, title, int(
            year), int(no_copies), int(no_available_copies))
        self.Books.append(nuevoLibro)

    def updateBook(self, book):
        for i in range(len(self.Books)):
            if self.Books[i].getIsbn() == book['isbn']:
                self.Books[i].setIsbn(int(book['isbn']))
                self.Books[i].setAuthor(book['author'])
                self.Books[i].setTitle(book['title'])
                self.Books[i].setYear(int(book['year']))
                return True
        return False

    def getBooks(self):
        Data = []
        for book in self.Books:
            object = {'isbn': book.getIsbn(), 'author': book.getAuthor(), 'title': book.getTitle(), 'year': book.getYear(
            ), 'no_copies': book.getNo_copies(), 'no_available_copies': book.getNo_available_copies()}
            Data.append(object)
        return Data

    def filterByAuthor(self, Data, author):
        filteredData = []
        for i in range(len(Data)):
            book = Data[i]
            if book['author'].lower() == author.lower():
                filteredData.append(book)
        return filteredData

    def filterByTitle(self, Data, title):
        filteredData = []
        for i in range(len(Data)):
            book = Data[i]
            if book['title'].lower() == title.lower():
                filteredData.append(book)
        return filteredData

    def filterByYear(self, Data, year_from, year_to):
        filteredData = []
        for i in range(len(Data)):
            book = Data[i]
            if (book['year'] >= year_from and book['year'] <= year_to):
                filteredData.append(book)
        return filteredData

#####################################
    def borrowedBook(self, lenderPosition):
        if (self.Lenders[lenderPosition].getborrowedBook()):
            return True
        else:
            return False

    def NoAvailableCopies(self, bookPosition):
        if (self.Books[bookPosition].getNo_available_copies() > 0):
            return True
        return False

#####################################
    def lenderExists(self, cui):
        for i in range(len(self.Lenders)):
            if self.Lenders[i].getCui() == cui:
                return i
        return None

    def addLender(self, lender):
        cui = lender['cui']
        last_name = lender['last_name']
        first_name = lender['first_name']
        nuevoPrestamista = Lender(cui, last_name, first_name)
        self.Lenders.append(nuevoPrestamista)

    def getLender(self, cui):
        for lender in self.Lenders:
            if lender.getCui() == cui:
                object = {'cui': lender.getCui(), 'last_name': lender.getLast_name(
                ), 'first_name': lender.getFirst_name(), 'record': lender.getRecord()}
                return object

    def newRecord(self, lenderPosition, bookPosition):
        self.uuid += 1
        lendDate = datetime.today()
        self.Books[bookPosition].setNo_available_copies(
            self.Books[bookPosition].getNo_available_copies() - 1)
        self.Lenders[lenderPosition].setborrowedBook(True)
        self.Lenders[lenderPosition].setRecord(self.uuid, int(
            self.Books[bookPosition].getIsbn()), self.Books[bookPosition].getTitle(), lendDate, None)
        self.Records.append(Record(self.uuid, self.Lenders[lenderPosition].getCui(), int(
            self.Books[bookPosition].getIsbn()), self.Books[bookPosition].getTitle(), lendDate, None))
        return self.uuid

    def recordExists(self, uuid):
        for i in range(len(self.Records)):
            if self.Records[i].getUuid() == uuid:
                return i
        return None

    def returnedDate(self, recordPosition):
        if self.Records[recordPosition].getReturnedDate() == None:
            return True
        return False

    def retunBook(self, recordPosition):
        for positionLender in range(len(self.Lenders)):
            if self.Records[recordPosition].getCui() == self.Lenders[positionLender].getCui():
                self.Records[recordPosition].setReturnedDate(datetime.today())
                self.Lenders[positionLender].setborrowedBook(False)
                length = len(self.Lenders[positionLender].getRecord())
                self.Lenders[positionLender].setRecordSpecific(
                    length-1, self.Records[recordPosition].getReturnedDate())
                break
        for positionBook in range(len(self.Books)):
            if self.Records[recordPosition].getIsbn() == self.Books[positionBook].getIsbn():
                self.Books[positionBook].setNo_available_copies(
                    self.Books[positionBook].getNo_available_copies() + 1)
                break

bankDatabase = Database()