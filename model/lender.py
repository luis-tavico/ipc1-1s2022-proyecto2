class Lender:

    Records = []
    borrowedBook = False

    def __init__(self, cui, last_name, first_name):
        self.cui = cui
        self.last_name = last_name
        self.first_name = first_name

    ################METHOD_GET##########################
    def getCui(self):
        return self.cui

    def getLast_name(self):
        return self.last_name

    def getFirst_name(self):
        return self.first_name

    def getRecord(self):
        return self.Records

    def getRecordSpecific(self, i):
        return self.Records[i]

    def getborrowedBook(self):
        return self.borrowedBook

    ################METHOD_SET#########################
    def setCui(self, cui):
        self.cui = cui

    def setLast_name(self, last_name):
        self.last_name = last_name

    def setFirst_name(self, first_name):
        self.first_name = first_name

    def setRecord(self, uuid, isbn, title, borrowedDate, returnedDate):
        object = {'uuid': uuid, 'isbn': isbn, 'title': title,
                  'lend_date': borrowedDate, 'return_date': returnedDate}
        self.Records.append(object)

    def setRecordSpecific(self, i, returnedDate):
        self.Records[i]['return_date'] = returnedDate
        
    def setborrowedBook(self, borrowedBook):
        self.borrowedBook = borrowedBook
