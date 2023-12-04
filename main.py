from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.String(200), nullable = True)

@app.route("/test/")
def test_page():
    return render_template("test.html")

@app.route("/")
def start_page():
    return render_template("index.html")

@app.route("/admin/")
def admin_page():
    return redirect(url_for("start_page"))

@app.route("/login/", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        new_account = Account(
            user = request.form["username"]
        )
        db.session.add(new_account)
        db.session.commit()
    return render_template("login.html")
    
if __name__ == "__main__":
    app.run(debug=True)