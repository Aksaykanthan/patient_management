import uuid 
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
    def __init__(self,name:str,password:str,email:str,gender:str,phoneno:str,dob, bloodgroup:str):
        super().__init__(name,password,email,gender,phoneno)
        self.dob = dob
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
            }
        db.patient.insert_one(patient)
        
        return patient
    
    def add_report(self):
        ...



p: Patient = Patient(**{"name": "aksay","password":"123","email":"aksay@gmail.com","gender":"male","phoneno":"12345345","dob":"01-04-2033","bloodgroup":"B+"})

# print(p.create_patient())


class Doctor(User):
    def __init__(self,name:str,password:str,email:str,gender:str,phoneno:str,specialization:str,year_of_grad,hospital: Hospital):
        super().__init__(name,password,email,gender,phoneno)
        self.specialization = specialization
        self.year_of_grad = year_of_grad
        self.hospital = hospital
    
    def create_doctor(self):
        ...


class Session:
    def __init__(self,patient,doctor,prescription):
        self.patient = patient
        self.doctor = doctor
        self.prescription = prescription
        self.date = datetime.date.today()
        self.time = datetime.datetime.now().strftime('%H:%M:%S')

class Hospital:
    def __init__(self,name,address):
        self.name = name
        self.address = address

class Medicine:
    def __init__(self,name,description):
        self.name = name
        self.description = description


class TestReport:
    def __init__(self,patient:Patient,doctor:Doctor):
        self.patient = patient
        self.doctor = doctor
        self.date = datetime.date.today()
        self.time = datetime.datetime.now().strftime('%H:%M:%S')


class BloodTest(TestReport):
    def __init__(self, patient: Patient, doctor: Doctor,bgroup,rbc,wbc,hb):
        super().__init__(patient, doctor)
        self.bloodgroup = bgroup
        self.rbc = rbc
        self.wbc = wbc
        self.hb = hb

class SugarTest(TestReport):
    def __init__(self, patient: Patient, doctor: Doctor):
        super().__init__(patient, doctor)

class XRay(TestReport):
    ...

class Report:
    ...

class Prescription:
    ...



class Record:
    def __init__(self,patient:Patient,report:Report):
        ...
    # methods to implement 
        # add patient report to DB
        # view patient report from DB
        # update patient report in DB
        # delete patient report from DB
