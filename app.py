from cgitb import reset
from flask import Flask,request,render_template,redirect, session,url_for
import pymongo


app = Flask(__name__)
app.secret_key = "medilink"

client = pymongo.MongoClient("localhost",27017,uuidRepresentation='standard')
db = client.Medilink

from models import Doctor, Patient, Hospital, Medicine, Session, Specialization,Report,GeneralTest,BloodTest
from user import routes

@app.route("/")
def home():
    return render_template("home.html", hospitals = Hospital.view_hospitals(),doctors = Doctor.view_doctors(),specializations = Specialization.view_specializations())

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

@app.route("/patient/verify",methods = ["GET","POST"])
def verifypatient():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        res,err = Patient.verify_patient(email,name)
        if err == 200:
            return redirect(url_for("detailpatient",_id = res.json.get("_id")))
        
        return redirect(url_for("verifypatient",msg = res.json.get("des"),_type=err))
    
    return render_template("patient/verifypatient.html")


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
    return render_template("doctor/viewdoctor.html", doctors = Doctor.view_doctors(),specializations = Specialization.view_specializations())

@app.route("/doctor/add",methods = ["GET","POST"])
def adddoctor():
    if request.method == "POST":
        _id = session.get("user").get("_id")
        name = session.get("user").get("name")
        email = session.get("user").get("email")
        res,err = Doctor(name=name,email=email,**request.form).create_doctor(_id)
        hospital_id = request.form.get("hospital")
        if err == 200:
            Hospital.add_doctor(_id,hospital_id)
            return redirect(url_for("detaildoctor",_id = res.json.get("id"),msg = res.json.get("des"),_type=err,hospitals = Hospital.view_hospitals()))
        
        return redirect(url_for("adddoctor",msg = res.json.get("des"),_type=err,hospitals = Hospital.view_hospitals()))
    
    return render_template("doctor/adddoctor.html",hospitals = Hospital.view_hospitals())

@app.route("/doctor/detail")
def detaildoctor():
    _id = request.args.get("_id")
    doctor = Doctor.get_doctor(_id)
    return render_template("doctor/detaildoctor.html",doctor=doctor)

@app.route("/doctor/review",methods = ["GET","POST"])
def addreview():
    if request.method == "POST":
        _id = request.args.get("_id")
        name = request.form.get("name")
        review = request.form.get("review")
        Doctor.add_review(_id,{"name":name,"review":review})
        
        return redirect(url_for("detaildoctor",_id = _id))

    return render_template("doctor/review.html")


@app.route("/doctor/filter",methods = ["GET","POST"])
def filterdoctor():
    if request.method == "GET":
        specialization = request.args.get("specialization")

        return render_template("doctor/viewdoctor.html", doctors = Doctor.view_doctors({"specialization":specialization}),specializations = Specialization.view_specializations(),specialization = specialization)

    
    return redirect(url_for("doctor"))

# ---------- MEDICINE ROUTES ------------

@app.route("/medicine")
def medicine():
    return render_template("medicine/viewmedicine.html", medicines = Medicine.view_medicines())

@app.route("/medicine/add",methods = ["GET","POST"])
def addmedicine():
    if request.method == "POST":
        res,err = Medicine(**request.form).create_medicine()
        if err == 200:
            return redirect(url_for("detailmedicine",_id = res.json.get("id"),msg = res.json.get("des"),_type=err))
        
        return redirect(url_for("addmedicine",msg = res.json.get("des"),_type=err))
    
    return render_template("medicine/addmedicine.html")

@app.route("/medicine/detail")
def detailmedicine():
    _id = request.args.get("_id")
    medicine = Medicine.get_medicine(_id)
    return render_template("medicine/detailmedicine.html",medicine=medicine)

# ---------- SESSION ROUTES ------------
@app.route("/addsession",methods = ["GET","POST"])
def addsession():
    if request.method == "POST":
        patient_id = request.args.get("_id")
        doctor_id = session.get("user").get("_id")
        count = request.form.get("count")
        subject = request.form.get("subject")
        followup = request.form.get("followup")
        details = request.form.get("details")
        prescription = Session.create_medicines(count,request.form)
        print(request.form)
        res,err = Session(subject,details,followup,prescription).create_session(patient_id,doctor_id)
        if err == 200:
            return redirect(url_for("detailpatient",_id = patient_id,msg = res.json.get("des"),_type=err))

    return render_template("session/addsession.html",meds = Medicine.view_medicines())

@app.route("/detailsession",methods = ["GET","POST"])
def detailsession():
    session_id = request.args.get("session_id")
    patient_id = request.args.get("patient_id")
    session = Session.get_session(patient_id,session_id)
    return render_template("session/detailsession.html",session=session)

# --------- SPECIALIZATION ROUTES ------------
@app.route("/specialization")
def specialization():
    return render_template("specialization/viewspecialization.html",specializations = list(db.specializations.find({})))


@app.route("/specialization/add",methods = ["GET","POST"])
def addspecialization():
    if request.method == "POST":
        res,err = Specialization(request.form.get("name")).create_specialization()
        return redirect(url_for("specialization",msg = res.json.get("des"),_type=err))
    
    return render_template("specialization/addspecialization.html")

# --------- TEST REPORT ROUTES ------------
@app.route("/addbloodreport",methods = ["GET","POST"])
def addbloodreport():
    if request.method == "POST":
        patient_id = request.args.get("_id")
        doctor_id = session.get("user").get("_id")
        res,err = BloodTest(doctor_id=doctor_id,reporttype="Blood Test",patient_id=patient_id,**request.form).create_report()
        if err == 200:
            return redirect(url_for("detailpatient",_id = patient_id,msg = res.json.get("des"),_type=err))

    return render_template("reports/bloodreport.html")

@app.route("/addgeneralreport",methods = ["GET","POST"])
def addgeneralreport():
    if request.method == "POST":
        patient_id = request.args.get("_id")
        doctor_id = session.get("user").get("_id")
        res,err = GeneralTest(doctor_id=doctor_id,reporttype="General Test",patient_id=patient_id,**request.form).create_report()
        if err == 200:
            return redirect(url_for("detailpatient",_id = patient_id,msg = res.json.get("des"),_type=err))

    return render_template("reports/generalreport.html")

@app.route("/detailreport",methods = ["GET","POST"])
def detailreport():
    report_id = request.args.get("report_id")
    patient_id = request.args.get("patient_id")
    report = Report.get_report(patient_id,report_id)

    if report.get("type") == "Blood Test":
        return render_template("reports/detailbloodreport.html",report=report)
    elif report.get("type") == "General Test":
        return render_template("reports/detailgeneralreport.html",report=report)
    else:
        return redirect(url_for("detailpatient",_id=patient_id))

# ------------- JINJA FILTERS ------------
@app.context_processor
def utility_processor():
    def get_doctorname(_id):
        return Doctor.get_doctorname(_id)
    def get_hospitalname(_id):
        return Hospital.get_hospitalname(_id)
    def get_hospital(_id):
        return Hospital.get_hospital(_id)
    def get_doctor(_id):
        return Doctor.get_doctor(_id)
    def get_allspecialization():
        return Specialization.view_specializations()
    def get_patientname(_id):
        return Patient.get_patientname(_id)
    def get_medicinename(_id):
        return Medicine.get_medicinename(_id)
    
    return dict(get_patientname=get_patientname,get_doctorname=get_doctorname,get_hospitalname=get_hospitalname,get_hospital=get_hospital,get_doctor=get_doctor,get_allspecialization=get_allspecialization,get_medicinename=get_medicinename)
