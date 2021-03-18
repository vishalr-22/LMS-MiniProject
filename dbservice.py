import mysql.connector as mysql

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
            `BookID` INT NOT NULL AUTO_INCREMENT,
            `Book_name` VARCHAR(40) NOT NULL,
            `Author` VARCHAR(40) NOT NULL,
            `Publisher` VARCHAR(40) NOT NULL,
            `Category` VARCHAR(20) NOT NULL,
            `Price` FLOAT NOT NULL,
            `Status` BOOL DEFAULT 1,
            PRIMARY KEY(`BookID`)
            );''')

        self.connector.commit()

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

    def update_record(self, table_name, Id, updated_data):
        set_values = ''

        for i, columns in enumerate(updated_data.keys()):
            if i != len(updated_data.keys())-1:
                set_values += f'{columns} = %({columns})s,'
            else:
                set_values += f'{columns} = %({columns})s WHERE Id = %(Id)s'
        
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
