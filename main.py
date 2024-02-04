from flask import Flask, render_template, request, redirect, url_for, session
import datetime
import createdb
import database
import os

UPLOAD_FOLDER = './static/business'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
WEEKDAYS = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
DEFAULT_IMAGE = "test1.jpeg"

app = Flask(__name__)
app.secret_key = "schimmel"
app.permanent_session_lifetime = datetime.timedelta(days=1)
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

    if database.check_plz(request.form["postalcode"]) == False: return render_template("signup.html", invalid_plz=True)

    database.create_KundenAccount(request.form["username"], request.form["password"], request.form["firstname"], request.form["lastname"],\
                                request.form["street"], request.form["housenumber"], request.form["postalcode"])
    return redirect(url_for("login_customer_page"))

@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile_page():
    if "user" in session and not "business" in session:
        profile = database.get_KundenAccount(session["user"])
        if request.method == "POST":

            if not request.form["password"]:
                return render_template("edit_profile.html", profile=profile, missing_fields=True)

            if database.login_kunde(session["user"], request.form["password"]):
                
                database.update_KundenAccount(session["user"], request.form["password"], request.form["firstname"], request.form["lastname"],\
                                request.form["street"], request.form["housenumber"], request.form["postalcode"])
                
                profile['firstname'] = request.form["firstname"]
                profile['lastname'] = request.form["lastname"]
                profile['street'] = request.form["street"]
                profile['housenumber'] = request.form["housenumber"]
                profile['postalcode'] = request.form["postalcode"]

                return render_template("edit_profile.html", profile=profile, saved_changes=True)
            else:
                return render_template("edit_profile.html", profile=profile, wrong_credentials=True)
        
        return render_template("edit_profile.html", profile=profile)

    else:
        return redirect(url_for("login_customer_page"))
    
@app.route("/edit_restaurant", methods=["GET", "POST"])
def edit_restaurant_page():
    if "user" in session and "business" in session:
        profile = database.get_restaurant(session["user"])
        if request.method == "POST":

            #if not request.form["password"]:
                #return render_template("edit_restaurant.html", profile=profile, items=items, deliverradius=deliverradius, weekdays=WEEKDAYS, missing_fields=True)

            #Passwortcheck
            if database.login_geschaeft(session["user"], request.form["password"]):
                
                #Datenbank update
                database.update_GeschaeftsAccount(session["user"], request.form["password"], request.form["name"], request.form["description"],\
                                request.form["street"], request.form["housenumber"], request.form["postalcode"])
                #Website Update 
                profile['name'] = request.form["name"]
                profile['description'] = request.form["description"]
                profile['street'] = request.form["street"]
                profile['housenumber'] = request.form["housenumber"]
                profile['postalcode'] = request.form["postalcode"]
                if "image" in request.files and request.files["image"].filename:
                    
                    save_restaurant_image(request.files["image"], session['user'])

                return render_template("edit_restaurant.html", profile=profile, saved_changes=True)
            else:
                return render_template("edit_restaurant.html", profile=profile, wrong_credentials=True)
        
        return render_template("edit_restaurant.html", profile=profile)
    else:
        return redirect(url_for("login_business_page"))

def save_restaurant_image(img, username):
    _, extension = os.path.splitext(img.filename)
    for other_file in os.listdir(app.config['UPLOAD_FOLDER']):
        stem, other_extension = os.path.splitext(other_file)
        if username == stem:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], other_file))
    img.save(os.path.join(app.config['UPLOAD_FOLDER'], username + extension))


@app.route("/edit_time", methods=["GET", "POST"])
def edit_restaurant_time():
    if "user" in session and "business" in session:
        profile = database.get_restaurant(session["user"])
        profile["times"] = database.get_business_hours(session["user"])
        if request.method == "POST":
            for day in WEEKDAYS:
                Error = False
                if request.form["open_closed_" + day] == "open":
                    if database.check_time(request.form["openingTime_" + day], request.form["closingTime_" + day]):
                        database.update_business_hours(session["user"], day, request.form["openingTime_" + day], request.form["closingTime_" + day])
                    else:
                        Error = True
                        break
                elif request.form["open_closed_" + day] == "closed":
                    database.delete_business_hours(session["user"], day)

                profile = database.get_restaurant(session["user"])
                profile["times"] = database.get_business_hours(session["user"])
                    
            if Error:
                return render_template("edit_time.html", profile=profile, weekdays=WEEKDAYS, wrong_credentials=True)
            else:
                return render_template("edit_time.html", profile=profile, weekdays=WEEKDAYS, saved_changes=True)

            
        return render_template("edit_time.html", profile=profile, weekdays=WEEKDAYS)
    else:
        return redirect(url_for("login_business_page")) 
    
