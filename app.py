from flask import Flask, render_template, request, redirect, session, flash

from models import User, db, connect_db, Note

from forms import RegisterForm, LoginForm, CSRFProtection, AddNote, UpdateNote

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

db.create_all()


@app.get('/')
def redirect_to_register():
    """ Redirect to register page """

    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register():
    """ Register a user on form validate or display register form """

    if 'username' in session:
        username = session['username']
        return redirect(f'/users/{username}')

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()

        session["username"] = username
        return redirect(f'/users/{username}')

    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Logs in user if user found in db (authenticate)"""

    # page protection
    if 'username' in session:
        username = session['username']
        return redirect(f'/users/{username}')

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate_user(username, password)

        if user:
            session["username"] = user.username
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ['Bad username/password']

    return render_template('login.html', form=form)


@app.get('/users/<username>')
def show_user_page(username):
    """Show user page"""

    form = CSRFProtection()

    if "username" not in session:
        flash("must be logged in to access user info")
        return redirect('/login')
    else:
        curr_user = User.query.get(username)
        return render_template('user_page.html', user=curr_user, form=form)


@app.post('/logout')
def logout():
    """Log user out"""

    form = CSRFProtection()

    if form.validate_on_submit():
        session.pop('username', None)

    return redirect('/')


@app.post('/users/<username>/delete')
def delete_user(username):
    """ Delete user's account """

    form = CSRFProtection()    

    if form.validate_on_submit():
        if session["username"] == username:
            user = User.query.get_or_404(username)
            session.pop('username', None)

            # notes = Note.query.filter_by('owner'=username)
            for note in user.notes:
                db.session.delete(note)

            db.session.delete(user)
            db.session.commit()

            flash("User was successfully deleted!")

    return redirect('/')



# ROUTES FOR NOTES

@app.route('/users/<username>/notes/add', methods=['GET', 'POST'])
def add_note(username):
    """ Add a note to the user's profile """

    form = AddNote()

    user = User.query.get_or_404(username)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_note = Note(title=title, content=content, owner=username)

        db.session.add(new_note)
        db.session.commit()

        return redirect(f'/users/{username}')

    else:
        return render_template('add_note.html', form=form, user=user)


@app.route("/notes/<int:note_id>/update", methods=["GET", "POST"])
def update_note(note_id):
    """Display update form to update note, redirects to user page"""

    if "username" not in session:
        flash("must be logged in to access note info")
        return redirect('/login')

    note = Note.query.get_or_404(note_id)
    form = UpdateNote(obj=note)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note.title = title
        note.content = content

        db.session.commit()

        return redirect(f'/users/{note.owner}')
    else:
        return render_template('note.html', form=form, note=note)


@app.post("/notes/<int:note_id>/delete")
def delete_note(note_id):
    """ Delete note """

    note = Note.query.get_or_404(note_id)
    form = CSRFProtection()

    if form.validate_on_submit():
        if session["username"] == note.owner:

            db.session.delete(note)
            db.session.commit()

            flash("Note was successfully deleted!")

    return redirect(f'/users/{note.owner}')