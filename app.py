from __future__ import unicode_literals
from flask import Flask, render_template, request, redirect, flash, session, send_file, send_from_directory, abort
import os
from flask_session import Session
from functions import *
from tempfile import mkdtemp
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash

# creando app
app = Flask(__name__)
app.config['SECRET_KEY'] = "?/x9c/xb0v/x83N/xd43nt/xbbT}//xf0/xd9/xc4/xa1?/xe4/x0f/xf8Z</xaa"

db = SQL("sqlite:///bd.db")

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/",methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        pass
    else:
        return render_template("index.html")

@app.route("/login",methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username").strip()
        password =  request.form.get("password").strip()

        if username == "" or password == "":
            return redirect("/login") #cambiar por una pagina de error, o ver como validar en js

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return redirect("/login") #no existe el usuario

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username").strip()
        password =  request.form.get("password").strip()
        confirmation =  request.form.get("confirmation").strip()

        # VALIDACIONES SI NO SE INTRODUJO ALGO
        if username == "" or password == "" or confirmation == "":
            return redirect("/register") #cambiar por una pagina de error, o ver como validar en js

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # VALIDACION NO PODER CREAR DOS USUARIOS CON EL MISMO NOMBRE
        for i in rows:
            if(i["username"] == request.form.get("username")):
                return redirect("/register") # decirle al usuario que el usuario ya esta tomado

        # VALIDACION QUE AMBAS CONTRASEÑAS SEAN IGUALES

        if(request.form.get("confirmation") != request.form.get("password")):
            return redirect("/register") # decirle al usuario que las contraseñas no son iguales

        # SE INTRODUCE EL USUARIO A LA BD
        db.execute("INSERT INTO users (username,hash) VALUES (?,?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/contacto",methods=["GET", "POST"])
@login_required
def contacto():
    if request.method == "POST":
        nombre = request.form.get("name").strip()
        subject =  request.form.get("subject").strip()
        message =  request.form.get("message").strip()
        if nombre == "" or subject == "" or message == "":
            return redirect("/contacto") #cambiar por una pagina de error, o ver como validar en js

        enviar_email(subject,f"by {nombre}: {message}")
        return redirect("/contacto")

    else:
        return render_template("contact.html")

@app.route("/descargar",methods=["GET", "POST"])
@login_required
def descargar():
    if request.method == "POST":
        link = request.form.get("link")
        # LIMPIANDO ESPACIOS VACIOS
        link = link.strip()
        # VALIDACION ESPACIO VACIO
        if link == "":
            return redirect("/descargar")

        opcion = request.form.get("plataforma")
        if opcion == "youtube":
            if descargar_plataformas(link,opcion) == "1":
                abort(403)

            formato = request.form.get("formato")
            lista = descargar_plataformas(link,opcion)

            miniatura = lista[0]

            title = lista[1]

            plataforma = lista[2]

            links = lista[3]

            title = (title[:25] + '..') if len(title) > 25 else title

            db.execute("INSERT INTO history(img, titulo, plataforma, links, user_id) VALUES(:img, :titulo, :plataforma, :links, :user_id)",
                img=miniatura, titulo=title, plataforma=plataforma, links=links, user_id=session["user_id"])

            if formato == "video":
                return redirect(f"https://projectlounge.pw/ytdl/download?url={link}")

            else:
                formato_audio = descargar_audio(link)
                return redirect(f"https://projectlounge.pw/ytdl/download?url={link}&format={formato_audio}")

        else:
            if descargar_plataformas(link,opcion) == "1":
                abort(403)

            lista = descargar_plataformas(link,opcion)
            miniatura = lista[0]

            title = lista[1]

            plataforma = lista[2]

            links = lista[3]

            title = (title[:25] + '..') if len(title) > 25 else title

            db.execute("INSERT INTO history(img, titulo, plataforma, links, user_id) VALUES(:img, :titulo, :plataforma, :links, :user_id)",
                img=miniatura, titulo=title, plataforma=plataforma, links=links, user_id=session["user_id"])

            return redirect(f"https://projectlounge.pw/ytdl/download?url={link}")

    else:
        return render_template("descargar.html")

@app.route("/logout",methods=["GET", "POST"])
@login_required
def logout():
    session.clear()
    return redirect("/")

@app.route("/history",methods=["GET", "POST"])
@login_required
def history():

    history = db.execute("SELECT * FROM history WHERE user_id = :user_id", user_id=session["user_id"])

    return render_template("history.html", history=history)

@app.route("/informacion",methods=["GET", "POST"])
@login_required
def informacion():

    return render_template("informacion.html")

@app.route("/desarrollo",methods=["GET", "POST"])
@login_required
def desarrollo():
    return render_template("desarrollo.html")




@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403


@app.errorhandler(401)
def page_not_found(e):
    return render_template('401.html'), 401


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404