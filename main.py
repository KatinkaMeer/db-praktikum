from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)
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
        database.create_KundenAccount(request.form["username"], request.form["password"], "test", "test", "test", "test", "test")
    return render_template("login.html")

@app.route("/login/", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        print(database.login_kunde(request.form["username"], request.form["password"]))
    return render_template("login.html")
    
if __name__ == "__main__":
    app.run(debug=True)