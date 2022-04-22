class Book:

    def __init__(self, isbn, author, title, year, no_copies, no_available_copies):
        self.isbn = isbn
        self.author = author
        self.title = title
        self.year = year
        self.no_copies = no_copies
        self.no_available_copies = no_available_copies

    ################METHOD_GET###########################
    def getIsbn(self):
        return self.isbn

    def getAuthor(self):
        return self.author

    def getTitle(self):
        return self.title

    def getYear(self):
        return self.year

    def getNo_copies(self):
        return self.no_copies

    def getNo_available_copies(self):
        return self.no_available_copies

    #################METHOD_SET##########################
    def setIsbn(self, isbn):
        self.isbn = isbn

    def setAuthor(self, author):
        self.author = author

    def setTitle(self, title):
        self.title = title

    def setYear(self, year):
        self.year = year

    def setNo_copies(self, no_copies):
        self.no_copies = no_copies

    def setNo_available_copies(self, no_available_copies):
        self.no_available_copies = no_available_copies