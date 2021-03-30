from flask import Flask, render_template,request, url_for, redirect, flash
from dbservice import dbservice
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super secret key"

db = dbservice()

def check_update_data(updated_data):
    for key in list(updated_data.keys()):
        if updated_data[key] in ['',' ']:
            removed_value = updated_data.pop(key,'Key Not Found')
    return updated_data

@app.route('/')
def adminpage():
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


