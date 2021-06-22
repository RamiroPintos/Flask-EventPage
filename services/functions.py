from models.models import *
from app import db


def show_events():
    event_list = db.session.query(Event).filter(Event.status == 1)
    return event_list


def get_user(id):
    user = db.session.query(User).filter(User.userId == id).one()
    return user


def get_event(id):
    event = db.session.query(Event).filter(Event.eventId == id).one()
    return event


def get_comment(id):
    return db.session.query(Comment).filter(Comment.commentId == id).one()


def show_myevents(id):
    event_list = db.session.query(Event).filter(Event.userId == id).all()
    return event_list


def show_comments(id):
    return db.session.query(Comment).filter(Comment.eventId == id).all()


def show_requests():
    return db.session.query(Event).filter(Event.status == 0).order_by(Event.date).all()


def list_user():
    return db.session.query(User).all()

