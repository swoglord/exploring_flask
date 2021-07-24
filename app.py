from flask import Flask, redirect, render_template, session, request, flash
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key='test'
#configure database connected to mysql (used phpmyadmin)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/linklearn'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#users is basically the table. 
#allows u to call on its attributes for each piece of data about a user. e.g. user.id
class users(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.Text, nullable=False)
    hash = db.Column("hash", db.Text, nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    """Log user in"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Forget any user_id
        session.clear()
        username = request.form.get('username')
        password = request.form.get('password')

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)

        #identify the user that is attempting to login bassed on username:
        user = users.query.filter_by(username=username).first()

        # Ensure username exists and password is tagged to username!:
        if not user or not check_password_hash(user.hash, password):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = user.id

        # Redirect user to home page
        flash("Log-in successful!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        #above condition must be put because by default, method is GET.
        #and when they first enter the website, it's a GET request. so you shouldn't check for inputs.
        #only check the user inputs when the request.method is POST
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

           #error checking: we expect user to return None if the username does not yet exist in users.
        user = users.query.filter_by(username=username).first()
    
        #error checking
        if not username:
            return apology("must provide username", 400)
        #if not 404, means a user exists with this username, hence return apology.
        elif user != None:
            return apology("that username already exists", 400)
        elif not password:
            return apology("must provide password", 400)
        elif password != confirm_password:
            return apology("Password and Confirmation password do not match", 400)

        #if nothing goes wrong, remember to hash password, then update users. 
        #create new user instance with username and corresponding pword hash, then add to db, then commit change.
        user = users(username=username, hash=generate_password_hash(password)) 
        db.session.add(user)
        db.session.commit()
        flash("Log in with your new account!")
        return redirect("/login")
    else:
        #this handles GET requests. condition "else " is used because GET is the only other request method other than POST here.
        return render_template("register.html")