from flask import flash, render_template
from flask import redirect, url_for, abort
from werkzeug.utils import secure_filename
import os.path
import os
from random import randint
from forms.forms import *
from app import app, db, login_manager
from services.functions import *
from services.mail_functions import sendMail
from flask_login import login_required, login_user, logout_user, current_user, LoginManager


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Debes iniciar sesión para continuar', 'warning')
    return redirect(url_for('index'))


def has_permission(user, event):
    aux = False
    if user.is_authenticated:
        if user.is_admin() or user.is_owner(event):
            aux = True
    return aux


@app.route('/', methods=["POST", "GET"])
@app.route('/<int:pag>', methods=["POST", "GET"])
def index(pag=1):
    filter = Filter()
    login_form = LoginForm()
    title = "Home"
    pag_size = 2
    event_list = show_events()

    events = event_list.filter(Event.status == 1).order_by(Event.date).paginate(pag, pag_size, error_out=False)

    if filter.is_submitted():
        event_list = db.session.query(Event)

        if filter.date.data is not None:
            event_list = event_list.filter(Event.date == filter.date.data)
        if filter.type.data != 'empty':
            event_list = event_list.filter(Event.type == filter.type.data)
        if filter.title.data != "":
            event_list = event_list.filter(Event.title.ilike('%' + filter.title.data + '%'))

        events = event_list.filter(Event.status == 1).order_by(Event.date).paginate(pag, pag_size, error_out=False)

        return render_template('events.html', title=title, events=events, event_list=event_list, filter=filter,
                               destination=filter, login_form=login_form)
    return render_template('events.html', title=title, events=events, filter=filter, login_form=login_form)


@app.route('/my-events')
@login_required
def my_events():
    from services.functions import show_myevents
    title = "Mis eventos"
    event_list = show_myevents(current_user.userId)

    return render_template('my_events.html', event_list=event_list)


@app.route('/show-event/<id>', methods=["POST", "GET"])
def show_event(id):
    event = get_event(id)
    login_form = LoginForm()

    if event.status == 1 or has_permission(current_user, event):

        form = CommentLog()
        comment_list = show_comments(id)

        if form.is_submitted():
            if form.validate_on_submit():
                flash('Comentario añadido', 'success')

                comment = Comment(text=form.comment.data, userId=current_user.userId,
                                  eventId=id)
                db.session.add(comment)
                db.session.commit()
                return redirect(url_for('show_event', id=id, login_form=login_form))
            else:
                flash('No se pudo comentar el evento', 'danger')
        return render_template('show_event.html', event=event, form=form,
                               comment_list=comment_list, id=id, login_form=login_form)
    else:
        return redirect(url_for('index'))


@app.route('/about')
def about():
    login_form = LoginForm()
    return render_template('about.html', login_form=login_form)


@app.route('/user-register', methods=["POST", "GET"])
def user_register():
    title = "Registro de usuario"
    login_form = LoginForm()
    form = UserRegister()

    if form.validate_on_submit():
        if validate_existence(form.email.data):
            user = User(name=form.name.data, lastname=form.lastname.data,
                        user=form.user.data, email=form.email.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()

            flash('Usuario creado con éxito', 'success')
            sendMail(form.email.data, 'Bienvenido a NDEAAH eventos', 'user_created', form=form)

            login_user(user, True)
            return redirect(url_for('index'))
        else:
            flash('Hay una cuenta registrada con el correo electrónico. Intenta recuperar tu contraseña', 'danger')

    return render_template('user_form.html', title=title, form=form,
                           login_form=login_form, destination=user_register)


@app.route('/create-event', methods=["POST", "GET"])
@login_required
def event_register():
    form = EventRegister()

    if form.validate_on_submit():
        f = form.image.data
        filename = secure_filename(form.title.data + " image" + str(randint(1, 100)))
        f.save(os.path.join('./static/images/', filename))
        flash('¡Evento creado con éxito! Debe ser aprobado por un administrador', 'success')
        event = Event(title=form.title.data, date=form.date.data,
                      time=form.time.data, image=filename,
                      place=form.place.data, type=form.type.data,
                      description=form.description.data, userId=current_user.userId)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('event_form.html', form=form, destination="event_register")


@app.route('/update-event/<int:id>', methods=["POST", "GET"])
@login_required
def update_event(id):
    event = get_event(id)
    if has_permission(current_user, event):

        class Event:
            event_name = event.title
            event_date = event.date
            event_time = event.time
            event_place = event.place
            image = event.image
            event_description = event.description
            event_type = event.type

        form = EventRegister(obj=Event)

        if form.validate_on_submit():
            flash('¡Evento editado con éxito! Debe ser aprobado por un administrador', 'success')

            event.title = form.title.data
            event.date = form.date.data
            event.time = form.time.data
            event.place = form.place.data
            event.description = form.description.data
            event.type = form.type.data
            event.status = 0

            db.session.add(event)
            db.session.commit()
            return redirect(url_for('my_events'))

        return render_template('event_form.html', form=form, destination="update_event",
                               event=event)
    else:
        return redirect(url_for('index'))


# User queries
@app.route('/user-list')
@login_required
def show_userList():
    user_list = list_user()

    if current_user.is_admin():
        return render_template('users.html', user_list=user_list)

    else:
        flash('Permiso de acceso denegado', 'warning')
        return redirect(url_for('index'))


# Delete User
@app.route('/delete-user/<int:id>')
@login_required
def deleteUserById(id):
    user = get_user(id)

    if current_user.is_admin():
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('show_userList'))

    else:
        flash('Permiso de acceso denegado', 'warning')
        return redirect(url_for('index'))


# Event queries
@app.route('/requests')
@login_required
def requests():
    event_list = show_requests()

    if current_user.is_admin():
        return render_template('requests.html', event_list=event_list)

    else:
        flash('Permiso de acceso denegado', 'warning')
        return redirect(url_for('index'))


@app.route('/approveById/<int:id>')
@login_required
def approveById(id):
    if current_user.is_admin():
        event = get_event(id)
        event.status = 1
        db.session.commit()
        sendMail(event.user.email, 'Evento aprobado', 'event_approved', event=event)
        return redirect(url_for('requests'))
    else:
        flash('Permiso de acceso denegado', 'warning')
        return redirect(url_for('index'))


@app.route('/deleteById/<int:id>')
@login_required
def deleteById(id):
    event = get_event(id)
    if current_user.is_admin() or current_user.is_owner(event):
        db.session.delete(event)
        db.session.commit()
        return redirect(url_for('requests'))
    else:
        flash('Permiso de acceso denegado', 'warning')
        return redirect(url_for('index'))


# Comment queries
@app.route('/deleteCommentById/<int:id>')
@login_required
def deleteCommentById(id):
    comment = get_comment(id)

    if current_user.is_admin() or current_user.is_owner(comment):
        db.session.delete(comment)
        db.session.commit()
        flash('Comentario añadido', 'success')
        return redirect(url_for('show_event', id=comment.eventId))
    else:
        flash('Permiso de acceso denegado', 'warning')
        return redirect(url_for('index'))


# Login
@app.route('/login', methods=["POST"])
def login():
    # Instance LoginForm
    login_form = LoginForm()

    if login_form.validate_on_submit():
        # Get user by email
        user = User.query.filter_by(email=login_form.email.data).first()
        # If the user exists and the password is verified
        if user is not None and user.check_pass(login_form.password.data):
            login_user(user, login_form.remember_me.data)
        else:
            # Show authentication error
            flash('Email o contraseña incorrecto', 'danger')
    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
