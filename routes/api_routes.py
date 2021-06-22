from flask import request
from app import csrf, app, db
from flask import jsonify
from services.functions import *
from services.mail_functions import sendMail
from sqlalchemy.exc import SQLAlchemyError


# Show User by ID
# curl -i -H "Content-Type:application/json" -H "Accept: application/json" http://localhost:5000/api/user/id
@app.route('/api/user/<id>', methods=['GET'])
def apiGetUserById(id):
    user = get_user(id)
    return jsonify(user.to_json())


# Show all Users
# curl -H "Accept:application/json" http://localhost:5000/api/users
@app.route('/')
@app.route('/api/users/', methods=['GET'])
def apiShowUsers():
    users_list = list_user()
    return jsonify({'users': [user.to_json() for user in users_list]})


# Delete User
# curl -i -X DELETE -H "Accept: application/json" http://localhost:5000/api/user/id
@app.route('/api/user/<id>', methods=['DELETE'])
@csrf.exempt
def deleteUser(id):
    user = get_user(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204


# Show Event by ID
# curl -i -H "Content-Type:application/json" -H "Accept: application/json" http://localhost:5000/api/event/id
@app.route('/api/event/<id>', methods=['GET'])
def apiGetEventById(id):
    event = get_event(id)
    return jsonify(event.to_json())


# Show all Events
# curl -H "Accept:application/json" http://localhost:5000/api/event/
@app.route('/')
@app.route('/api/event/', methods=['GET'])
def apiShowEvents():
    event_list = show_events()
    return jsonify({'events': [event.to_json() for event in event_list]})


# Update Event
# curl -i -X PUT -H "Content-Type:application/json" -H "Accept:application/json" http://localhost:5000/api/evento/id -d '{"title":"", "type":""}'
@app.route('/api/event/<id>', methods=['PUT'])
@csrf.exempt
def apiUpdateEvent(id):
    event = get_event(id)
    event.title = request.json.get('title', event.title)
    event.date = request.json.get('date', event.date)
    event.place = request.json.get('place', event.place)
    event.description = request.json.get('description', event.description)
    event.type = request.json.get('type', event.type)
    event.status = 0
    try:
        db.session.add(event)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print(e)

    return jsonify(event.to_json()), 201


# Approve event
# curl -i -X PUT -H "Content-Type:application/json" -H
# "Accept:application/json" http://localhost:5000/api/event/id/approve
@app.route('/api/event/<id>/approve', methods=['PUT'])
@csrf.exempt
def apiApproveEvent(id):
    event = get_event(id)
    event.status = 1
    db.session.add(event)
    db.session.commit()

    sendMail(event.user.email, 'Evento aprobado', 'event_approved', event=event)
    return jsonify(event.to_json()), 201


# Delete Event
# curl -i -X DELETE -H "Accept: application/json" http://localhost:5000/api/event/id
@app.route('/api/event/<id>', methods=['DELETE'])
@csrf.exempt
def deleteEvent(id):
    event = get_event(id)
    db.session.delete(event)
    db.session.commit()
    return '', 204


# Show Comment by ID
# curl -i -H "Content-Type:application/json" -H "Accept: application/json" http://localhost:5000/api/comment/id
@app.route('/api/comment/<id>', methods=['GET'])
def apiGetCommentById(id):
    comment = get_comment(id)
    return jsonify(comment.to_json())


# Show Comments by Events
# curl -i -H "Content-Type:application/json" -H "Accept: application/json" http://localhost:5000/api/comments/id
@app.route('/api/comments/<event>', methods=['GET'])
def apiGetCommentByEvent(event):
    comment_list = show_comments(event)
    return jsonify({'Comments': [comment.to_json() for comment in comment_list]})


# Delete Comment
# curl -i -X DELETE -H "Accept: application/json" http://localhost:5000/api/comment/id
@app.route('/api/comment/<id>', methods=['DELETE'])
@csrf.exempt
def apiDeleteCommentById(id):
    comment = get_comment(id)
    db.session.delete(comment)
    db.session.commit()
    return '', 204
