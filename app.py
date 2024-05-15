from flask import Flask,request,render_template,redirect,url_for
import pymongo

app = Flask(__name__)
app.secret_key = "medilink"

client = pymongo.MongoClient("localhost",27017,uuidRepresentation='standard')
db = client.Medilink

from models import Patient,Hospital
from user import routes

@app.route("/")
def home():
    return render_template("home.html")

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
            return redirect(url_for("detailpatient",_id = res.json.id))
        
        return redirect(url_for("addpatient",msg = res))

    return render_template("patient/addpatient.html")

@app.route("/patient/detail")
def detailpatient():
    _id = request.args.get("_id")
    return render_template("patient/detailpatient.html",patient = Patient.get_patient(_id))

# --------- hOSPITAL ROUTES ------------

@app.route("/hospital")
def hospital():
    
    return render_template("hospital/viewhospital.html", hospitals = Hospital.view_hospitals())

@app.route("/hospital/add",methods = ["GET","POST"])
def addhospital():
    if request.method == "POST":
        res,err = Hospital(**request.form).create_hospital()
        if err == 200:
            return redirect(url_for("detailhospital",_id = res.json.id,msg = res))
        
        return redirect(url_for("addhospital",msg = res))
    
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
    return render_template("doctor.html")

@app.route("/doctor/add")
def adddoctor():
    return render_template("adddoctor.html")

@app.route("/doctor/detail")
def detaildoctor():
    return render_template("detaildoctor.html")


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

