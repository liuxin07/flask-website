#!/usr/bin/env python3
import json
import os
from datetime import datetime
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient


app=Flask(__name__)
app.config.update(dict(SQLALCHEMY_DATABASE_URI='mysql://root:@localhost/shiyanlou',SQLALCHEMY_TRACK_MODIFICATIONS=False))
db = SQLAlchemy(app)
mongo = MongoClient('127.0.0.1', 27017).shiyanlou


class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category')
    content = db.Column(db.Text)

    def __init__(self,title,created_time,category,content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content
        
    
    def add_tag(self, tag_name):
        file_item = mongo.files.find_one({'file_id': self.id})
        if file_item:
            tags = file_item['tags']
            if tag_name not in tags:
                tags.append(tag_name)
            mongo.files.update_one({'file_id': self.id}, {'$set': {'tags':tags}})
        else:
            tags = [tag_name]
            mongo.files.insert_one({'file_id':self.id, 'tags': tags})
        return tags

    def remove_tag(self, tag_name):
        db.files.delete_many(self.tag_name)

    @property
    def tags(self):
        for x in db.files.find():
            return x
        return render_template()

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self,name):
        self.name = name

def insert_data():
    db.create_all()
    java = Category('Java')
    python = Category('Python')
    file1 = File('Hello Java', datetime.utcnow(),
            java, 'File Content -Java is cool!')
    file2 = File('Hello Python', datetime.utcnow(),
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
    return render_template('index.html',files=File.query.all())

@app.route('/files/<int:file_id>')
def file(file_id):
    file_item = File.query.get_or_404(file_id)
    return render_template('file.html',file_item=file_item)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__=='__main__':
    insert_data()
