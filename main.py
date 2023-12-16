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

@app.route("/signup/customer", methods=["GET", "POST"])
def signup_customer_page():

    required_fields = ["username", "password", "firstname", "lastname", "street", "housenumber", "postalcode"]

    if request.method != "POST":
        return render_template("signup.html")

    if not set(required_fields).issubset(request.form.keys()):
        return render_template("signup.html", missing_fields=True)
    database.create_KundenAccount(request.form["username"], request.form["password"], request.form["firstname"], request.form["lastname"],\
                                request.form["street"], request.form["housenumber"], request.form["postalcode"])
    return redirect(url_for("login_customer_page"))

@app.route("/signup/business", methods=["GET", "POST"])
def signup_business_page():

    required_fields = ["username", "password", "restaurantname", "description", "street", "housenumber", "postalcode"]

    if request.method != "POST":
        return render_template("signup.html", business=True)

    if not set(required_fields).issubset(request.form.keys()):
        return render_template("signup.html", missing_fields=True)
    database.create_GeschaeftsAccount(request.form["username"], request.form["password"], request.form["restaurantname"], request.form["description"],\
                                request.form["street"], request.form["housenumber"], request.form["postalcode"])
    return redirect(url_for("login_business_page"))
    
@app.route("/login/customer", methods=["GET", "POST"])
def login_customer_page():
    if request.method == "POST":
        if database.login_kunde(request.form["username"], request.form["password"]):
            if "stayloggedin" in request.form:
                session.permanent = True
            else:  
                session.permanent = False
            session["user"] = request.form["username"]
            session.pop("business", None)
            return redirect(url_for("restaurants_page"))
    return render_template("login.html")

@app.route("/login/business", methods=["GET", "POST"])
def login_business_page():
    if request.method == "POST":
        print(database.login_geschaeft(request.form["username"], request.form["password"]))
        if database.login_geschaeft(request.form["username"], request.form["password"]):
            if "stayloggedin" in request.form:
                session.permanent = True
            else:  
                session.permanent = False
            session["user"] = request.form["username"]
            session["business"] = True
            return redirect(url_for("start_page"))
    return render_template("login.html", business=True)

@app.route("/logout/")
def logout_page():
    session.pop("user", None)
    return redirect(url_for("start_page"))

@app.route("/restaurants/")
def restaurants_page():
    if "user" in session and not "business" in session:
        restaurants = database.get_restaurants(session["user"])
        print(restaurants)
        return render_template("restaurants.html", restaurants=restaurants)
    else:
        return redirect(url_for("login_customer_page"))

@app.route("/restaurant/<id>")
def restaurant_page(id):
    if "user" in session and not "business" in session:
        restaurants = database.get_restaurants()
        print(restaurants)
        return render_template("restaurants.html", restaurants=restaurants)
    else:
        return redirect(url_for("login_customer_page"))

if __name__ == "__main__":
    app.run(debug=True)