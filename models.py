
from flask import jsonify, session
import uuid
from app import db
import datetime

class User:
    def __init__(self,name:str,password:str,email:str,gender:str,phoneno:str) -> None:
        self.name = name
        self.email = email
        self.password = password
        self.gender = gender
        self.phoneno = phoneno

    def __str__(self) -> str:
        return f"Name: {self.name}"

class Patient(User):
    def __init__(self,name:str,email:str,gender:str,phonenumber:str,dob, bloodgroup:str,address:str,password:str=None):
        super().__init__(name,password,email,gender,phonenumber)
        self.dob = dob
        self.address = address
        self.bloodgroup = bloodgroup
        self.session = []
        self.report = []
    
    def create_patient(self):
        patient = {
            "_id" : uuid.uuid4().hex,
            "name": self.name,
            "password":self.password,
            "email":self.email,
            "gender":self.gender,
            "phoneno":self.phoneno,
            "dob":self.dob,
            "bloodgroup":self.bloodgroup,
            "address" : self.address
            }
        
        if db.patients.find_one({'email': patient['email']}):
            return jsonify({"des":"Patient Already exists","type":"danger"}),400

        if db.patients.insert_one(patient):
            return jsonify({"des": "Patient Has Been Registered Successfully","type":"success","id":patient['_id']}),200
        
        return jsonify({"des":"Registration failed","type":"danger"}),400
    
    @staticmethod
    def view_patients():
        return list(db.patients.find({}))

    @staticmethod
    def get_patient(_id):
        return db.patients.find_one({"_id":_id})
    
    @staticmethod
    def get_patientname(_id):
        return db.patients.find_one({"_id":_id}).get("name")
    
    @staticmethod
    def verify_patient(email,name):
        patient = db.patients.find_one({"email":email,"name":name})
        if patient:
            return jsonify(patient),200
        return jsonify({"des":"Patient Not Found","type":"danger"}),400


class Hospital:
    def __init__(self,name:str,email:str,phonenumber:str,location:str):
        self.name = name
        self.email = email
        self.phoneno = phonenumber
        self.location = location
        self.doctors = []
    
    def create_hospital(self):
        hospital = {
            "_id" : uuid.uuid4().hex,
            "name": self.name,
            "email": self.email,
            "phoneno": self.phoneno,
            "location": self.location,
            "doctors": self.doctors
        }

        if db.hospitals.find_one({'email': hospital['email']}):
            return jsonify({"des":"Hospital Already exists","type":"danger"}),400

        if db.hospitals.insert_one(hospital):
            return jsonify({"des": "Hospital Has Been Registered Successfully","type":"success","id":hospital['_id']}),200

        return jsonify({"des":"Registration failed","type":"danger"}),400

    @staticmethod
    def add_doctor(doctor_id,hospital_id):
        db.hospitals.update_one({"_id": hospital_id},{"$push": {"doctors": doctor_id}},)
        return jsonify({"des":"Doctor Added Successfully","type":"success"}),200
    
    @staticmethod
    def get_hospitalname(_id):
        return db.hospitals.find_one({"_id":_id}).get("name")
    
    @staticmethod
    def view_hospitals():
        return list(db.hospitals.find({}))
    
    @staticmethod
    def get_hospital(_id):
        return db.hospitals.find_one({"_id":_id})


