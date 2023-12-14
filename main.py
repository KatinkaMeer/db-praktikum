from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import database

app = Flask(__name__)
app.secret_key = "schimmel"
app.permanent_session_lifetime = timedelta(days=1)
database.create_tables()


@app.route("/test/")
def test_page():
    return render_template("test.html")

@app.route("/")
def start_page():
    return render_template("index.html")

@app.route("/admin/")
def admin_page():
    return redirect(url_for("start_page"))

@app.route("/signup/", methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        database.create_KundenAccount(request.form["username"], request.form["password"], request.form["firstname"], request.form["lastname"],\
                                     request.form["street"], request.form["housenumber"], request.form["postalcode"])
    return render_template("signup.html")

@app.route("/login/", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        if database.login_kunde(request.form["username"], request.form["password"]):
            if "stayloggedin" in request.form:
                session.permanent = True
            else:  
                session.permanent = False
            session["user"] = request.form["username"]
            return redirect(url_for("restaurants_page"))
    return render_template("login.html")

@app.route("/logout/")
def logout_page():
    session.pop("user", None)
    return redirect(url_for("login_page"))

@app.route("/restaurants/")
def restaurants_page():
    if "user" in session:
        return render_template("index.html")
    else:
        return redirect(url_for("login_page"))


if __name__ == "__main__":
    app.run(debug=True)