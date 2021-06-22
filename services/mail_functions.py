import smtplib
from threading import Thread

from flask import render_template
from flask_mail import Message

from app import email, app
from exceptions.exceptions import write_logmail


def sendMail(to, subject, template, **kwargs):
    msg = Message(subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template('email/' + template + '.txt', **kwargs)
    msg.html = render_template('email/' + template + '.html', **kwargs)
    thr = Thread(target=mail_sender, args=[app, msg, to, subject])
    # Start thread
    thr.start()


def mail_sender(app, msg, to, subject):
    with app.app_context():
        try:
            email.send(msg)
        except smtplib.SMTPAuthenticationError as e:
            print("Error de autenticacion: " + str(e))
            write_logmail(e, "Error de autenticacion: ", subject, to)

        except smtplib.SMTPServerDisconnected as e:
            print("Servidor desconectado: " + str(e))
            write_logmail(e, "Servidor descontctado: ", subject, to)

        except smtplib.SMTPSenderRefused as e:
            print("Se requiere autenticacion: " + str(e))
            write_logmail(e, "Se requiere autenticacion: ", subject, to)

        except smtplib.SMTPException as e:
            print("Unexpected error: " + str(e))
            write_logmail(e, "Unexpected error: ", subject, to)
