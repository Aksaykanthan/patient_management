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
        hospital = db.hospitals.find_one({"_id":hospital_id})
        hospital['doctors'].append(doctor_id)
        db.hospitals.update_one({"_id":hospital_id},{"$set":hospital})
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
            db.hospitals.update_one({"_id": doctor["hospital"]},{"$push": {"doctors": doctor['_id']}},)
            return jsonify({"des": "Doctor Has Been Registered Successfully","type":"success","id":doctor['_id']}),200
        
        return jsonify({"des":"Registration failed","type":"danger"}),400
    
    @staticmethod
    def get_doctorname(_id):
        return db.doctors.find_one({"_id":_id}).get("name")
    
    @staticmethod
    def view_doctors():
        return list(db.doctors.find({}))

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
    


class Session:
    def __init__(self,subject:str,details:str,followup:str,prescription:list=[],report:list=[]):
        self.subject = subject
        self.details = details
        self.prescription = prescription
        self.followup = followup
        self.current = datetime.datetime.now()
        self.time = self.current.strftime("%X")
        self.date = self.current.strftime("%x")
        self.report = report

    def create_session(self,patient_id,doctor_id):
        self.doctor_id = doctor_id
        self.hospital_id = db.doctors.find_one({"_id": doctor_id}).get("hospital")
        session = {
            "doctor":self.doctor_id,
            "hospital":self.hospital_id,
            "subject":self.subject,
            "details":self.details,
            "prescription":self.prescription,
            "followup":self.followup,
            "time":self.time,
            "date":self.date,
            "prescription":self.prescription
            }
        db.patients.update_one({"_id": patient_id},{"$push": {"session": session}},)
        return jsonify({"des":"Session Created Successfully","type":"success"}),200


class Prescription:
    def __init__(self,medicine:str,morning:bool,evening:bool,night:bool,duration:str="Next Visit"):
        self.medicine = medicine
        self.morning = morning
        self.evening = evening
        self.night = night
        self.duration = duration

    def create_prescription(self):
        prescription = {
            "medicine":self.medicine,
            "morning":self.morning,
            "evening":self.evening,
            "night":self.night,
            "duration":self.duration
        }
        return prescription


class Specialization:
    def __init__(self,specialization:str):
        self.specialization = specialization
    
    def create_specialization(self):
        specialization = {
            "_id" : uuid.uuid4().hex,
            "specialization": self.specialization,
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