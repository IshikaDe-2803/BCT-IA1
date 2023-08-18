from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
from static import contract
import sys

basedir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder='templates')
app.secret_key = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(
    os.path.join(basedir, 'Data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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
        if password_copy == password1 and len(password1) > 8:
            createUser = contract.functions.createUser(email_id, password1).transact({
                'from': '0xa05b6d77321c1229A2B40ca4b357b501eC1F408a'
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

    # print('Hello world!', flush=True)
    if 'email' not in session:
        # Redirect to login if not authenticated
        return redirect(url_for('login'))

    if 'email' not in session:
        # Redirect to login if not authenticated
        return redirect(url_for('login'))

    email = session['email']

    # Fetch the user's userId from the contract or database based on the email
    user_id = contract.functions.getUserIdByEmail(email).call()
    username = session['email']
    # Determine the sort order based on the query parameter
    # Default sorting by timestamp
    sort_order = request.args.get('sort', 'timestamp')
    # print(sort_order)
    if request.method == "POST":
        session['notification'] = ""
        title = request.form['title']
        content = request.form['content']
        if 'is-public' in request.form:
            is_public = True
        else:
            is_public = False

        createNote = contract.functions.createNote(title, content, is_public, user_id).transact({
            'from': '0xa05b6d77321c1229A2B40ca4b357b501eC1F408a'
        })
        allNotes = formatNotes(contract.functions.getAllNotes().call())
        return redirect(url_for('notes', user_id=user_id))
    else:
        user_notes = formatNotes(
            contract.functions.getUserNotes(user_id).call(), sort_order)

        search_query = request.args.get('search', '')
        if search_query:
            # Filter notes based on search query
            user_notes = [
                note for note in user_notes if search_query.lower() in note['title'].lower()]
        no_notes_found = not user_notes
    return render_template('notes.html', allNotes=user_notes, search_query=search_query, no_notes_found=no_notes_found)


@app.route('/delete', methods=['POST'])
def delete():
    session['notification'] = ""
    noteid = int(request.form['noteid'])
    delNote = contract.functions.deleteNote(noteid).transact({
        'from': '0xa05b6d77321c1229A2B40ca4b357b501eC1F408a'
    })

    email = session['email']
    user_id = contract.functions.getUserIdByEmail(email).call()
    user_notes = formatNotes(contract.functions.getUserNotes(user_id).call())
    return render_template('notes.html', allNotes=user_notes)


@app.route('/publicNotes')
def publicNotes():
    publicNotes = formatNotes(contract.functions.getPublicNotes().call())
    print(publicNotes)
    return render_template('publicNotes.html', allNotes=publicNotes)


def formatNotes(notes, sort_by="timestamp"):
    allNotes = []
    for note in notes:
        allNotes.append({
            "id": note[0],
            "title": note[1],
            "content": note[2],
            "timestamp": formatDate(note[3]),
            "publicNote": note[4],
            "username": note[5][1]
        })
    # print(sort_by,file=sys.stderr)

    if sort_by == "timestamp":
        allNotes.sort(key=lambda x: x[sort_by], reverse=True)
    else:
        allNotes.sort(key=lambda x: x[sort_by], reverse=False)

    # Sort by specified key in reverse order
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
        return render_template('homepage.html', contact=contact)
    else:
        return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5002)
