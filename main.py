from flask import Flask, render_template, request, url_for, redirect, flash
from dbservice import dbservice
from datetime import datetime
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "super secret key"

db = dbservice()

def check_update_data(updated_data):
    for key in list(updated_data.keys()):
        if updated_data[key] in ['',' ']:
            removed_value = updated_data.pop(key,'Key Not Found')
    return updated_data

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        table = 'User'
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        phoneno = request.form.get('phoneno')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        data = {'First_Name':fname ,'Last_Name':lname,'Phone':phoneno,'email':email,'Username':username,'Password':password}
        db.signup(table, data)
        return render_template('signin.html',text='Signup Successfull!')
    return render_template('signup.html')

@app.route('/signin_user',methods=['POST','GET'])
def signin_user():
    if request.method=='POST':
        table = 'User'
        username = request.form.get('username')
        upassword = request.form.get('upassword')
        data = {'Username':username ,'Password':upassword}
        val= db.signin_admin(table, data)
        if val == 1:
            record = db.fetch_user_records(table,username)
            rec = db.fetch_books_records('user_issue',username)
            fine = db.fine_calc('user_issue', username)
            res_book = db.reserved_book_records('user_reserve',username)
            rec2 = db.fetch_cd_records('user_issue2',username)
            fine2 = db.fine_calc('user_issue2', username)
            res_cd = db.reserved_book_records('user_reserve2',username)
            return render_template('studentdashboard.html',record=record,rec=rec,rec2=fine ,res_date='hello',rec3=res_book,rec4=rec2,rec5=fine2,rec6=res_cd)
        else:
            return render_template('signin.html',text='Invalid Credentials!')
    return render_template('signin.html')

@app.route('/signin_admin',methods=['POST','GET'])
def signin_admin():
    if request.method=='POST':
        table = 'Admin'
        adminname = request.form.get('adminname')
        apassword = request.form.get('apassword')
        data = {'Username':adminname ,'Password':apassword}
        val = db.signin_admin(table, data)
        if val == 1:
            return render_template('adminpage.html')
        else:
            return render_template('signin.html',text='Invalid Credentials!')
    return render_template('signin.html')

@app.route('/studentdashboard',methods=['POST','GET'])
def studentdashboard():
    return render_template('studentdashboard.html')

@app.route('/display2', methods = ['POST', 'GET'])
def display2():
    cat1 = db.fetch_records('books')
    cat2 = db.fetch_records('Cd')
    cat3 = db.fetch_records('magazine')
    cat4 = db.fetch_records('journal')

    return render_template('display.html', record1=cat1, record2=cat2, record3=cat3, record4=cat4)

@app.route('/renew/<id>', methods = ['POST', 'GET'])
def renew(id):
    table = 'User_issue'
    table2 = 'User'
    data = db.fetch_column_data(table, ['Due_date', 'Extension'], condition_name = 'Book_id', condition_value = id)
    date = data[0][0]
    extension = data[0][1]
    usernamet = db.fetch_column_data('User_issue', ['username'], condition_name = 'Book_Id', condition_value = id)
    username = usernamet[0][0]
    if extension == 0:
        new_date = date + timedelta(days = 7)
        db.update_record(table, Id = id, updated_data = {'Due_date': new_date, 'Extension': 1}, opt = 1)
    record = db.fetch_user_records(table2, username)
    rec = db.fetch_books_records(table, username)
    fine = db.fine_calc(table, username)
    res_book = db.reserved_book_records('user_reserve',username)
    rec2 = db.fetch_cd_records('user_issue2',username)
    fine2 = db.fine_calc('user_issue2', username)
    res_cd = db.reserved_book_records('user_reserve2',username)
    if extension == 0: 
        return render_template('studentdashboard.html',record=record,rec=rec,rec2=fine ,res_date='hello',rec3=res_book,rec4=rec2,rec5=fine2,rec6=res_cd)
    else:
        flash('You have already renewed your book for one time !')
        return render_template('studentdashboard.html', record=record,rec=rec,rec2=fine ,res_date='hello',rec3=res_book,rec4=rec2,rec5=fine2,rec6=res_cd)

@app.route('/reserve1',methods=['POST','GET'])
def reserve1():
    if request.method=='POST':
        
        return render_template('reserve.html',text1='',text2='',rec=[])
    return render_template('reserve.html')

@app.route('/resv_book',methods=['POST','GET'])
def resv_book():
    if request.method=='POST':
        table1 = 'books'
        table2 = 'user_reserve'
        username = request.form.get('username')
        bookid = request.form.get('bookid')
        date = request.form.get('date')
        data = {'username':username, 'Book_Id':bookid, 'Reserve_date':date }
        status = db.fetch_column_data('books', ['Status'], condition_name='Book_ID', condition_value=bookid)
        db.resv_book(table1,table2, data)
        if status[0][0] == 0:
            return render_template('reserve.html',text1='Book is already issued by someone !')
        elif status[0][0] == 1:
            return render_template('reserve.html',text1='Book is already reserved by someone !')
        else:
            db.update_record(table1, Id = bookid, updated_data = {'Status': 1}, opt = 1)
            return render_template('reserve.html',text1='Reserve Successful')
    return render_template('reserve.html')

