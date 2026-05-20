import os
from flask import Flask, render_template,request,redirect,session,jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__,template_folder="templates1",static_folder="static1")
app.secret_key="skrivniključ"

# nastavim povezavo do SQLite baze
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "db", "notes.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


#Flask aplikacijo povežemo z SQLAlchemy
db = SQLAlchemy(app)

class User(db.Model):
    # ID uporabnika
    id = db.Column(db.Integer, primary_key=True)

    # Uporabniško ime
    username = db.Column(db.String(100), unique=True, nullable=False)

    # Geslo
    password = db.Column(db.String(200), nullable=False)


class Note(db.Model):
    # ID zapiska
    id = db.Column(db.Integer, primary_key=True)

    # Naslov zapiska
    title = db.Column(db.String(200), nullable=False)

    # Vsebina zapiska
    content = db.Column(db.Text, nullable=False)

    #ID uporabnika(lastnik zapiska)

    user_id=db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    

@app.route("/register", methods=["GET", "POST"])
def register():

    #Če uporabnik poskuša registrirati
    if request.method == "POST":

        #dobimo podatke iz obrazca
        username=request.form["username"]
        password=request.form["password"]
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return "Uporabniško ime že obstaja"
        #hashiramo geslo
        hashed_password=generate_password_hash(password)

        #ustvarimo novega uporabnika
        new_user=User(
            username=username,
            password=hashed_password

        )

        db.session.add(new_user)
        
        
        #shranimo uporabnika
        db.session.commit()

        #presumerimo na login
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username=request.form["username"]
        password=request.form["password"]


        #poiščemo uporabnika v bazi
        user=User.query.filter_by(username=username).first()

        #preverimo geslo
        if user and check_password_hash(user.password,password):
            
            #shrani ID uporabnika
            session["user_id"]=user.id

            return redirect ("/")

        return "napačni podatki"

    return render_template("login.html")

@app.route("/logout")
def logout():

    # Izbrišemo session
    session.clear()

    return redirect("/login")

@app.route("/")
def index():

    #preverimo ali je uporabnik prijavljen
    if "user_id" not in session:
        return redirect("/login")

    #dobimo zapise uporabnika
    notes=Note.query.filter_by(
        user_id=session["user_id"]   
    ).all()

    return render_template("index.html",notes=notes)

@app.route("/add", methods=["GET", "POST"])
def add_note():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        # Podatki iz forme
        title = request.form["title"]
        content = request.form["content"]

        # Ustvarimo nov zapisek
        note = Note(
            title=title,
            content=content,
            user_id=session["user_id"]
        )

        # Dodamo v bazo
        db.session.add(note)

        # Shranimo spremembe
        db.session.commit()

        return redirect("/")

    return render_template("add_note.html")      

if __name__ == "__main__":


    app.run(debug=True)
