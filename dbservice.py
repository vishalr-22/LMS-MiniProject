from datetime import datetime
import mysql.connector as mysql
from datetime import datetime,date
from datetime import timedelta

class dbservice:
    def __init__(self):
        self.connector = None
        self.dbcursor = None
        self.connect_database()
        self.create_table()
    
    def connect_database(self):
        self.connector = mysql.connect(host='127.0.0.1', user='root', password='vishal')

        self.dbcursor = self.connector.cursor()
        self.dbcursor.execute('USE library_management_sys')

    def create_table(self):
        self.dbcursor.execute(''' CREATE TABLE IF NOT EXISTS `Books` (
            `Book_ID` INT NOT NULL AUTO_INCREMENT,
            `Title` VARCHAR(40) NOT NULL,
            `Author` VARCHAR(40) NOT NULL,
            `Genre` VARCHAR(20) NOT NULL,
            `Publisher` VARCHAR(40) NOT NULL,
            `Price` FLOAT NOT NULL,
            `Status` TINYINT DEFAULT 2,
            PRIMARY KEY(`Book_ID`)
        );''')

        self.dbcursor.execute(''' CREATE TABLE IF NOT EXISTS `CD` (
            `C_ID` INT NOT NULL AUTO_INCREMENT,
            `Title` VARCHAR(40) NOT NULL,
            `Author` VARCHAR(40) NOT NULL,
            `Genre` VARCHAR(20) NOT NULL,
            `Company` VARCHAR(40) NOT NULL,
            `CD_type` VARCHAR(20) NOT NULL,
            `Price` FLOAT NOT NULL,
            `Status` TINYINT DEFAULT 2,
            PRIMARY KEY(`C_ID`)
        );''')

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS `Magazine`(
            `Magz_ID` INT NOT NULL AUTO_INCREMENT,
            `Title` VARCHAR(40) NOT NULL,
            `Company` VARCHAR(40) NOT NULL,
            `Category` VARCHAR(20) NOT NULL,
            `Price` FLOAT NOT NULL,
            `Release_date` DATE NOT NULL,
            PRIMARY KEY(`Magz_ID`) 
        );''')

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS `Journal`(
            `J_ID` INT NOT NULL AUTO_INCREMENT,
            `Topic` VARCHAR(30) NOT NULL,
            `Year` INT NOT NULL,
            PRIMARY KEY(`J_ID`)
        );''')

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS `Admin`(
            `Admin_Id` INT NOT NULL AUTO_INCREMENT,
            `Username` VARCHAR(25) NOT NULL UNIQUE,
            `Password` VARCHAR(20) NOT NULL,
            PRIMARY KEY(`Admin_Id`)
        );''')

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS `User`(
            `User_Id` INT NOT NULL AUTO_INCREMENT,
            `First_Name` VARCHAR(25) NOT NULL,
            `Last_name` VARCHAR(25),
            `Phone` INT UNIQUE,
            `Email` VARCHAR(40) NOT NULL,
            `Username` VARCHAR(25) NOT NULL UNIQUE,
            `Password` VARCHAR(20) NOT NULL,
            PRIMARY KEY(`User_Id`)
        );''')

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS `User_Issue`(
            `User_Id` INT NOT NULL,
            `Username` VARCHAR(25) NOT NULL,
            `Book_Id` INT NOT NULL,
            `Issue_date` DATE NOT NULL,
            `Due_date` DATE NOT NULL,
            `Extension` INT(2) DEFAULT 0,
            FOREIGN KEY(`Username`) REFERENCES USER(`Username`) ON DELETE CASCADE,
            FOREIGN KEY(`Book_Id`) REFERENCES BOOKS(`Book_ID`) ON DELETE CASCADE
        );''')

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS `User_Issue2`(
            `User_Id` INT NOT NULL,
            `Username` VARCHAR(25) NOT NULL,
            `C_Id` INT NOT NULL,
            `Issue_date` DATE NOT NULL,
            `Due_date` DATE NOT NULL,
            `Extension` INT(2) DEFAULT 0,
            FOREIGN KEY(`Username`) REFERENCES USER(`Username`) ON DELETE CASCADE,
            FOREIGN KEY(`C_Id`) REFERENCES CD(`C_ID`) ON DELETE CASCADE
        );''')

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS `User_Reserve`(
            
            `Username` VARCHAR(25) NOT NULL,
            `Book_Id` INT UNIQUE NOT NULL,
            `Reserve_date` DATE NOT NULL,
            FOREIGN KEY(`Username`) REFERENCES USER(`Username`) ON DELETE CASCADE,
            FOREIGN KEY(`Book_Id`) REFERENCES BOOKS(`Book_Id`) ON DELETE CASCADE
        );''')

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS `User_Reserve2`(
            
            `Username` VARCHAR(25) NOT NULL,
            `Cd_Id` INT UNIQUE NOT NULL,
            `Reserve_date` DATE NOT NULL,
            FOREIGN KEY(`Username`) REFERENCES USER(`Username`) ON DELETE CASCADE,
            FOREIGN KEY(`Cd_Id`) REFERENCES cd(`C_ID`) ON DELETE CASCADE
        );''')

        self.connector.commit()

        
    def signup(self, table_name, input_data):
        keys = list(input_data.keys())
        
        #Preparing Query
        table_data, table_values = '(', ' VALUES ('
        for i, x in enumerate(keys):
            if i != len(keys)-1:
                table_values += f'%({x})s, '
                table_data += f'{x}, '
            else:
                table_values += f'%({x})s)'
                table_data += f'{x})'

        add_query = (f'INSERT INTO {table_name} ' + table_data + table_values)
        print(add_query)

        #Execute Query
        try:
            self.dbcursor.execute(add_query, input_data)
            self.connector.commit()
        except Exception as e:
            print(e)


    
    def signin_user(self, table_name, input_data):
        paswd = input_data["Password"]
        user = input_data["Username"]
        print(paswd)
        #Preparing Query
        pwd = (f"SELECT Username FROM {table_name} WHERE Password = %(paswd)s")
        try:
            self.dbcursor.execute(pwd,{'paswd':paswd})
            records = self.dbcursor.fetchone()
            
            if records == None:
                return 0
            else:
                return 1
        except Exception as e:
            print(e)
        return 0
    
    def resv_book(self, table1, table2, data):
        bookid = data["Book_Id"]
        try:
            select_query = (f'UPDATE {table1} SET Status=1 WHERE Book_Id=%(bookid)s AND status=2')
            self.dbcursor.execute(select_query,{'bookid':bookid})

            username = data["username"]
            date = data["Reserve_date"]
            select_query2 = (f'INSERT INTO {table2} VALUES(%(username)s, %(bookid)s, %(date)s)')
            self.dbcursor.execute(select_query2,{'username':username, 'bookid':bookid, 'date':date})
            
            self.connector.commit()
        except Exception as e:
            print(e)    
    
    def resv_cd(self, table1, table2, data):
        cid = data["Cd_Id"]
        try:
            select_query = (f'UPDATE {table1} SET Status=1 WHERE C_ID=%(cid)s AND status=2')
            self.dbcursor.execute(select_query,{'cid':cid})

            username = data["username"]
            date = data["Reserve_date"]
            select_query2 = (f'INSERT INTO {table2} VALUES(%(username)s, %(cid)s, %(date)s)')
            self.dbcursor.execute(select_query2,{'username':username, 'cid':cid, 'date':date})
            
            self.connector.commit()
        except Exception as e:
            print(e)    
        

    def search_book(self, table_name,title):
        select_query = (f'SELECT * FROM {table_name} WHERE Title=%(title)s AND status=2')

        try:
            self.dbcursor.execute(select_query,{'title':title})
            records = self.dbcursor.fetchone()
        except Exception as e:
            print(e)
        if records == None:
            return 0
        else:
            return records

    def fetch_catalogue(self, table_name, category):

        try:
            select_query = (f'SELECT Id, PName, Price, Stock, Description,Date FROM {table_name} WHERE Category=\'{category}\'')
            print(select_query)
            self.dbcursor.execute(select_query)
            records = self.dbcursor.fetchall()
            return records
        except Exception as e:
            print(e)

    

    def fetch_reserve_date(self, table_name, username):
        select_query = (f'SELECT Reserve_date FROM {table_name} WHERE Username=%(user)s')

        self.dbcursor.execute(select_query,{'user':username})
        records = self.dbcursor.fetchone()
        return records

    def fetch_user_records(self, table_name, username):
        select_query = (f'SELECT First_Name, Phone, Email, Last_name, Username FROM {table_name} WHERE Username=%(user)s')

        try:
            self.dbcursor.execute(select_query,{'user':username})
            records = self.dbcursor.fetchone()
        except Exception as e:
            print(e)
        return records
    
    def fetch_books_records(self, table_name, username):
        select_query = (f'SELECT Books.Book_Id,Title,Author,Genre,Publisher,Price,Issue_date,Due_date FROM books,{table_name} WHERE Books.Book_Id=user_issue.Book_Id AND Username=%(user)s') 
        try:
            self.dbcursor.execute(select_query,{'user':username})
            records = self.dbcursor.fetchall()
        except Exception as e:
            print(e)
        return records
    
    def fetch_cd_records(self, table_name, username):
        select_query = (f'SELECT cd.C_Id,Title,Author,Genre,Company,CD_type,Price,Issue_date,Due_date FROM cd,{table_name} WHERE cd.C_Id=user_issue2.C_Id AND Username=%(user)s') 
        try:
            self.dbcursor.execute(select_query,{'user':username})
            records = self.dbcursor.fetchall()
        except Exception as e:
            print(e)
        return records
    
    def fine_calc(self, table_name, username):
        select_query = (f'SELECT Due_date FROM {table_name} WHERE Username=%(user)s')        
        try:
            self.dbcursor.execute(select_query,{'user':username})
            records = self.dbcursor.fetchall()
        except Exception as e:
            print(e)
        
        lst = []
        for i in records:
            if i[0] < date.today():
                lst.append(5*(i[0]-date.today()).days)
            else:
                lst.append(0)
        return lst
    
    def reserved_book_records(self, table_name, username):
        select_query = (f'SELECT * FROM {table_name} WHERE Username=%(user)s')        
        try:
            self.dbcursor.execute(select_query,{'user':username})
            records = self.dbcursor.fetchall()
        except Exception as e:
            print(e)
        return records

    def signin_admin(self, table_name, input_data):
        paswd = input_data["Password"]
        pwd = (f"SELECT Username FROM {table_name} WHERE Password = %(paswd)s")
        
        try:
            self.dbcursor.execute(pwd,{'paswd':paswd})
            records = self.dbcursor.fetchone()
            if records == None:
                return 0
            else:
                return 1
        except Exception as e:
            print(e)
        return 0


    def add_record(self, table_name, input_data):
        keys = list(input_data.keys())
        
        #Preparing Query
        table_data, table_values = '(', ' VALUES ('
        for i, x in enumerate(keys):
            if i != len(keys)-1:
                table_values += f'%({x})s, '
                table_data += f'{x}, '
            else:
                table_values += f'%({x})s)'
                table_data += f'{x})'

        add_query = (f'INSERT INTO {table_name} ' + table_data + table_values)
        
        #Execute Query
        try:
            self.dbcursor.execute(add_query, input_data)
            self.connector.commit()
        except Exception as e:
            print(e)

    def fetch_records(self, table_name):
        select_query = (f'SELECT * FROM {table_name}')

        try:
            self.dbcursor.execute(select_query)
            records = self.dbcursor.fetchall()
        except Exception as e:
            print(e)
        return records

    def delete_record(self, table_name, title, opt = 0):
        if opt == 0:
            if table_name == 'Journal':
                delete_query = (f"DELETE FROM {table_name} WHERE Topic = %(title)s")
            else:
                delete_query = (f"DELETE FROM {table_name} WHERE Title = %(title)s")
        else:
            if opt == 1:
                delete_query = (f"DELETE FROM {table_name} WHERE Book_Id = %(title)s")
            elif opt == 2:
                delete_query = (f"DELETE FROM {table_name} WHERE C_Id = %(title)s")
        try:
            self.dbcursor.execute(delete_query, {'title':title})
            self.connector.commit()
        except Exception as e:
            print(e)

    def update_record(self, table_name, Id, updated_data, opt):
        set_values = ''

        for i, columns in enumerate(updated_data.keys()):
            if i != len(updated_data.keys())-1:
                set_values += f'{columns} = %({columns})s,'
            else:
                if opt == 1:
                    set_values += f'{columns} = %({columns})s WHERE Book_Id = %(Id)s'
                elif opt == 2:
                    set_values += f'{columns} = %({columns})s WHERE C_Id = %(Id)s'
        
        updated_data['Id'] = Id
        update_query = (f'UPDATE {table_name} SET '+ set_values)
        try:
            self.dbcursor.execute(update_query, updated_data)
            self.connector.commit()
        except Exception as e:
            print(' *** Updation Failed *** \n', e)

    def fetch_column_data(self, table_name, columns, condition_name=None, condition_value=None):
        fetch_query = 'SELECT '

        for i,column in enumerate(columns):
            if i < len(columns)-1:
                fetch_query += f'{column}, '
            else:
                fetch_query += f'{column} FROM {table_name}'
        
        if condition_name != None and condition_value != None:
            fetch_query += f' WHERE {condition_name} = %(condition_value)s'
            try:
                self.dbcursor.execute(fetch_query, {'condition_value': condition_value})
            except Exception as e:
                print(e)
        else:
            try:
                self.dbcursor.execute(fetch_query)
            except Exception as e:
                print(e)
        columns_data = self.dbcursor.fetchall()

        return columns_data

    def get_last_insert_id(self):
        count_query = (f'SELECT last_insert_id()')
        try:
            self.dbcursor.execute(count_query)
            no_records = self.dbcursor.fetchone()
        except Exception as e:
            print(e)
        return no_records[0]
