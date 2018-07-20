import sqlite3
from datetime import datetime
from collections import namedtuple

from flask import Flask, render_template, session, redirect, request, url_for, g
app = Flask(__name__)
app.config.from_envvar('APP_SETTINGS')

DATABASE = './data/mms.sqlite'

AccountingEntry = namedtuple('AccountingEntry', 'uid, crdate, amount, date, desc, tags')
Tag = namedtuple('Tag', 'uid, value')

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
def index():
    if not session.get('login', False):
        return redirect(url_for('login'))

    query = '''SELECT uid, crdate, amount, date, desc 
             FROM accounting_entry WHERE NOT DELETED LIMIT 10
            '''

    acc_entries = []

    for row in get_rows(query):
        query = '''SELECT tag.uid, tag.value FROM tag INNER JOIN tag_mm 
                   ON tag.uid=tag_mm.uid_local 
                   AND tag_mm.uid_foreign=(?)'''
        entry_tags = get_rows(query, (row[0],))
        
        entry_tags = [Tag._make(tag) for tag in entry_tags]
        
        acc_entries.append(AccountingEntry._make(row + (entry_tags,)))

    tags = get_rows('SELECT uid, value FROM tag WHERE NOT DELETED')
    tags = [Tag._make(tag) for tag in tags]

    return render_template('index.html', acc_entries=acc_entries, tags=tags)


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

    return redirect(url_for('index'))
    

@app.route('/create/tag', methods=['POST'])
def create_tag():
    tag = request.form['tag']
    
    cur = get_db().cursor()
    
    query = 'INSERT INTO tag (value) VALUES (?)'
    cur.execute(query, (tag,))
    
    get_db().commit()
    
    return redirect(url_for('index'))

