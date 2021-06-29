from flask import url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, \
    check_password_hash  # It allows to generate and verify pass with hash     # TOKENS
from app import db, login_manager, app


class User(UserMixin, db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(500), nullable=False)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, nullable=False, default=False)

    events = db.relationship("Event", back_populates="user", cascade="all, delete-orphan")
    comments = db.relationship("Comment", back_populates="user", cascade="all, delete-orphan")

    # Convert object to JSON
    def to_json(self):
        user_json = {
            'userId': url_for('apiGetUserById', id=self.userId, _external=True),
            'user': self.user,
            'name': self.name,
            'lastname': self.lastname,
            'email': self.email,
        }
        return user_json

    @staticmethod
    # Convert JSON to objet
    def from_json(user_json):
        user = user_json.get('user')
        name = user_json.get('name')
        lastname = user_json.get('lastname')
        email = user_json.get('email')
        return user(user=user, name=name, lastname=lastname, email=email)

    # It is a decorator that will allow us to intercept the writing, reading, deletion of attributes
    @property
    def password(self):
        raise AttributeError('The password cannot be read')

    #  Set the password and generate a hash
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_id(self):
        return self.userId

    #  Compares the hash of the entered value with that of the database
    def check_pass(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return str(self.name) + ' ' + str(self.lastname)

    # Check if the user is an admin
    def is_admin(self):
        aux = False
        if self.admin == 1:
            aux = True
        return aux

    # Checks if the user is an owner, it can be used with comments or events.
    def is_owner(self, event_or_comment):
        aux = False
        if self.userId == event_or_comment.userId:
            aux = True
        return aux


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Event(db.Model):
    eventId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    title = db.Column(db.String(60), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    place = db.Column(db.String(60), nullable=False)
    image = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    type = db.Column(db.String(15), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)

    user = db.relationship("User", back_populates="events")
    comments = db.relationship("Comment", back_populates="event", cascade="all, delete-orphan")

    # Convert object to JSON
    def to_json(self):
        event_json = {
            'eventId': url_for('apiGetEventById', id=self.eventId, _external=True),
            'title': self.title,
            'date': self.date,
            'place': self.place,
            'image': self.image,
            'description': self.description,
            'type': self.type,
        }
        return event_json

    @staticmethod
    # Convert JSON to object
    def from_json(event_json):
        title = event_json.get('title')
        date = event_json.get('date')
        place = event_json.get('place')
        image = event_json.get('image')
        description = event_json.get('description')
        type = event_json.get('type')
        return event(event=event, title=title, date=date, place=place,
                     image=image, description=description, type=type, status=status)


class Comment(db.Model):
    commentId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=False)
    eventId = db.Column(db.Integer, db.ForeignKey('event.eventId'), nullable=False)
    text = db.Column(db.String(500), nullable=False)

    user = db.relationship("User", back_populates="comments")
    event = db.relationship("Event", back_populates="comments")

    # Convert objet to JSON
    def to_json(self):
        comment_json = {
            'commentId': url_for('apiGetCommentById', id=self.commentId, _external=True),
            'user': self.user.user,
            'text': self.text,
            'event': url_for('apiGetEventById', id=self.eventId, _external=True)
        }
        return comment_json

    @staticmethod
    # Convert JSON to object
    def from_json(comment_json):
        user = comment_json.get('user')
        event = comment_json.get('event')
        text = comment_json.get('text')
        return comment(event=event, user=user, text=text)
