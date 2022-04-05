from flask import Flask, render_template, request, redirect

from models import User, db, connect_db

from forms import RegisterForm

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

        return redirect('/secret')

    else:
        return render_template('register.html', form=form)