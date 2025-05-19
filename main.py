import datetime
import mysql.connector
class admin:
    def __init__(self):
        self.books=[]
        self.members=[]
        self.borrowedbook=[]
    def addbook(self):
        bookname=input("Enter The Title Of the book: ")
        author=input("Enter the author of the book: ")
        genre=input("Enter the genre of the book: ")
        bookdata=[bookname,author,genre]
        self.books.append(bookdata)
        print("Book added sucessfully")
    def updatebook(self):
        booktitle=input("Enter The Title Of the book: ")
        newtitle=input("Enter the new title of the book: ")
        for i,book in enumerate(self.books):
            title,author,genre=book
            if title==booktitle:
                title=newtitle
                self.books[i]=title,author,genre
                print("Book Updated successfully")
                return
        print("No Such Book Exists")
    def removebook(self):
        booktitle = input("Enter The Title Of the book: ")
        for i,book in enumerate(self.books):
            title,author,genre=book
            if title==booktitle:
                self.books.pop(i)
                print("BOOK REMOVED SUCCESSFULLY")
        return False
    def addmembers(self,name):
        x=datetime.datetime.now()
        y=x.strftime("%x")
        self.members.append([name,y])
        print("MEMBER ADDED SUCCESSFULLY")
    def displaymembers(self):
        if len(self.members)==0:
            print("NO MEMBERS EXISTS")
            return
        for i,member in enumerate(self.members):
            name,date=member
            print(f"Member{i+1}:{name}  Datejoined:{date}")
    def display(self):
        for book in self.books:
            title,author,genre=book
            print(f"Title:{title},author:{author},genre:{genre}")

    def adminfeatures(self):
        while True:
            print("Library Management System")
            print("1.Add Book")
            print("2.Update Book")
            print("3.Remove Book")
            print("4.Add Member")
            print("5.Display All Books")
            print("6.Display All Members")
            print("7.Exit")
            choice=int(input("Enter Your Choice: "))
            if choice==1:
                self.addbook()
            elif choice==2:
                self.updatebook()
            elif choice==3:
                self.removebook()
            elif choice==4:
                name = input("Enter the name: ")
                self.addmembers(name)
            elif choice==5:
                self.display()
            elif choice==6:
                self.displaymembers()
            elif choice==7:
                break
            else:
                print("Invalid Choice")
class user(admin):
    def __init__(self):
        super().__init__()
    def borrowbook(self):
        bookname=input("Enter the name of the book to be borrowed: ")
        for i, book in enumerate(self.books):
            title, author, genre = book
            if title == bookname:
                self.borrowedbook.append([title,author,genre])
                self.books.pop(i)
                print("BOOK BORROWED SUCCESFULLY")
    def userfeatures(self):
        while True:
            print("Library Management System")
            print("1.Borrow Book")
            print("2.return Book")
            print("3.Display All Books")
            print("4.Display All Members")
            print("5.Exit")
            choice=int(input("Enter Your Choice: "))
            if choice==1:
                if not self.borrowbook():
                    print("THIS BOOK IS OUT OF STOCK")
            elif choice==2:
                self.addbook()
            elif choice==3:
                self.display()
            elif choice==4:
                self.displaymembers()
            elif choice==5:
                break

def admindetails():
    username=input("Enter the Username: ")
    password=input("Enter your Password: ")
    if username=="admin" and password=="pass":
        print("Logged in as admin")
        a=admin()
        a.adminfeatures()
    else:
        print("INVALID CREDENTIALS")
def userdetails():
    username = input("Enter the Username: ")
    password = input("Enter your Password: ")
    if username == "user" and password == "pass":
        print("Logged in as user")
        u=user()
        u.addmembers(username)
        u.userfeatures()
    else:
        print("INVALID CREDENTIALS")


while True:
    role=input("Enter role (admin/user):")
    if role=="admin":
        admindetails()
    elif role=="user":
        userdetails()
    else:
        print("This role does not exists !Please Enter the Correct Role")




