class Record:

    def __init__(self, uuid, cui, isbn, title, borrowedDate, returnedDate):
        self.uuid = uuid
        self.cui = cui
        self.isbn = isbn
        self.title = title
        self.borrowedDate = borrowedDate
        self.returnedDate = returnedDate
    
    ################METHOD_GET##########################
    def getUuid(self):
        return self.uuid

    def getCui(self):
        return self.cui

    def getIsbn(self):
        return self.isbn
    
    def getTitle(self):
        return self.title

    def getBorrowedDate(self):
        return self.borrowedDate
    
    def getReturnedDate(self):
        return self.returnedDate

    ################METHOD_SET#########################
    def setUuid(self, uuid):
        self.uuid = uuid

    def setCui(self, cui):
        self.cui = cui

    def setIsbn(self, isbn):
        self.isbn = isbn
    
    def setTitle(self, title):
        self.title = title
    
    def setBorrowedDate(self, borrowedDate):
        self.borrowedDate = borrowedDate
    
    def setReturnedDate(self, returnedDate):
        self.returnedDate = returnedDate