class Doctor(User):
    def __init__(self,name:str,email:str,gender:str,phonenumber:str,dob, graduation,degree:str,specialization:str,hospital:str,password:str=None):
        super().__init__(name,password,email,gender,phonenumber)
        self.dob = dob
        self.graduation = graduation
        self.degree = degree
        self.specialization = specialization
        self.reviews = []
        self.ratings = 0
        self.hospital = hospital
        self.session = []
    
    def create_doctor(self,_id):
        doctor = {
            "_id" : _id,
            "name": self.name,
            "password":self.password,
            "email":self.email,
            "gender":self.gender,
            "phoneno":self.phoneno,
            "dob":self.dob,
            "specialization" : self.specialization,
            "graduation":self.graduation,
            "degree":self.degree,
            "reviews":self.reviews,
            "hospital":self.hospital,
            }
        
        if db.doctors.find_one({'_id': doctor['_id']}):
            return jsonify({"des":"Doctor Already exists","type":"danger"}),400
        if db.doctors.insert_one(doctor):
            if not db.hospitals.find_one({"_id": doctor["hospital"]}):
                db.hospitals.update_one({"_id": doctor["hospital"]},{"$push": {"doctors": doctor['_id']}},)
            return jsonify({"des": "Doctor Has Been Registered Successfully","type":"success","id":doctor['_id']}),200
        
        return jsonify({"des":"Registration failed","type":"danger"}),400
    
    @staticmethod
    def get_doctorname(_id):
        return db.doctors.find_one({"_id":_id}).get("name")
    
    @staticmethod
    def view_doctors(spec = {}):
        return list(db.doctors.find(spec))

    @staticmethod
    def get_doctor(_id):
        return db.doctors.find_one({"_id":_id})
    
    @staticmethod
    def add_review(_id,review):
        doctor = db.doctors.find_one({"_id":_id})
        review['date'] = datetime.datetime.now().strftime("%x")
        doctor['reviews'].append(review)
        db.doctors.update_one({"_id":_id},{"$set":doctor})
        return jsonify({"des":"Review Added Successfully","type":"success"}),200



class Medicine:
    def __init__(self,name:str,description:str,note:str=None):
        self.name = name
        self.description = description
        self.note = note
    
    def create_medicine(self):
        medicine = {
            "_id" : uuid.uuid4().hex,
            "name": self.name,
            "description":self.description,
            "note": self.note
            }
        
        if db.medicines.find_one({'name': medicine['name']}):
            return jsonify({"des":"Medicine Already exists","type":"danger"}),400

        if db.medicines.insert_one(medicine):
            return jsonify({"des": "Medicine Has Been Registered Successfully","type":"success","id":medicine['_id']}),200
        
        return jsonify({"des":"Registration failed","type":"danger"}),400

    @staticmethod
    def view_medicines():
        return list(db.medicines.find({}))

    @staticmethod
    def get_medicine(_id):
        return db.medicines.find_one({"_id":_id})
    
    @staticmethod
    def get_medicinename(_id):
        return Medicine.get_medicine(_id).get("name")


class Session:
    def __init__(self,subject:str,details:str,followup:str,prescription:list=[]):
        self.subject = subject
        self.details = details
        self.prescription = prescription
        self.followup = followup
        self.current = datetime.datetime.now()
        self.time = self.current.strftime("%X")
        self.date = self.current.strftime("%x")

    def create_session(self,patient_id,doctor_id):
        self.doctor_id = doctor_id
        self.hospital_id = db.doctors.find_one({"_id": doctor_id}).get("hospital")
        session = {
            "_id" : uuid.uuid4().hex,
            "doctor":self.doctor_id,
            "hospital":self.hospital_id,
            "subject":self.subject,
            "details":self.details,
            "prescription":self.prescription,
            "followup":self.followup,
            "time":self.time,
            "date":self.date,
            }
        db.patients.update_one({"_id": patient_id},{"$push": {"session": session}},)
        session["patient_id"] = patient_id
        db.doctors.update_one({"_id": self.doctor_id},{"$push": {"session": session}},)
        return jsonify({"des":"Session Created Successfully","type":"success"}),200
    
    @staticmethod
    def create_medicines(count,extra):
        prescription = []
        for i in range(int(count)):
            # Construct key strings dynamically using i
            medicine_key = "medicine" + str(i)
            morning_key = "morning" + str(i)
            afternoon_key = "afternoon" + str(i)
            night_key = "night" + str(i)

            # Use get method to retrieve values with default False
            medicine = extra.get(medicine_key, None)  # None as default
            morning = True if extra.get(morning_key, False) else False
            afternoon = True if extra.get(afternoon_key, False) else False
            night = True if extra.get(night_key, False) else False

            med = Prescription(medicine,morning,afternoon,night).create_prescription()
            prescription.append(med)
        return prescription


    
    @staticmethod
    def get_session(patient_id,session_id):
        session = db.patients.find_one({"_id": patient_id, "session": { "$elemMatch": {"_id": session_id}}}, projection={"session": {"$elemMatch": {"_id": session_id}}})
        return session["session"][0]


