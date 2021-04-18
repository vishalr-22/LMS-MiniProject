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
    # if request.method=='POST':
    #     return render_template('homepage.html')
    return render_template('homepage.html')
#mypart

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
            # res_date = db.fetch_issued_books('')
            fine = db.fine_calc('user_issue', username)
            return render_template('studentdashboard.html',record=record,rec=rec,rec2=fine ,res_date='hello')
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
#mypart

@app.route('/studentdashboard',methods=['POST','GET'])
def studentdashboard():
    if request.method=='POST':
        
        return render_template('studentdashboard.html')
    return render_template('studentdashboard.html')


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
    return render_template('add_option.html')

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
    return render_template('add_option.html')

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
        title = request.form.get('title')
        db.delete_record(table, title)
        return render_template('delete_option.html', text='Book deleted successfully!')
    return render_template('delete_option.html')

@app.route('/delete_cd',methods=['POST','GET'])
def delete_cd():
    if request.method=='POST':
        table = 'CD'
        title = request.form.get('title')
        db.delete_record(table, title)
        return render_template('delete_option.html', text='CD deleted successfully!')
    return render_template('delete_option.html')

@app.route('/delete_magz',methods=['POST','GET'])
def delete_magz():
    if request.method=='POST':
        table = 'Magazine'
        title = request.form.get('title')
        db.delete_record(table, title)
        return render_template('delete_option.html', text='Magazine deleted successfully!')
    return render_template('delete_option.html')

@app.route('/delete_journal',methods=['POST','GET'])
def delete_journal():
    if request.method=='POST':
        table = 'Journal'
        topic = request.form.get('topic')
        db.delete_record(table, topic)
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

@app.route('/issue', methods=['POST', 'GET'])
def issue():
    if request.method=='POST':
        table = 'User'
        table2 = 'Books'
        username = request.form.get('username')
        title = request.form.get('title')
        issue_date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        due_date = datetime.now() + timedelta(days = 10)
        user = db.fetch_column_data(table, ['User_Id', 'Username'], condition_name = 'Username', condition_value = username)
        book = db.fetch_column_data(table2, ['Book_Id', 'Title'], condition_name = 'Title', condition_value = title)
        data = {'User_Id': user[0][0], 'Username': user[0][1], 'Book_Id': book[0][0], 'Issue_date': issue_date, 'Due_date': due_date}
        db.add_record('User_Issue', data)
        return render_template('issue.html', text = 'Book issued successfully...')
    return render_template('issue.html')


