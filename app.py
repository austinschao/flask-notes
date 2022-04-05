from flask import Flask, render_template, request, redirect, session, flash

from models import User, db, connect_db

from forms import RegisterForm, LoginForm, CSRFProtection

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

        return redirect(f'/users/{username}')

    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Logs in user if user found in db (authenticate)"""

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