from flask import Flask, render_template, session, redirect, url_for, request
import utils


app = Flask(__name__)
app.secret_key = "946fc61909983c886d51b76cd5b2859e5701b3f74d5dae1c25678e9fa415536b"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if utils.check_credentials(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials. Try again."
    
    return render_template('index.html')
    

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])


@app.route('/book-manager')
def book_manager():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('book_manager.html', username=session['username'])


@app.route('/user-manager')
def user_manager():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('user_manager.html', username=session['username'])


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
