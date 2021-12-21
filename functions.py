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


def descargar_plataformas(url,opcion):
    ydl_opts = {}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            meta = ydl.extract_info(
                url, download=False)


            if opcion == "youtube" or opcion == "twitter" or opcion == "tiktok":
                # link del video
                links = meta["webpage_url"]

                if opcion == "youtube" or opcion == "twitter":
                # miniatura del video
                    miniatura = meta["thumbnails"][0]["url"]
                else:
                    miniatura = meta["thumbnail"]

                # plataforma proveniente del video
                plataforma = meta["extractor"]

                title = meta["title"]

                lista = [miniatura, title, plataforma, links]

                return lista

            else:
                links = meta["webpage_url"]
                plataforma = meta["extractor"]
                miniatura = "https://capafons.es/wp-content/uploads/2021/05/facebook-logo-new.png"
                title = "Video de Facebook"
                lista = [miniatura, title, plataforma, links]
                return lista

        except:
            return "1"

def descargar_audio(url):
    ydl_opts = {
        'format': 'bestaudio',
        'noplaylist' : True
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            meta = ydl.extract_info(
                url, download=False)
            return meta["formats"][0]["format_id"]
        except:
            return "1"


