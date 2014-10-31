from flask import Flask, render_template, redirect, request, flash, session
import model
import jinja2


app = Flask(__name__)
app.secret_key = "kjsgajjhueajkbgjkshfj"
app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def render_login():
	return render_template("login.html")

@app.route("/signup")
def signup_form():
	return render_template("signup_form.html")

@app.route("/users")
def index():
    user_list = model.session.query(model.User).limit(15).all()
    return render_template("user_list.html", users = user_list)


@app.route("/ratinglist")
def rating_list():
	#home
	user = model.session.query(model.User).filter_by(id=session['user_id']).one()
	print "User is", user
	rating_list = model.session.query(model.Rating).filter_by(user_id = session['user_id']).all()
	print "Rating List", rating_list
	# print rating_list[0].rating_list
	return render_template("user_rating.html", rating_list = rating_list, user=user)

@app.route("/signup", methods = ["POST"])
def user_signup():
	email = request.form.get("email")
	password = request.form.get("password")
	age = request.form.get("age")
	zipcode = request.form.get("zipcode")
	check_for_dupes = model.session.query(model.User).filter_by(email = email).all()
	print check_for_dupes
	if check_for_dupes == []:
		user = model.User()
		user.email = email
		user.age = age
		user.zipcode = zipcode
		user.password = password
		print user
		model.session.add(user)
		model.session.commit()
		flash("Welcome and please login to begin!")

		return render_template("login.html")
	else:
		flash("I'm sorry but this email address already exists in our records. Please use a different email address.")
		return render_template("login.html")


@app.route("/login", methods = ["POST"])
def login():
	email = request.form.get("email")
	password = request.form.get("password")
	login_user = model.session.query(model.User).filter_by(email = email).all()
	print "/login", login_user
	if login_user == []:  # true if we found anything
		flash("You are not in our records. Please sign up.")
		return redirect("/signup")

	if login_user[0].password != password:
		flash("Your password does not match our records. Please try again.")
		print "/login wrong password", login_user[0].password, password
		return redirect("/")   # GET
	else:
		session['user_id'] = login_user[0].id
		print session
		flash("Welcome!")
		return redirect("/ratinglist")

@app.route("/movies")
def movies_page():
	movie_list = model.session.query(model.Movie).all()
	return render_template("movie_list.html", movie_list=movie_list)

@app.route("/newrating/<int:id>")   # /newrating/17
def new_rating_form(id):
	movie = model.session.query(model.Movie).filter_by(id = id).first()
	title = movie.name
	return render_template("new_rating_form.html", title=title, movie_id=id)

@app.route("/savenew", methods = ["POST"])
def save_new_rating():
	movie_id = request.form.get("movie_id")
	movie_title = request.form.get("movie_title")
	rating = request.form.get("rating")
	newrating = model.Rating()
	newrating.rating = rating
	newrating.movie_id = movie_id
	newrating.user_id = session["user_id"]
	model.session.add(newrating)
	model.session.commit()
	flash("Thank you for rating %s", movie_title)
	return redirect("/ratinglist")

@app.route("/saveupdate", methods = ["Post"])
def save_update():
	movie_title = request.form.get("title")
	movie_id = request.form.get("movie_id")
	rating = request.form.get("rating")
	rating_object = model.session.query(model.Rating).filter_by(movie_id=movie_id).filter_by(user_id=session['user_id']).first()
	rating_object.rating = rating
	model.session.commit()
	flash("Thank you for rating %s", movie_title)
	return redirect("/ratinglist")


@app.route("/updaterating/<int:id>")
def rating_update_form(id):
	movie = model.session.query(model.Movie).filter_by(id=id).one()
	title = movie.name
	return render_template("rating_form.html", title = title, movie_id=id)



if __name__ == "__main__":
    app.run(debug = True)
