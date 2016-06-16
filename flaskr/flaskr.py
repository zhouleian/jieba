# coding=utf-8

#all imports
import sqlite3
import os
from flask import Flask,render_template,redirect,url_for,flash,request,session,g,abort
from contextlib import closing

app = Flask(__name__)
#configuration
DATABASE = os.path.join("/home/zhoulei/python_test/flaskr", 'flaskr.db')
#DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'password'

#create our little application
#app.config.from_envvar('FLASKR_SETTINGS',silent = True)
app.config.from_object(__name__)



def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    return rv

def init_db():
    """Initializes the database."""
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql',mode = 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()

#请求之前初始化连接，请求之后关闭连接
@app.before_request
def before_request():
    """Initializes the connection"""
    g.db = connect_db()
@app.teardown_request
def teardown_request(exception):
    """Close the connection"""
    db = getattr(g,'db',None)
    if db is not None:
        db.close()


@app.route('/')
def show_entries():
    cur = g.db.execute('select title,text from entries order by id desc')
    entries = [dict(title = row[0],text = row[1]) for row in cur.fetchall()]
    #entries = cur.fetchall()
    return render_template('show_entries.html',entries = entries)

@app.route('/add',methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title,text) values (?,?)',[request.form['title'],request.form['text']])
    g.db.commit()
    flash("new entry was successfully posted")
    return redirect(url_for("show_entries"))

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
                error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html',error = error)

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()