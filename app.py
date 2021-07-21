from flask import Flask, redirect, render_template, session, request, flash
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology

app = Flask(__name__)

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

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        #TODO, QUERY DB for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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

        #TODO, SQL here
        users = db.execute("SELECT username FROM users")

        #error checking
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif request.form.get("username") in [user["username"] for user in users]:
            #each user is represented by a dict, in the whole list. the list is the value returned by db.execute("---") assigned to the variable users.
            #user["username"] returns the username for each user(represented by dict) in the users (represented by list)
            #hence the list comprehension gets a list of all available usernames.
            return apology("that username already exists", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Password and Confirmation password do not match", 400)

        #if nothing goes wrong, remember to hash password, then update users. no need to update cash as theres a default value for every new row:
        else:
            #TODO: SQL HERE
            db.execute("INSERT INTO users (username, hash) VALUES (?,?)", request.form.get("username"), generate_password_hash(request.form.get("password")))
            flash("Log in with your new account!")
            return redirect("/login")
    else:
        #this handles GET requests. condition "else " is used because GET is the only other request method other than POST here.
        return render_template("register.html")
        