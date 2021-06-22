from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SelectField, \
    SubmitField, TextField
from wtforms import validators, BooleanField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import ValidationError
from wtforms_components import TimeField
from app import db
from models.models import *


class LoginForm(FlaskForm):
    # Mail field definition
    email = EmailField('E-email',
                       [
                           validators.Required(message="Email requerido"),
                           validators.Email(message='Formato de email incorrecto')
                       ])

    # Password field definition
    password = PasswordField('Contraseña', [
        validators.Required(),
    ])

    remember_me = BooleanField('Recordar esta cuenta')

    # Definition of submit field
    submit = SubmitField("Ingresar")


class UserRegister(FlaskForm):

    # Username validation function
    def user_symbolFilter(form, field):
        if (field.data.find("_") != -1) or (field.data.find("#") != -1):
            raise validators.ValidationError("El título solo puede contener letras, números y puntos")

    # Check if the username already exists in the data base
    def validate_username(self, field):
        if User.query.filter_by(user=field.data).first():
            raise ValidationError('Nombre de usuario no disponible')

    def make_optional(field):
        field.validators.insert(0, validators.Optional())

    user = TextField('Nombre de Usuario',
                     [
                         validators.Required(message="Nombre de usuario requerido"),
                         validators.length(min=4, max=25, message='La longitud del nombre de usuariono es válida'),
                         user_symbolFilter,
                         validate_username
                     ])

    name = TextField('Nombre',
                     [
                         validators.Required(message="Nombre requerido"),
                         validators.length(min=4, max=25, message='La longitud del nombre no es válida'),
                         user_symbolFilter
                     ])

    lastname = TextField('Apellido',
                         [
                             validators.Required(message="Apellido requerido"),
                             validators.length(min=4, max=25, message='La longitud del apellido no es válida'),
                             user_symbolFilter
                         ])

    password = PasswordField('Contraseña',
                             [
                                 validators.Required(),
                                 # The password field must match to confirm
                                 validators.EqualTo("confirm", message="La contraseña no coincide")
                             ])

    confirm = PasswordField("Repetir contraseña")

    email = EmailField('Correo electrónico',
                       [
                           validators.Required(message="Email requerido"),
                           validators.Email(message='Formato de email incorrecto')
                       ])

    submit = SubmitField("Enviar")


class EventRegister(FlaskForm):

    def event_symbolFilter(form, field):
        if (field.data.find("_") != -1) or (field.data.find("#") != -1):
            raise validators.ValidationError("El título solo puede contener letras, números y puntos")

    def make_optional(field):
        field.validators.insert(0, validators.Optional())

    event_types = [
        ('Fiesta Privada', 'Fiesta Privada'),
        ('Fiesta pública', 'Fiesta pública'),
        ('Recital', 'Recital'),
        ('Deporte', 'Deporte'),
        ('Teatro', 'Teatro'),
        ('Conferencia', 'Conferencia'),
        ('Muestra', 'Muestra'),
        ('Fiesta', 'Fiesta'),
        ('Fastival', 'Fastival'),
        ('Otro', 'Otro'),
    ]

    title = StringField('Título',
                        [
                            validators.DataRequired(message="Título requerido"),
                            validators.length(min=5, max=60,
                                              message='El título del evento debe tener entre 5 y 60 caracteres'),
                            event_symbolFilter
                        ])

    date = DateField('Fecha del evento',
                     [
                         validators.DataRequired(message="Ingrese una fecha válida")
                     ])

    time = TimeField('Hora',
                     [
                         validators.DataRequired(message="Ingrese un horario válido")
                     ])

    place = StringField('Lugar',
                        [
                            validators.Required(message="Lugar del evento requerido")
                        ])

    image = FileField(validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'El archivo debe ser una image jpg o png')
    ])

    description = TextAreaField('Descripción')

    type = SelectField('Tipo', choices=event_types)

    submit = SubmitField("Registrar Evento")


class CommentLog(FlaskForm):
    comment = TextAreaField('Comentario', [
        validators.Required(message="Ingrese un comentario"),
        validators.Length(min=5)
    ])

    submit = SubmitField("Enviar")


class Filter(FlaskForm):
    type = [
        ('empty', 'Todas'),
        ('Fiesta Privada', 'Fiesta Privada'),
        ('Fiesta pública', 'Fiesta pública'),
        ('Recital', 'Recital'),
        ('Deporte', 'Deporte'),
        ('Teatro', 'Teatro'),
        ('Conferencia', 'Conferencia'),
        ('Muestra', 'Muestra'),
        ('Fiesta', 'Fiesta'),
        ('Fastival', 'Fastival'),
        ('Otro', 'Otro'),
    ]

    date = DateField('Fecha')

    title = StringField('Titulo', render_kw={"placeholder": "Titulo completo"})

    type = SelectField('Tipo', [], choices=type)

    submit = SubmitField("Buscar")


class LoginForm(FlaskForm):
    email = EmailField('Email',
                       [
                           validators.Required(message="Email requerido"),
                           validators.Email(message='Formato de email incorrecto')
                       ])

    password = PasswordField('Password', [
        validators.Required(),
    ])

    remember_me = BooleanField('Recordarme')

    submit = SubmitField("Entrar")


def validate_existence(email):
    aux = False

    if db.session.query(User).filter(User.email.ilike(email)).count() == 0:
        aux = True
    return aux
