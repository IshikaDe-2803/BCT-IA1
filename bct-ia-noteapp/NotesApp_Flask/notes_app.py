from flask import Flask, render_template, request, redirect, session
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
        check_email = Users.query.filter_by(email=email_id).first()
        if check_email is not None and check_email.password == password1:
            session['email'] = email_id
            success = 'Login SUCCESSFUL'
            return redirect('notes')
        elif check_email is None:
            error = 'Account Doesn\'t Exists'
            return render_template('Login.html', error=error)
        else:
            error = 'Incorrect Login Credentials'
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
            session['email'] = email_id
            new_user = Users(email=email_id, password=password1)
            db.session.add(new_user)
            db.session.commit()
            return render_template('Login.html', signup=True)
        elif check_email is not None:
            error = 'Account Already Exists'
            return render_template('SignUp.html', error=error)
        else:
            error = 'Error: Incorrect Password'
            return render_template('SignUp.html', error=error)

    else:
        return render_template('SignUp.html')


@app.route('/notes', methods=['GET', 'POST'])
def notes():
    username = session['email']
    if request.method == "POST":
        session['notification'] = ""
        title = request.form['title']
        content = request.form['content']
        if 'is-public' in request.form:
            is_public = True
        else :
            is_public = False
        # Check duplicates:
        #     allNotes = Notes.query.filter_by(username=username)
        #     session['notification'] = "Note title entered already exists!"
        #     return redirect('notes')
        createNote = contract.functions.createNote(title, content, is_public).transact({
            'from': '0x9DfC5A23f2B9a4da299Ad4177CE417F670E3D91a'
        })
        allNotes = formatNotes(contract.functions.getAllNotes().call())
        return render_template('notes.html', allNotes=allNotes)
    else:
        allNotes = formatNotes(contract.functions.getAllNotes().call())
        return render_template('notes.html', allNotes=allNotes)


@app.route('/delete', methods=['POST'])
def delete():
    session['notification'] = ""
    noteid = int(request.form['noteid'])
    delNote = contract.functions.deleteNote(noteid).transact({
            'from': '0x9DfC5A23f2B9a4da299Ad4177CE417F670E3D91a'
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



