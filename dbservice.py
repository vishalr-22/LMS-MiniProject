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
        self.connector = mysql.connect(host='127.0.0.1', user='root', password='mysql27')

        self.dbcursor = self.connector.cursor()
        self.dbcursor.execute('USE library')

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
            `User_Id` INT NOT NULL,
            `Username` VARCHAR(25) NOT NULL,
            `Book_Id` INT NOT NULL,
            `Reserve_date` DATE NOT NULL,
            FOREIGN KEY(`Username`) REFERENCES USER(`Username`) ON DELETE CASCADE,
            FOREIGN KEY(`Book_Id`) REFERENCES BOOKS(`Book_Id`) ON DELETE CASCADE
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
        #keys = list(input_data.values())
        paswd = input_data["Password"]
        user = input_data["Username"]
        print(paswd)
        #Preparing Query
        pwd = (f"SELECT Username FROM {table_name} WHERE Password = %(paswd)s")
        #if pwd != NULL:
        # rec = (f"SELECT First_Name, Phone, Email FROM {table_name} WHERE Username = %(user)s")
        try:
            self.dbcursor.execute(pwd,{'paswd':paswd})
            records = self.dbcursor.fetchone()
            
            if records == None:
                return 0
            else:
                return 1
            #self.connector.commit()
        except Exception as e:
            print(e)
        return 0
    
    #mypart

    # def fetch_issued_books(self, table_name, username):
    #     select_query = (f'SELECT Reserve_date FROM {table_name} WHERE Username=%(user)s')

    #     self.dbcursor.execute(select_query,{'user':username})
    #     records = self.dbcursor.fetchone()
    #     print("fjj")
    #     print(records)
    #     return records

    def fetch_reserve_date(self, table_name, username):
        select_query = (f'SELECT Reserve_date FROM {table_name} WHERE Username=%(user)s')

        self.dbcursor.execute(select_query,{'user':username})
        records = self.dbcursor.fetchone()
        print("fjj")
        print(records)
        return records

    def fetch_user_records(self, table_name, username):
        select_query = (f'SELECT First_Name, Phone, Email, Last_name, Username FROM {table_name} WHERE Username=%(user)s')

        self.dbcursor.execute(select_query,{'user':username})
        records = self.dbcursor.fetchone()
        print("fjj")
        print(records)
        return records
    
    def fetch_books_records(self, table_name, username):
        #select_query = (f'SELECT First_Name, Phone, Email FROM {table_name} WHERE Username=%(user)s')
        select_query = (f'SELECT Books.Book_Id,Title,Author,Genre,Publisher,Price,Issue_date,Due_date FROM books,{table_name} WHERE Books.Book_Id=user_issue.Book_Id AND Username=%(user)s') 
        self.dbcursor.execute(select_query,{'user':username})
        records = self.dbcursor.fetchall()
        print("fjj1")
        print(records)
        return records
    
    def fine_calc(self, table_name, username):
        select_query = (f'SELECT Due_date FROM {table_name} WHERE Username=%(user)s')        
        self.dbcursor.execute(select_query,{'user':username})
        records = self.dbcursor.fetchall()
        lst = []
        print(records)
        print(datetime.now())
        for i in records:
            if i[0] < date.today():
                lst.append(5*(i[0]-date.today()).days)
            else:
                lst.append(0)
        print(lst)
        return lst

    def signin_admin(self, table_name, input_data):
        #keys = list(input_data.values())
        paswd = input_data["Password"]
        print(paswd)
        #Preparing Query
        pwd = (f"SELECT Username FROM {table_name} WHERE Password = %(paswd)s")
        #if pwd != NULL:

        try:
            self.dbcursor.execute(pwd,{'paswd':paswd})
            records = self.dbcursor.fetchone()
            if records == None:
                return 0
            else:
                return 1
            #self.connector.commit()
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
        print(add_query)

        #Execute Query
        try:
            self.dbcursor.execute(add_query, input_data)
            self.connector.commit()
        except Exception as e:
            print(e)

    def fetch_records(self, table_name):
        select_query = (f'SELECT * FROM {table_name}')

        self.dbcursor.execute(select_query)
        records = self.dbcursor.fetchall()
        return records

    def delete_record(self, table_name, title, opt = 0):
        if opt == 0:
            if table_name == 'Journal':
                delete_query = (f"DELETE FROM {table_name} WHERE Topic = %(title)s")
                print(delete_query)
            else:
                delete_query = (f"DELETE FROM {table_name} WHERE Title = %(title)s")
                print(delete_query)
        else:
            if opt == 1:
                delete_query = (f"DELETE FROM {table_name} WHERE Book_Id = %(title)s")
            elif opt == 2:
                delete_query = (f"DELETE FROM {table_name} WHERE C_Id = %(title)s")
            print(delete_query)
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
        print(update_query)
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
            print(fetch_query)
            self.dbcursor.execute(fetch_query, {'condition_value': condition_value})
        else:
            self.dbcursor.execute(fetch_query)
        columns_data = self.dbcursor.fetchall()

        return columns_data

    def get_last_insert_id(self):
        count_query = (f'SELECT last_insert_id()')
        
        self.dbcursor.execute(count_query)
        no_records = self.dbcursor.fetchone()
        return no_records[0]
