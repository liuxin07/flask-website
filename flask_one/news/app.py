#!/usr/bin/env python3
import json
import os
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config.update(dict(SQLALCHEMY_DATABASE_URI='mysql://root:@localhost/shiyanlou',SQLALCHEMY_TRACK_MODIFICATIONS=False))
db = SQLAlchemy(app)

class File(db.Model):
    __titlename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category',uselist=False)
    content = db.Column(db.Text)

    def __init__(self,title,created_time,category,content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content


class Category(db.Model):
    __titlename__ = 'categories'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    files = db.relationship('File')

    def __init__(self,name):
        self.name = name

def insert_data():
    java = Category('Java')
    python = Category('Python')
    file1 = File('Hello Java', datetime.utcnow(),
            java, 'File Content -Java is cool!')
    file2 = File('Hello Python', datetime.utcow(),
            python, 'File Content -python is cool!')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()



def get_files():
    filelist = {}
    for filename in os.listdir('/home/shiyanlou/files'):
        with open('/home/shiyanlou/files'+'/'+filename) as f:
            filelist[filename[:-5]]=json.load(f)
    return filelist 

@app.route('/')
def index():
    files = get_files()
    titles = [item['title'] for item in files.values()]
    return render_template('index.html',titles=titles)

@app.route('/files/<filename>')
def file(filename):
    files = get_files()
    file_item = files.get(filename)
    if file_item == None:
            abort(404)
    return render_template('files.html',file_item=file_item)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__=='__main__':
    app.run()