@app.route('/resv_cd',methods=['POST','GET'])
def resv_cd():
    if request.method=='POST':
        table1 = 'cd'
        table2 = 'user_reserve2'
        username = request.form.get('username')
        cid = request.form.get('cdid')
        date = request.form.get('date')
        data = {'username':username, 'Cd_Id':cid, 'Reserve_date':date }
        db.resv_cd(table1,table2, data)
        status = db.fetch_column_data('Cd', ['Status'],'C_ID', cid)
        if status[0][0] == 0:
            return render_template('reserve.html',text1='CD is already issued by someone !')
        elif status[0][0] == 1:
            return render_template('reserve.html',text1='CD is already reserved by someone !')
        else:
            db.update_record(table1, Id = cid, updated_data = {'Status': 1}, opt = 2)
            return render_template('reserve.html',text1='Reserve Successful')
    return render_template('reserve.html')

@app.route('/search_book',methods=['POST','GET'])
def search_book():
    if request.method=='POST':
        table = 'books'
        bookname = request.form.get('bookname')
        records = db.search_book(table, bookname)
        if records == 0:
            return render_template('reserve.html',text2='Book Not Available')
        else:
            return render_template('reserve.html',rec=records)
    return render_template('reserve.html')

@app.route('/search_cd',methods=['POST','GET'])
def search_cd():
    if request.method=='POST':
        table = 'cd'
        cdname = request.form.get('cdname')
        records = db.search_book(table, cdname)
        if records == 0:
            return render_template('reserve.html',text2='Book Not Available')
        else:
            return render_template('reserve.html',rec2=records)
    return render_template('reserve.html')

@app.route('/adminpage',methods=['POST','GET'])
def adminpage():
    if request.method=='POST':
        return render_template('adminpage.html')
    return render_template('adminpage.html')

@app.route('/add_book',methods=['POST','GET'])
def add_book():
    if request.method=='POST':
        table = 'Books'
        title = request.form.get('title')
        author = request.form.get('author')
        publisher = request.form.get('publisher')
        genre = request.form.get('genre')
        price = request.form.get('price')
        data = {'Title':title, 'Author':author, 'Publisher':publisher, 'Genre':genre, 'Price':price}
        db.add_record(table, data)
        return render_template('add_option.html',text='New Book added!')
    else:
        genres = db.fetch_column_data('Genres',['Id', 'Genre'])
        return render_template('add_option.html', genres = genres)

@app.route('/add_cd',methods=['POST','GET'])
def add_cd():
    if request.method=='POST':
        table = 'CD'
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        company = request.form.get('company')
        ctype = request.form.get('ctype')
        price = request.form.get('price')
        data = {'Title':title, 'Author':author, 'Genre':genre, 'Company':company, 'CD_type':ctype, 'Price':price}
        db.add_record(table, data)
        return render_template('add_option.html', text='New CD added!')
    else:
        genres = db.fetch_column_data('Genres',['Id', 'Genre'])
        return render_template('add_option.html', genres = genres)

@app.route('/add_magz',methods=['POST','GET'])
def add_magz():
    if request.method=='POST':
        table = 'Magazine'
        title = request.form.get('title')
        company = request.form.get('company')
        category = request.form.get('category')
        rdate = request.form.get('date')
        price = request.form.get('price')
        data = {'Title':title, 'Company':company, 'Category':category, 'Price':price, 'Release_date':rdate}
        db.add_record(table, data)
        return render_template('add_option.html', text='New Magazine added!')
    return render_template('add_option.html')

@app.route('/add_journal',methods=['POST','GET'])
def add_journal():
    if request.method=='POST':
        table = 'Journal'
        topic = request.form.get('topic')
        year = request.form.get('year')
        data = {'Topic':topic, 'Year':year}
        db.add_record(table, data)
        return render_template('add_option.html', text='New Journal added!')
    return render_template('add_option.html')

@app.route('/delete_book',methods=['POST','GET'])
def delete_book():
    if request.method=='POST':
        table = 'Books'
        id = request.form.get('id')
        title = request.form.get('title')
        db.delete_record(table, id, opt = 1)
        return render_template('delete_option.html', text='Book deleted successfully!')
    return render_template('delete_option.html')

@app.route('/delete_cd',methods=['POST','GET'])
def delete_cd():
    if request.method=='POST':
        table = 'CD'
        id = request.form.get('id')
        db.delete_record(table, id, opt = 2)
        return render_template('delete_option.html', text='CD deleted successfully!')
    return render_template('delete_option.html')

