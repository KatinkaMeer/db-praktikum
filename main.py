from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import database
import createdb
import os

UPLOAD_FOLDER = './static/business'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = "schimmel"
app.permanent_session_lifetime = timedelta(days=1)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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

    usernames = database.get_usernames()
    if request.form["username"] in usernames:
        return render_template("signup.html", username_taken=True)

    for value in request.form.values():
        if value == '': return render_template("signup.html", missing_fields=True)

    database.create_KundenAccount(request.form["username"], request.form["password"], request.form["firstname"], request.form["lastname"],\
                                request.form["street"], request.form["housenumber"], request.form["postalcode"])
    return redirect(url_for("login_customer_page"))

@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile_page():
    if "user" in session and not "business" in session:
        if request.method == "POST" and database.login_kunde(request.form["username"], request.form["password"]):
                
            database.update_KundenAccount(request.form["username"], request.form["password"], request.form["firstname"], request.form["lastname"],\
                                request.form["street"], request.form["housenumber"], request.form["postalcode"])
            return render_template("index.html")
            
        profile = database.get_KundenAccount(session["user"])
        return render_template("edit_profile.html", profile=profile)
    else:
        return render_template("login_kunde.html")

def save_restaurant_image(img):
    _, extension = os.path.splitext(img.filename)
    for other_file in os.listdir(app.config['UPLOAD_FOLDER']):
        stem, other_extension = os.path.splitext(other_file)
        if request.form["username"] == stem:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], other_file))
    img.save(os.path.join(app.config['UPLOAD_FOLDER'], request.form["username"] + extension))

@app.route("/signup/business", methods=["GET", "POST"])
def signup_business_page():

    required_fields = ["username", "password", "restaurantname", "description", "street", "housenumber", "postalcode"]
    

    if request.method != "POST":
        return render_template("signup.html", business=True)

    usernames = database.get_usernames(business=True)
    if request.form["username"] in usernames:
        return render_template("signup.html", business=True, username_taken=True)

    for value in request.form.values():
        if value == '': return render_template("signup.html", missing_fields=True, business=True)


    if "image" in request.files and request.files["image"].filename:
        print(type(request.files["image"]))
        save_restaurant_image(request.files["image"])
        

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
        restaurants = database.get_restaurants_near(session["user"])
        image_names = os.listdir(app.config['UPLOAD_FOLDER'])
        image_tuples = list(map(os.path.splitext, image_names))
        for restaurant in restaurants:
            restaurant["image_path"] = "test1.jpeg"
            for index, value in enumerate(image_tuples):
                if restaurant["username"] == value[0]:
                    restaurant["image_path"] = 'business/' + value[0] + value[1]
                    image_tuples.pop(index)
                    break
            
        return render_template("restaurants.html", restaurants=restaurants)
    else:
        return redirect(url_for("login_customer_page"))
    

@app.route("/menue/<username>", methods=["GET", "POST"])
def menue_page(username):
    if "user" in session:
        restaurant = database.get_restaurant(username)
        image_names = os.listdir(app.config['UPLOAD_FOLDER'])
        image_tuples = list(map(os.path.splitext, image_names))
        restaurant["image_path"] = "test1.jpeg"
        for index, value in enumerate(image_tuples):
            if username == value[0]:
                restaurant["image_path"] = 'business/' + value[0] + value[1]
                image_tuples.pop(index)
                break

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
    
@app.route("/orders")
def order_page():
    if "user" in session:
        if "business" in session:
            orders = database.get_orders(session["user"], True)
            return render_template("orders_business.html", orders=orders)
        else:
            orders = database.get_orders(session["user"], False)
            return render_template("orders_customer.html", orders=orders)
    return redirect(url_for("login_customer_page"))

def get_items(mDict) -> list[dict]:
    names = request.form.getlist("orderlist_names")
    prices = request.form.getlist("orderlist_prices")
    amounts = request.form.getlist("orderlist_amounts")
    items = []
    for (name, price, amount) in zip(names, prices, amounts):
        items.append({
            "name": name,
            "price": int(price),
            "amount": int(amount)
        })
    return items

@app.route("/confirm_order", methods=["POST"])
def confirm_order_page():
    if "user" in session and not "business" in session:
        restaurant = restaurant = database.get_restaurant(request.form["restaurant"])
        items = get_items(request.form)
        item_sum = 0
        for item in items:
            item_sum += item["price"] * item["amount"]
        return render_template("confirm_order.html", restaurant=restaurant, items=items)
    else:
        return redirect(url_for("login_customer_page"))

@app.route("/place_order", methods=["POST"])
def place_order_page():
    if "user" in session and not "business" in session:
        items = get_items(request.form)
        database.create_order(session["user"], request.form["restaurant"], items, request.form["comment"])
        return render_template("place_order.html")
    else:
        return redirect(url_for("login_customer_page"))

if __name__ == "__main__":
    app.run(debug=True)