@app.route("/edit_delivery_radius", methods=["GET", "POST"])
def edit_restaurant_delivery_radius():
    if "user" in session and "business" in session:
        if request.method == "POST":
            print(request.form)
            if "submit new PLZ" in request.form:
                if database.check_plz(request.form["new PLZ"]):
                    database.update_lieferradius(request.form["new PLZ"], session["user"])
                    delivery_radius = database.get_delivery_radius(session["user"])
                    return render_template("edit_delivery_radius.html", delivery_radius=delivery_radius, saved_changes=True)
                else:
                    delivery_radius = database.get_delivery_radius(session["user"])
                    return render_template("edit_delivery_radius.html", delivery_radius=delivery_radius, invalid_plz=True)

            elif "delete PLZ" in request.form:
                database.delete_lieferradius(request.form["delete PLZ"], session["user"])
                delivery_radius = database.get_delivery_radius(session["user"])
                return render_template("edit_delivery_radius.html", delivery_radius=delivery_radius, deleted_changes=True)

        delivery_radius = database.get_delivery_radius(session["user"])
        return render_template("edit_delivery_radius.html", delivery_radius=delivery_radius)
    else:
        return redirect(url_for("login_business_page")) 
    
@app.route("/edit_menue", methods=["GET", "POST"])
def edit_restaurant_menue():
    if "user" in session and "business" in session:
        restaurant = database.get_restaurant(session["user"])
        items = database.get_items(session["user"])
        if request.method == "POST":
            if "add_button" in request.form:
                try:
                    database.create_item(session['user'], request.form["name"], request.form["category"], request.form["description"], request.form["price"])
                except Exception as err:
                    return render_template("edit_menue.html", restaurant=restaurant, items=items, error=err)
            elif "update_button" in request.form:
                database.update_item(request.form['id'], session['user'], request.form["name"], request.form["category"], request.form["description"], request.form["price"])
            elif "delete_button" in request.form:
                database.delete_item(request.form["id"])

        restaurant = database.get_restaurant(session["user"])
        items = database.get_items(session["user"])
        return render_template("edit_menue.html", restaurant=restaurant, items=items)
    else:
        return redirect(url_for("login_business_page")) 
    

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
        save_restaurant_image(request.files["image"], request.form["username"])
        
    if database.check_plz(request.form["postalcode"]) == False: return render_template("signup.html", business=True, invalid_plz=True)

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
        else:
            return render_template("login.html", wrong_credentials=True)
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
        else:
            return render_template("login.html", business=True, wrong_credentials=True)
    return render_template("login.html", business=True)

@app.route("/logout/")
def logout_page():
    session.pop("user", None)
    session.pop("business", None)
    return redirect(url_for("start_page"))

@app.route("/restaurants/")
def restaurants_page():
    if "user" in session and not "business" in session:
        day_index = datetime.datetime.now().weekday()
        restaurants = database.get_restaurants_near_and_open(session["user"], WEEKDAYS[day_index])
        image_names = os.listdir(app.config['UPLOAD_FOLDER'])
        image_tuples = list(map(os.path.splitext, image_names))
        for restaurant in restaurants:
            restaurant["image_path"] = DEFAULT_IMAGE
            for index, value in enumerate(image_tuples):
                if restaurant["username"] == value[0]:
                    restaurant["image_path"] = 'business/' + value[0] + value[1]
                    image_tuples.pop(index)
                    break
            
        return render_template("restaurants.html", restaurants=restaurants)
    
    elif "user" in session and "business" in session:
            restaurant = database.get_restaurant(session["user"])

            image_name = os.listdir(app.config['UPLOAD_FOLDER'])
            image_tuple = list(map(os.path.splitext, image_name))
            restaurant["image_path"] = DEFAULT_IMAGE

            for index, value in enumerate(image_tuple):
                if restaurant["username"] == value[0]:
                    restaurant["image_path"] = 'business/' + value[0] + value[1]
                    image_tuple.pop(index)
                    break

            return render_template("restaurant_preview.html", restaurant=restaurant)

    else:
        return redirect(url_for("login_customer_page"))
    

