from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

class User(db.Model):
    """ Creating a User """

    notes = db.relationship('Note', backref = "user")

    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True)

    password = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(50), nullable=False, unique=True)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)


    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """ Register a user and return an instance of the user """

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

        return cls(username=username, password=hashed_pw, email=email,
                first_name=first_name, last_name=last_name)


    @classmethod
    def authenticate_user(cls, username, password):
        """ Authenticate if the user is valid and return an instance of the user"""

        user = cls.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Note(db.Model):
    """ Create a Note """

    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.Text, nullable=False)

    owner = db.Column(db.Text, db.ForeignKey('users.username'), nullable=False)



def connect_db(app):
    """ Connecting to database """

    db.app = app
    db.init_app(app)
