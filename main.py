from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import database
import createdb

app = Flask(__name__)
app.secret_key = "schimmel"
app.permanent_session_lifetime = timedelta(days=1)
createdb.create_tables()


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

    for value in request.form.values():
        if value == '': return render_template("signup.html", missing_fields=True)

    database.create_KundenAccount(request.form["username"], request.form["password"], request.form["firstname"], request.form["lastname"],\
                                request.form["street"], request.form["housenumber"], request.form["postalcode"])
    return redirect(url_for("login_customer_page"))

@app.route("/signup/business", methods=["GET", "POST"])
def signup_business_page():

    required_fields = ["username", "password", "restaurantname", "description", "street", "housenumber", "postalcode"]

    if request.method != "POST":
        return render_template("signup.html", business=True)
    
    for value in request.form.values():
        if value == '': return render_template("signup.html", missing_fields=True)

    database.create_GeschaeftsAccount(request.form["username"], request.form["password"], request.form["restaurantname"], request.form["description"],\
                                request.form["street"], request.form["housenumber"], request.form["postalcode"])
    return redirect(url_for("login_business_page"))
    
@app.route("/login/customer", methods=["GET", "POST"])
def login_customer_page():
    if request.method == "POST":

        for value in request.form.values():
            if value == '': return render_template("login.html", missing_fields=True)

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

        for value in request.form.values():
            if value == '': return render_template("login.html", missing_fields=True)

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

@app.route("/restaurants_near_you/")
def restaurants_page():
    if "user" in session and not "business" in session:
        restaurants = database.get_restaurants_near(session["user"])
        print(restaurants)
        return render_template("restaurants.html", restaurants=restaurants)
    else:
        return redirect(url_for("login_customer_page"))
    

@app.route("/restaurants/all")
def all_restaurants_page():
    restaurants = database.get_restaurants()
    return render_template("restaurants.html", restaurants=restaurants)

@app.route("/menue/<username>")
def menue_page(username):
    if "user" in session:
        restaurant = database.get_restaurant(username)
        items = database.get_items(username)
        return render_template("menue.html", restaurant=restaurant, items=items)
    else:
        return redirect(url_for("login_customer_page"))

@app.route("/restaurant/edit")
def edit_restaurant_page(username):
    if "user" in session and "business" in session:
        postalcodes = database.get_delivery_radius(username)
        return render_template("edit_restaurant.html", postalcodes=postalcodes)
    else:
        return redirect(url_for("login_customer_page"))
    



if __name__ == "__main__":
    app.run(debug=True)