@app.route("/menue/<username>", methods=["GET", "POST"])
def menue_page(username):
    if "user" in session:
        restaurant = database.get_restaurant(username)
        restaurant["times"] = database.get_business_hours(username)
        image_names = os.listdir(app.config['UPLOAD_FOLDER'])
        image_tuples = list(map(os.path.splitext, image_names))
        restaurant["image_path"] = "test1.jpeg"
        for index, value in enumerate(image_tuples):
            if username == value[0]:
                restaurant["image_path"] = 'business/' + value[0] + value[1]
                image_tuples.pop(index)
                break

        items = database.get_items(username)
        return render_template("menue.html", restaurant=restaurant, items=items, weekdays=WEEKDAYS)
    else:
        return redirect(url_for("login_customer_page"))
    

@app.route("/menue_preview/<username>", methods=["GET", "POST"])
def menue_preview_page(username):
    if "user" in session:
        restaurant = database.get_restaurant(username)
        restaurant["times"] = database.get_business_hours(username)
        image_names = os.listdir(app.config['UPLOAD_FOLDER'])
        image_tuples = list(map(os.path.splitext, image_names))
        restaurant["image_path"] = "test1.jpeg"
        for index, value in enumerate(image_tuples):
            if username == value[0]:
                restaurant["image_path"] = 'business/' + value[0] + value[1]
                image_tuples.pop(index)
                break

        items = database.get_items(username)
        return render_template("menue_preview.html", restaurant=restaurant, items=items, weekdays=WEEKDAYS)
    else:
        return redirect(url_for("login_customer_page"))

    
@app.route("/orders", methods=["GET", "POST"])
def order_page():
    if "user" in session:
        if request.method == "POST":
                if "abschließen" in request.form:
                    status = "abgeschlossen"
                elif "akzeptieren" in request.form:
                    status = "in Zubereitung"
                else:
                    status = "storniert"

                database.update_orderstatus(request.form["orderid"], status)
        if "business" in session:
            orders = database.get_orders(session["user"], True)
            print(not orders)
            return render_template("orders_business.html", orders=orders)
        else:
            orders = database.get_orders(session["user"], False)
            return render_template("orders_customer.html", orders=orders)
    return redirect(url_for("login_customer_page"))

def get_items(mDict) -> list[dict]:
    ids = request.form.getlist("orderlist_ids")
    amounts = request.form.getlist("orderlist_amounts")
    items = []
    for id, amount in zip(ids, amounts):
        item = database.get_item(id)
        if item:
            item['amount'] = amount
            items.append(item)
    return items

@app.route("/confirm_order", methods=["POST"])
def confirm_order_page():
    if "user" in session and not "business" in session:
        restaurant = restaurant = database.get_restaurant(request.form["restaurant"])
        items = get_items(request.form)
        return render_template("confirm_order.html", restaurant=restaurant, items=items)
    else:
        return redirect(url_for("login_customer_page"))

@app.route("/place_order", methods=["GET", "POST"])
def place_order_page():
    if request.method == "GET":
        return render_template("error.html", error_message="GET Request nicht erlaubt")
    if "user" in session and not "business" in session:
        items = get_items(request.form)
        try:
            database.create_order(session["user"], request.form["restaurant"], items, request.form["comment"])
        except Exception as err:
            return render_template("error.html", error_message=err)
        return render_template("place_order.html")
    else:
        return redirect(url_for("login_customer_page"))

@app.route("/get_new_orders_amount", methods=["GET"])
def get_new_orders_amount():
    amount = 0
    if "user" in session and "business" in session:
        orders = database.get_orders(session['user'], business=True)
        for order in orders:
            if order['orderstatus'] == 'in Bearbeitung':
                amount += 1
    return {'amount': amount}


if __name__ == "__main__":
    app.run(debug=False)

