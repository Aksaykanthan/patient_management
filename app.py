from flask import Flask,request,render_template,redirect,url_for
import pymongo
# from user.routes import login_required

app = Flask(__name__)
app.secret_key = "medilink"

client = pymongo.MongoClient("localhost",27017,uuidRepresentation='standard')
db = client.Medilink



from models import Patient
from user import routes

@app.route("/")
def home():
    return render_template("home.html")


@app.route('/patient')
@routes.login_required
def patient():
    
    return render_template("patient/viewpatient.html",patients = db.patients)

@app.route('/patient/add',methods = ["GET","POST"])
@routes.login_required
def addpatient():
    if request.method == "POST":
        res,err = Patient(**request.form).create_patient()
        print(res.json)
        if err == 200:
            return redirect(url_for("patient/view",patient_id = res['id']))
        
        return redirect(url_for("addpatient",msg = res))
        # name = request.form.get("name")
        # email = request.form.get("email")
        # phone = request.form.get("phone")
        # address = request.form.get("address")
    return render_template("patient/addpatient.html")