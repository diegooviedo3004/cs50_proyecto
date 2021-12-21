from __future__ import unicode_literals
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import youtube_dl
from flask import redirect, session
from functools import wraps

sender_address = 'kevinguadamuz8@gmail.com' # Hay que hacer, que el usuario ingrese correo y contraseña
sender_pass = 'Alexk3viN30'
receiver_address = 'abrahamcastillo3004@gmail.com'

def enviar_email(subject,content):
    mail_content = content
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject


    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def descargar_plataformas(url):
    ydl_opts = {
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except:
            return "Not a valid url"