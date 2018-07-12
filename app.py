from flask import Flask, render_template, session, redirect, request, url_for
app = Flask(__name__)
app.config.from_envvar('APP_SETTINGS')

@app.route('/')
def index():
    if not session.get('login', False):
        return redirect(url_for('login'))

    return render_template('index.html')


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
    return ''

