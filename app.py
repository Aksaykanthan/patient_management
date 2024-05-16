from flask import Flask,request,render_template,redirect, session,url_for,flash
import pymongo

app = Flask(__name__)
app.secret_key = "medilink"

client = pymongo.MongoClient("localhost",27017,uuidRepresentation='standard')
db = client.Medilink

from models import Doctor, Patient,Hospital
from user import routes

@app.route("/")
def home():
    return render_template("home.html")

# --------- PATIENT ROUTES ------------

@app.route('/patient')
@routes.login_required
def patient():
    return render_template("patient/viewpatient.html",patients = Patient.view_patients())

@app.route('/patient/add',methods = ["GET","POST"])
@routes.login_required
def addpatient():
    if request.method == "POST":
        res,err = Patient(**request.form).create_patient()
        # print(res.json.id)
        if err == 200:
            return redirect(url_for("detailpatient",_id = res.json.get("id"),msg = res.json.get("des"),_type=err))
        
        return redirect(url_for("addpatient",msg = res.json.get("des"),_type=err))

    return render_template("patient/addpatient.html")

@app.route("/patient/detail")
def detailpatient():
    _id = request.args.get("_id")
    return render_template("patient/detailpatient.html",patient = Patient.get_patient(_id))

# --------- HOSPITAL ROUTES ------------

@app.route("/hospital")
def hospital():
    return render_template("hospital/viewhospital.html", hospitals = Hospital.view_hospitals())

@app.route("/hospital/add",methods = ["GET","POST"])
def addhospital():
    if request.method == "POST":
        res,err = Hospital(**request.form).create_hospital()
        if err == 200:
            # flash(res.json.get("des"),res.json.get("type"))
            return redirect(url_for("detailhospital",_id = res.json.get("id"),msg = res.json.get("des"),_type=err))
        
        return redirect(url_for("addhospital",msg = res.json.get("des"),_type=err))
    
    return render_template("hospital/addhospital.html")

@app.route("/hospital/detail",methods = ["GET","POST"])
def detailhospital():
    _id = request.args.get("_id")
    hospital = Hospital.get_hospital(_id)
    doctors = hospital.get("doctors")
    # doctors = [Doctor.get_doctor(doctor) for doctor in hospital["doctors"]]
    return render_template("hospital/detailhospital.html",hospital = hospital,doctors = doctors)


# --------- DOCTOR ROUTES ------------

@app.route("/doctor")
def doctor():
    return render_template("doctor/viewdoctor.html", doctors = Doctor.view_doctors())

@app.route("/doctor/add",methods = ["GET","POST"])
def adddoctor():
    if request.method == "POST":
        _id = session.get("user").get("_id")
        name = session.get("user").get("name")
        email = session.get("user").get("email")
        res,err = Doctor(name=name,email=email,**request.form).create_doctor(_id)
        if err == 200:
            return redirect(url_for("detaildoctor",_id = res.json.get("id"),msg = res.json.get("des"),_type=err,hospitals = Hospital.view_hospitals()))
        
        return redirect(url_for("adddoctor",msg = res.json.get("des"),_type=err,hospitals = Hospital.view_hospitals()))
    
    return render_template("doctor/adddoctor.html",hospitals = Hospital.view_hospitals())

@app.route("/doctor/detail")
def detaildoctor():
    _id = request.args.get("_id")
    doctor = Doctor.get_doctor(_id)
    return render_template("doctor/detaildoctor.html",doctor=doctor)


# ---------- MEDICINE ROUTES ------------
@app.route("/medicine")
def medicine():
    return render_template("medicine.html")

@app.route("/medicine/add")
def addmedicine():
    return render_template("addmedicine.html")

@app.route("/medicine/detail")
def detailmedicine():
    return render_template("detailmedicine.html")

