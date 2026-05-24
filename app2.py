from flask import Flask, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Flask app
app = Flask(
    __name__,
    template_folder="templates2",
    static_folder="static2"
)

app.secret_key = "secretkey"

UPLOAD_FOLDER = "static2/uploads"

os.makedirs(UPLOAD_FOLDER,exist_ok=True)

os.makedirs("db2",exist_ok=True)


basedir = os.path.abspath(os.path.dirname(__file__))

# pot do baze
db_path = os.path.join(
    basedir,
    "db2",
    "social.db"
)

# baza
app.config["SQLALCHEMY_DATABASE_URI"] = \
    "sqlite:///" + db_path

db = SQLAlchemy(app)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True
    )

    password = db.Column(db.String(200))

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.Text)

    image = db.Column(db.String(200))

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        password = generate_password_hash(
            request.form["password"]
        )

        # preveri user
        user = User.query.filter_by(
            username=username
        ).first()

        if user:
            return "User že obstaja"

        new_user = User(
            username=username,
            password=password
        )

        db.session.add(new_user)

        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            session["user_id"] = user.id

            return redirect("/")

        return "Napačni podatki"

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

@app.route("/")
def index():

    if "user_id" not in session:
        return redirect("/login")

    posts = Post.query.all()

    return render_template(
        "index.html",
        posts=posts
    )

@app.route("/add", methods=["GET", "POST"])
def add_post():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        content = request.form["content"]

        file = request.files["image"]

        filename = ""

        # shrani sliko
        if file and file.filename != "":

            filename = file.filename

            file.save(
                os.path.join(
                    UPLOAD_FOLDER,
                    filename
                )
            )

        new_post = Post(
            content=content,
            image=filename,
            user_id=session["user_id"]
        )

        db.session.add(new_post)

        db.session.commit()

        return redirect("/")

    return render_template("add_post.html")


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5001)
