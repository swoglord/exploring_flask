from datetime import datetime
from tempfile import mkdtemp
from flask import Flask, redirect, render_template, session, request, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import (HTTPException, InternalServerError,
                                 default_exceptions)
from helpers import apology, login_required
from flask_sqlalchemy import SQLAlchemy
import os
import re

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#configure database connected to mysql (used phpmyadmin)
#'mysql://root@localhost/linklearn' is the URI for local mySQL database

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
# rest of connection code using the connection string `uri`
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

class links(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.Text, nullable=False)
    url = db.Column("url", db.Text, nullable=False)
    nickname = db.Column("nickname", db.Text, nullable=False)
    description = db.Column("description", db.Text, nullable=False)
    timestamp = db.Column("timestamp", db.DateTime, nullable=False)
    deleted = db.Column("deleted", db.Boolean, default=False, nullable=False)
    permdeleted = db.Column("permdeleted", db.Boolean, default=False, nullable=False)


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
        session["username"] = user.username
        # Redirect user to home page
        flash("Log-in successful!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

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

@app.route('/', methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        if request.form.get("delete"):
            link_id = request.form.get("link_id")
            link_to_delete = links.query.filter_by(id=link_id).first()
            link_to_delete.deleted = True
            db.session.commit()
            flash("You deleted the link, {link}! It's now in your trash and you can restore it or permanently delete it as you wish.".format(link=link_to_delete.nickname))
            return redirect('/trash')
        if request.form.get("save_desc"):
            link_id = request.form.get("link_id")
            new_description = request.form.get("description"+"_"+link_id)
            link = links.query.filter_by(id=link_id).first()
            link.description = new_description
            db.session.commit()
            flash("You edited and saved a description!")
            return redirect("/")
    user_links = links.query.filter_by(username=session["username"]).all()
    return render_template("index.html", user_links=user_links, username=session["username"])


@app.route('/add', methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        # error checking - figure out how to check if a url is a valid link - learn about regex!
        #TODO
        username = session["username"]
        url = request.form.get("url")
        nickname = request.form.get("nickname")
        description = request.form.get("description")
        if not url or not nickname or not description:
            return apology("You must fill in all fields to add in a link!")
        #if nothing wrong, add this link to the table, links!
        timestamp = datetime.now()
        link = links(username=username, url=url, nickname=nickname, description=description, timestamp=timestamp)
        db.session.add(link)
        db.session.commit()
        flash("You added a new link, {nickname}!".format(nickname=link.nickname))
        return redirect("/")
    return render_template("add.html")

@app.route("/history")
@login_required
def history():
    user_links = links.query.filter_by(username=session["username"]).all()
    return render_template("history.html", user_links=user_links)

@app.route("/trash", methods=['GET','POST'])
@login_required
def trash():
    if request.method == "POST":
        if request.form.get("restore"):
            restore_id = request.form.get("restore_id")
            link_to_restore = links.query.filter_by(id=restore_id).first()
            link_to_restore.deleted = False
            db.session.commit()
            flash("You restored the link, {link}!".format(link=link_to_restore.nickname))
            return redirect('/')
        elif request.form.get("delete"):
            delete_id = request.form.get("delete_id")
            link_to_delete = links.query.filter_by(id=delete_id).first()
            nickname = link_to_delete.nickname
            link_to_delete.permdeleted = True
            db.session.commit()
            flash("You permanently deleted the link, {nickname}!".format(nickname=nickname))
            return redirect('/trash')
    user_links = links.query.filter_by(username=session["username"]).all()
    return render_template("trash.html", user_links=user_links)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

