#!/usr/bin/env python3
import json
import os
from flask import Flask,render_template

app=Flask(__name__)

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
    for filename in files.get(filename):
        if filename == None;
            abort(404)
    return render_template('files.html',filename=filename)

def not_found(error):
    return render_template('404.html'), 404

if __name__=='__main__':
    app.run()