@app.route('/delete_magz',methods=['POST','GET'])
def delete_magz():
    if request.method=='POST':
        table = 'Magazine'
        id = request.form.get('id')
        db.delete_record(table, id)
        return render_template('delete_option.html', text='Magazine deleted successfully!')
    return render_template('delete_option.html')

@app.route('/delete_journal',methods=['POST','GET'])
def delete_journal():
    if request.method=='POST':
        table = 'Journal'
        id = request.form.get('id')
        db.delete_record(table, id)
        return render_template('delete_option.html', text='Journal deleted successfully!')
    return render_template('delete_option.html')

@app.route('/display/<title>')
def display(title):
    record = db.fetch_records(title)
    if title == 'Books':
        return render_template('view_book.html', record=record)
    elif title == 'CD':
        return render_template('view_cd.html', record=record)
    elif title == 'Magazine':
        return render_template('view_magz.html', record=record)
    elif title == 'Journal':
        return render_template('view_journal.html', record=record)

@app.route('/issue_book', methods=['POST', 'GET'])
def issue_book():
    if request.method=='POST':
        table = 'User'
        table2 = 'Books'
        username = request.form.get('username')
        bookid = request.form.get('bookid')
        issue_date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        due_date = datetime.now() + timedelta(days = 10)
        user = db.fetch_column_data(table, ['User_Id', 'Username'], condition_name = 'Username', condition_value = username)
        book = db.fetch_column_data(table2, ['Status'], condition_name = 'Book_Id', condition_value = bookid)
        nob = db.count_records('User_issue', user[0][0])
        print(nob[0])
        if book[0][0] == 2 and nob[0] < 4:
            data = {'User_Id': user[0][0], 'Username': user[0][1], 'Book_Id': bookid, 'Issue_date': issue_date, 'Due_date': due_date}
            db.add_record('User_Issue', data)
            db.update_record(table2, Id = bookid, updated_data = {'Status': 0}, opt = 1)
            return render_template('issue.html', text = 'Book issued successfully...')
        else:
            if book[0][0] == 0:
                return render_template('issue.html', text = 'Book is already issued to someone !')
            elif book[0][0] == 1:
                return render_template('issue.html', text = 'Book is reserved by someone !')
            elif nob[0] >= 4:
                return render_template('issue.html', text = 'User already has four books issued !')
    return render_template('issue.html')

@app.route('/issue_cd', methods=['POST', 'GET'])
def issue_cd():
    if request.method=='POST':
        table = 'User'
        table2 = 'CD'
        username = request.form.get('username')
        cdid = request.form.get('cdid')
        issue_date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        due_date = datetime.now() + timedelta(days = 10)
        user = db.fetch_column_data(table, ['User_Id', 'Username'], condition_name = 'Username', condition_value = username)
        cd = db.fetch_column_data(table2, ['Status'], condition_name = 'C_ID', condition_value = cdid)
        noc = db.count_records('User_issue2', user[0][0])
        if cd[0][0] == 1 and noc[0] < 2:
            data = {'User_Id': user[0][0], 'Username': user[0][1], 'C_ID': cdid, 'Issue_date': issue_date, 'Due_date': due_date}
            db.add_record('User_Issue2', data)
            db.update_record(table2, Id = cdid, updated_data = {'Status': 0}, opt = 2)
            return render_template('issue.html', text = 'CD issued successfully...')
        else:
            if cd[0][0] == 0:
                return render_template('issue.html', text = 'CD is already issued to someone !')
            elif cd[0][0] == 1:
                return render_template('issue.html', text = 'CD is reserved by someone !')
            elif noc[0] >= 1:
                return render_template('issue.html', text = 'User already has one CD issued !')
    return render_template('issue.html')

@app.route('/return_book', methods=['POST', 'GET'])
def return_book():
    if request.method=='POST':
        table = 'Books'
        bookid = request.form.get('bookid')
        book = db.fetch_column_data(table, ['Status'], condition_name = 'Book_Id', condition_value = bookid)
        if book[0][0] == 0:
            db.delete_record('User_Issue', bookid, opt = 1)
            db.update_record(table, Id = bookid, updated_data = {'Status': 2}, opt = 1)
            return render_template('return.html', text = 'Book returned successfully...')
        else:
            return render_template('return.html', text = 'Book is not issued to anyone !')
    return render_template('return.html')

@app.route('/return_cd', methods=['POST', 'GET'])
def return_cd():
    if request.method=='POST':
        table = 'CD'
        cdid = request.form.get('cdid')
        cd = db.fetch_column_data(table, ['Status'], condition_name = 'C_ID', condition_value = cdid)
        if cd[0][0] == 0:
            db.delete_record('User_Issue2', cdid, opt = 2)
            db.update_record(table, Id = cdid, updated_data = {'Status': 2}, opt = 2)
            return render_template('return.html', text = 'CD returned successfully...')
        else:
            return render_template('return.html', text = 'CD is not issued to anyone !')
    return render_template('return.html')