from flask import Flask, render_template, request, redirect, url_for,flash,session
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
from static import contract

basedir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder='templates')
app.secret_key = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(
    os.path.join(basedir, 'Data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(120), primary_key=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, email=None, password=None):
        self.email = email
        self.password = password

class Contact(db.Model):
    __tablename__ = 'contact'
    name = db.Column(db.String(120), nullable=False, unique=False)
    email = db.Column(db.String(120), nullable=False, unique=False)
    message = db.Column(db.String(1200), primary_key=True, nullable=False)

    def __init__(self, name=None, email=None, message=None):
        self.name = name
        self.email = email
        self.message = message

@app.route('/')
def index():
    session['email'] = ''
    return render_template('homepage.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email_id = request.form['email']
        password1 = request.form['password']
        
        # Fetch the user's ID using the getUserIdByEmail function from the contract
        user_id = contract.functions.getUserIdByEmail(email_id).call()
        
        if user_id > 0:
            # Fetch the user's data using the getUsers function from the contract
            user_data = contract.functions.getUsers(user_id).call()
            
            user_id, username, stored_password = user_data
            
            # Verify password and perform login logic
            if stored_password == password1:
                session['email'] = email_id
                return redirect(url_for('notes'))  # Redirect to user's notes
            else:
                error = 'Incorrect Login Credentials'
                return render_template('Login.html', error=error)
        else:
            error = 'Account Doesn\'t Exist'
            return render_template('Login.html', error=error)
    else:
        return render_template('Login.html')





@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email_id = request.form['email']
        password1 = request.form['password']
        password_copy = request.form['cpassword']
        check_email = Users.query.filter_by(email=email_id).first()
        if check_email is None and password_copy == password1 and len(password1) > 8:
            createUser = contract.functions.createUser(email_id, password1).transact({
                'from': '0xaED46E104f772d08e01EA06815De22Dacb8341E8'
            })

            # Fetch the user's userId from the contract
            user_id = contract.functions.getUserIdByEmail(email_id).call()

            # Set session data and redirect to user's notes
            session['email'] = email_id
            return redirect(url_for('notes', user_id=user_id))
        elif check_email is not None:
            flash('Account already exists')
        else:
            flash('Error: Incorrect Password or Password Length')
    return render_template('SignUp.html')

@app.route('/notes', methods=['GET', 'POST'])
def notes():

    if 'email' not in session:
        return redirect(url_for('login'))  # Redirect to login if not authenticated

    if 'email' not in session:
        return redirect(url_for('login'))  # Redirect to login if not authenticated

    email = session['email']
    
    # Fetch the user's userId from the contract or database based on the email
    user_id = contract.functions.getUserIdByEmail(email).call()
    username = session['email']
    if request.method == "POST":
        session['notification'] = ""
        title = request.form['title']
        content = request.form['content']
        if 'is-public' in request.form:
            is_public = True
        else:
            is_public = False

        createNote = contract.functions.createNote(title, content, is_public, user_id).transact({
            'from': '0xaED46E104f772d08e01EA06815De22Dacb8341E8'
        })
        allNotes = formatNotes(contract.functions.getAllNotes().call())
        return redirect(url_for('notes', user_id=user_id))
    else:
        user_notes = formatNotes(contract.functions.getUserNotes(user_id).call())
        return render_template('notes.html', allNotes=user_notes)


@app.route('/delete', methods=['POST'])
def delete():
    session['notification'] = ""
    noteid = int(request.form['noteid'])
    delNote = contract.functions.deleteNote(noteid).transact({
            'from': '0xaED46E104f772d08e01EA06815De22Dacb8341E8'
        })
    allNotes = formatNotes(contract.functions.getAllNotes().call())
    return render_template('notes.html', saved=True, allNotes=allNotes)

@app.route('/publicNotes')
def publicNotes():
    publicNotes = formatNotes(contract.functions.getPublicNotes().call()) 
    return render_template('publicNotes.html', allNotes=publicNotes)

def formatNotes(notes):
    allNotes = []
    for note in notes:
        allNotes.append({
            "id": note[0],
            "title": note[1],
            "content": note[2],
            "timestamp": formatDate(note[3]),
            "publicNote": note[4]
        })  
    return allNotes

def formatDate(unix_date):
    return datetime.datetime.fromtimestamp(unix_date)

@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        email_id = request.form['email']
        name1 = request.form['name']
        message1 = request.form['message']
        new_message = Contact(name=name1, email=email_id, message=message1)
        db.session.add(new_message)
        db.session.commit()
        contact = True
        return render_template('homepage.html', contact = contact)
    else:
        return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5002)



