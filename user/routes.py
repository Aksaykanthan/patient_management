from functools import wraps
from flask import Flask,render_template,request,redirect,url_for,session
from app import app
from user.models import User


def login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            return redirect(url_for("home"))
    return wrap

@app.route("/user/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        res,error = User(**{"name":"","email":email,"password":password}).signin()
        if error == 200:
            return redirect(url_for("dashboard"))
        else:
            return render_template("auth/login.html",msg = res)
    
    return render_template("auth/login.html")


@app.route("/user/signup",methods=["POST","GET"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        
        res,error = User(**{'name':name,"email":email,"password":password}).signup()
        if error == 200:
            return render_template("auth/login.html",msg = res)
            # return redirect(url_for("login",msg = res))
        else:
            return render_template("auth/register.html",msg = res)
            # return redirect(url_for("signup",msg = res))
    
    return render_template("auth/register.html")


@app.route("/user/signout",methods=["POST","GET"])
def signout():
    User.signout()
    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")