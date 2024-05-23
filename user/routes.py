from functools import wraps
from flask import Flask,render_template,request,redirect,url_for,session
from app import app,db
from user.models import User

from models import Doctor

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
        
        res,err = User(**{"name":"","email":email,"password":password}).signin()
        print(res.json.get("_id"))
        if err == 200:
            if db.doctors.find_one({'_id': res.json.get("_id")}):
                return redirect(url_for("dashboard"))
            return redirect(url_for("adddoctor"))
        else:
            return redirect(url_for("login",msg = res.json.get("des"),_type=err))
    
    return render_template("auth/login.html")


@app.route("/user/signup",methods=["POST","GET"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        
        res,err = User(**{'name':name,"email":email,"password":password}).signup()
        if err == 200:
            return redirect(url_for("login",msg = res.json.get("des"),_type=err))
            # return redirect(url_for("login",msg = res.json))
        return redirect(url_for("signup",msg = res.json.get("des"),_type=err))
            # return redirect(url_for("signup",msg = res.json))
    
    return render_template("auth/register.html")


@app.route("/user/signout",methods=["POST","GET"])
def signout():
    User.signout()
    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required
def dashboard():
    _id = session.get("user").get("_id")
    doctor = Doctor.get_doctor(_id)
    print(doctor)
    return render_template("dashboard.html",doctor=doctor)