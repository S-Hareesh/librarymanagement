import datetime
import mysql.connector


#databasename=librarydata
#table1=bookdata
try:
    class admin:
        def __init__(self):
            self.mydatabase = mysql.connector.connect(host="localhost", user="root", passwd="yourpassword",
                                                 database="librarydata")
            self.cur = self.mydatabase.cursor()

        def addbook(self):
            bookname=input("Enter The Title Of the book: ").strip()
            author=input("Enter the author of the book: ").strip()
            genre=input("Enter the genre of the book: ").strip()
            query="insert into bookdata values (%s,%s,%s,%s)"
            user=(bookname,author,genre,'available')
            self.cur.execute(query,user)
            self.mydatabase.commit()
            print("Book added sucessfully")
        def updatebook(self):
            booktitle=input("Enter The Title Of the book: ")
            newtitle=input("Enter the new title of the book: ")
            query="select count(bookname) from bookdata where bookname=%s"
            self.cur.execute(query,(booktitle,))
            records=self.cur.fetchall()
            if records[0][0]==0:
                print("No Such Book Exists")
                return False
            query="update bookdata set bookname = %s where bookname=%s"
            self.cur.execute(query,(newtitle,booktitle))
            self.mydatabase.commit()
            print("Book Updated successfully")
        def removebook(self):
            booktitle = input("Enter The Title Of the book: ")
            query = "select count(bookname) from bookdata where bookname=%s"
            self.cur.execute(query,(booktitle,))
            records = self.cur.fetchall()
            if records[0][0] == 0:
                print(f"No Such Book named {booktitle} Exists ")
                return
            query="delete from bookdata where bookname=(%s)"
            self.cur.execute(query,(booktitle,))
            self.mydatabase.commit()
            print("BOOK REMOVED SUCCESSFULLY")
        def addmembers(self,name,passwd):
            x=datetime.datetime.now()
            y=x.strftime("%y-%m-%d")
            query="select count(name) from memberdata where name=%s"
            self.cur.execute(query,(name,))
            result=self.cur.fetchall()
            if result[0][0]>=1:
                print("MEMBER ALREADY EXISTS")
                return
            query="insert into memberdata values (%s,%s,%s)"
            self.cur.execute(query,(y,name,passwd))
            self.mydatabase.commit()
            print("MEMBER ADDED SUCCESSFULLY")
        def displaymembers(self):
            query="Select count(name) from memberdata"
            self.cur.execute(query)
            count=self.cur.fetchall()
            if len(count)==0:
                print("NO MEMBERS EXISTS")
                return
            query = "Select distinct(name),DATEJOINED from memberdata"
            self.cur.execute(query)
            names = self.cur.fetchall()
            count=1
            for name,date in names:
                print(f"Member{count} Name :{name} joined on {date}" )
                count+=1
        def display(self):
            query="Select * from bookdata"
            self.cur.execute(query)
            result=self.cur.fetchall()
            for book in result:
                title,author,genre,status=book
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
                    passwd=input("Enter the passwd: ")
                    self.addmembers(name,passwd)
                elif choice==5:
                    self.display()
                elif choice==6:
                    self.displaymembers()
                elif choice==7:
                    break
                else:
                    print("Invalid Choice")
    class user(admin):
        def borrowbook(self,username):
            bookname=input("Enter the name of the book to be borrowed: ")
            query="select count(bookname) from bookdata where bookname=%s"
            self.cur.execute(query,(bookname,))
            response=self.cur.fetchall()
            if response[0][0]==0:
                return False
            query="insert into borrowedbook values (%s,%s)"
            self.cur.execute(query,(username,bookname))
            query="update bookdata set status='Not available' where bookname=%s"
            self.cur.execute(query, (bookname,))
            self.mydatabase.commit()
            print("BOOK BORROWED SUCCESFULLY")
            return True
        def returnedbook(self,username):
            booknames = input("Enter The Title Of the book: ")
            query="delete from borrowedbook where name=%s and bookname=%s"
            self.cur.execute(query,(username,booknames))
            query = "update bookdata set status='available' where bookname=%s"
            self.cur.execute(query, (booknames,))
            self.mydatabase.commit()
            print("BOOK RETURNED SUCCESFULLY")
        def display(self):
            query="Select * from bookdata where status='available'"
            self.cur.execute(query)
            result=self.cur.fetchall()
            for book in result:
                title,author,genre,status=book
                print(f"Title:{title},author:{author},genre:{genre}")


        def userfeatures(self,username):
            while True:
                print("Library Management System")
                print("1.Borrow Book")
                print("2.return Book")
                print("3.Display All Books")
                print("4.Display All Members")
                print("5.Exit")
                try:
                    choice=int(input("Enter Your Choice: "))
                    if choice==1:
                        if not self.borrowbook(username):
                            print("THIS BOOK IS OUT OF STOCK")
                    elif choice==2:
                        self.returnedbook(username)
                    elif choice==3:
                        self.display()
                    elif choice==4:
                        self.displaymembers()
                    elif choice==5:
                        break
                except ValueError :
                    print("INVALID CHARACTER")

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
        mydatabase = mysql.connector.connect(host="localhost", user="root", passwd="hareesh@21",
                                             database="librarydata")
        cur = mydatabase.cursor()
        query1="select distinct(name),passwd from memberdata where name=%s and passwd=%s"
        cur.execute(query1,(username,password))
        result=cur.fetchall()
        if len(result)==1:
            print("Logged in as user")
            u=user()
            u.userfeatures(username)
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
except Exception as e:
    print(e)




