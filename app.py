import sqlite3
from datetime import datetime
from functools import wraps
from collections import namedtuple

from flask import Flask, render_template, session, redirect, request, url_for, g
app = Flask(__name__)
app.config.from_envvar('APP_SETTINGS')

DATABASE = './data/mms.sqlite'

AccountingEntry = namedtuple('AccountingEntry', 'uid, crdate, amount, date, desc, tags')
Tag = namedtuple('Tag', 'uid, value')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('login', False):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)

    if db is not None:
        db.close()

def get_rows(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()

    return rows


@app.route('/')
@login_required
def index():
    
    query = 'SELECT SUM(amount) FROM accounting_entry WHERE NOT deleted'
    balance=get_rows(query)[0][0]
    
    today = datetime.today()
    first = int(datetime(today.year, today.month, 1).timestamp())
    query = '''SELECT SUM(amount) FROM accounting_entry WHERE 
               amount < 0 AND date >= (?) AND NOT deleted'''
    spending = get_rows(query, (first,))[0][0]
    
    return render_template('index.html', balance=balance, spending=spending)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['passwd'] == app.config['PASSWD']:
            session['login'] = True

            if request.form.get('remember', False):
                session.permanent = True

            return redirect(url_for('index'))

    if session.get('login', False):
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session['login'] = False
    return redirect(url_for('login'))


@app.route('/create/entry', methods=['POST'])
def create_entry():
    crdate = int(datetime.today().timestamp())
    amount = request.form['amount']
    desc = request.form['desc']
    date = int(datetime.strptime(request.form['date'], '%Y-%m-%d').timestamp())

    cur = get_db().cursor()

    query = 'INSERT INTO accounting_entry (crdate, amount, date,  desc) VALUES (?, ?, ?, ?)'

    cur.execute(query, (crdate, amount, date, desc))
    
    entry_uid = get_rows('SELECT last_insert_rowid()')[0][0]

    for tag_uid in [int(uid) for uid in request.form.getlist('tag')]:
        query = 'INSERT INTO tag_mm (uid_local, uid_foreign) VALUES (?,?)'
        cur.execute(query, (tag_uid, entry_uid))
        
    get_db().commit()

    return redirect(url_for('entries'))
    

@app.route('/create/tag', methods=['POST'])
def create_tag():
    tag = request.form['tag']
    
    cur = get_db().cursor()
    
    query = 'INSERT INTO tag (value) VALUES (?)'
    cur.execute(query, (tag,))
    
    get_db().commit()
    
    return redirect(url_for('tags'))

@app.route('/entries')
@login_required
def entries():
    query = '''SELECT uid, crdate, amount, date, desc 
             FROM accounting_entry WHERE NOT DELETED ORDER BY crdate DESC LIMIT 10
            '''

    acc_entries = []

    for row in get_rows(query):
        query = '''SELECT tag.uid, tag.value FROM tag INNER JOIN tag_mm 
                   ON tag.uid=tag_mm.uid_local 
                   AND tag_mm.uid_foreign=(?)'''
        entry_tags = get_rows(query, (row[0],))
        
        entry_tags = [Tag._make(tag) for tag in entry_tags]
        
        acc_entries.append(AccountingEntry._make(row + (entry_tags,)))
    
    return render_template('entries.html', acc_entries=acc_entries)

@app.route('/tags')
@login_required
def tags():
    tags = get_rows('SELECT uid, value FROM tag WHERE NOT DELETED')
    tags = [Tag._make(tag) for tag in tags]
    
    return render_template('tags.html', tags=tags)

