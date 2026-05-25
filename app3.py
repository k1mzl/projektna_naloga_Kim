from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(
    __name__,
    template_folder="templates3",
    static_folder="static3"
)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"

db = SQLAlchemy(app)


class Task(db.Model):
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    text = db.Column(
        db.String(200)
    )


@app.route("/")
def index():

    vsi_taski = Task.query.all()

    return render_template(
        "index.html",
        tasks=vsi_taski
    )

    
@app.route("/add", methods=["GET", "POST"])
def add_task():

    if request.method == "POST":
        text = request.form["text"]
        
        nov_task = Task(
            text=text
        )

        db.session.add(nov_task)
        db.session.commit()

        return redirect("/")
    return render_template("add_task.html")


@app.route("/delete/<int:id>")
def izbrisi_task(id):

    task = Task.query.get(id)

    db.session.delete(task)

    db.session.commit()

    return redirect("/")


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5002)