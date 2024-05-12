from flask import jsonify
import uuid
from app import db

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
        return db.patients.find()

    @staticmethod
    def get_patient(id):
        return db.patients.find_one({"_id":id})
