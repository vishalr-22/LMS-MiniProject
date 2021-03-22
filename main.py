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
        return render_template('add_book.html',text='New Book added!')
    return render_template('add_book.html')

@app.route('/view_book')
def view_book():
    record = db.fetch_records('Books')
    return render_template('view_book.html', record=record)

