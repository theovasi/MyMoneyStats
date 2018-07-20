import sqlite3
from datetime import datetime

from flask import Flask, render_template, session, redirect, request, url_for, g
app = Flask(__name__)
app.config.from_envvar('APP_SETTINGS')

DATABASE = './data/mms.sqlite'


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

    acc_entries = get_rows('SELECT * FROM accounting_entry WHERE NOT DELETED LIMIT 10')

    return render_template('index.html', acc_entries=acc_entries)


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
	amount = request.form['amount']
	desc = request.form['desc']
	date = int(datetime.strptime(request.form['date'], '%Y-%m-%d').timestamp())
	
	cur = get_db().cursor()

	print(cur.execute('select * from accounting_entry').fetchall())

	query = 'INSERT INTO accounting_entry (amount, date,  desc) VALUES (?, ?, ?)'

	cur.execute(query, (amount, date, desc))
	
	get_db().commit()
	
	return redirect(url_for('index'))