class Prescription:
    def __init__(self,medicine:str,morning:bool,evening:bool,night:bool):
        self.medicine = medicine
        self.morning = morning
        self.evening = evening
        self.night = night

    def create_prescription(self):
        prescription = {
            "medicine":self.medicine,
            "morning":self.morning,
            "evening":self.evening,
            "night":self.night,
        }
        return prescription


class Specialization:
    def __init__(self,name:str):
        self.specialization = name
    
    def create_specialization(self):
        specialization = {
            "_id" : uuid.uuid4().hex,
            "name": self.specialization,
        }
        
        if db.specializations.find_one({'name': specialization['name']}):
            return jsonify({"des":"Specialization Already exists","type":"danger"}),400

        if db.specializations.insert_one(specialization):
            return jsonify({"des": "Specialization Has Been Registered Successfully","type":"success"}),200
        
        return jsonify({"des":"Registration failed","type":"danger"}),400

    @staticmethod
    def view_specializations():
        return list(db.specializations.find({}))

    @staticmethod
    def get_specialization(_id):
        return db.specializations.find_one({"_id":_id})
    
class Report:
    def __init__(self,reporttype:str,details:str,):
        self.type = reporttype
        self.details = details
        self.current = datetime.datetime.now()
        self.time = self.current.strftime("%X")
        self.date = self.current.strftime("%x")

    def create_report(self,doctor_id):
        self.doctor_id = doctor_id
        self.hospital_id = db.doctors.find_one({"_id": doctor_id}).get("hospital")
        report = {
            "_id" : uuid.uuid4().hex,
            "type":self.type,
            "time":self.time,
            "date":self.date,
            "doctor":self.doctor_id,
            "hospital":self.hospital_id,
            "details":self.details,
            }
        return report
    
    @staticmethod
    def get_report(patient_id,report_id):
        report = db.patients.find_one({"_id": patient_id, "reports": { "$elemMatch": {"_id": report_id}}}, projection={"reports": {"$elemMatch": {"_id": report_id}}})
        return report["reports"][0]


class BloodTest(Report):
    def __init__(self,doctor_id:str,reporttype:str,patient_id:str,details:str,bloodgroup:str,rbc:str,wbc:str,pc:str,hemoglobin:str,glucose:str,colestrol:str):
        super().__init__(reporttype,details)        
        self.report = super().create_report(doctor_id)
        self.bloodgroup = bloodgroup
        self.rbc = rbc
        self.wbc = wbc
        self.pc = pc
        self.hemoglobin = hemoglobin
        self.glucose = glucose
        self.colestrol = colestrol
        self.patient_id = patient_id
    
    def create_report(self):
        self.report["bloodgroup"] = self.bloodgroup
        self.report["rbc"] = self.rbc
        self.report["wbc"] = self.wbc
        self.report["pc"] = self.pc
        self.report["hemoglobin"] = self.hemoglobin
        self.report["glucose"] = self.glucose
        self.report["colesterol"] = self.colestrol

        db.patients.update_one({"_id": self.patient_id},{"$push": {"reports": self.report}},)
        return jsonify({"des":"Session Created Successfully","type":"success"}),200
    
class GeneralTest(Report):
    def __init__(self,doctor_id:str,reporttype:str,patient_id:str,details:str,temperature:str,heartrate:str,bloodpressure:str,weight:str,height:str):
        super().__init__(reporttype,details)
        self.report = super().create_report(doctor_id)
        self.temperature = temperature
        self.heartrate = heartrate
        self.bloodpressure = bloodpressure
        self.weight = weight
        self.height = height
        self.patient_id = patient_id
    
    def create_report(self):
        self.report["temperature"] = self.temperature
        self.report["heartrate"] = self.heartrate
        self.report["bloodpressure"] = self.bloodpressure
        self.report["weight"] = self.weight
        self.report["height"] = self.height

        db.patients.update_one({"_id": self.patient_id},{"$push": {"reports": self.report}},)
        return jsonify({"des":"Session Created Successfully","type":"success"}),200
    