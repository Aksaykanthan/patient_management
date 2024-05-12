from flask import Flask,jsonify,request,session
import uuid
from passlib.hash import pbkdf2_sha256
from app import db


class User:
    def __init__(self,name,email,password):
        self.name = name
        self.email = email
        self.password = password
    
    def start_session(self,user):
        del user['password']    
        
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user),200
    
    
    def signup(self):
        user = {
            '_id':uuid.uuid4().hex,
            'name':f"{self.name}",
            'email':f"{self.email}",
            "password":f"{self.password}"
        }
        user["password"] = pbkdf2_sha256.encrypt(user['password'])
        
        if db.doctors.find_one({'email': user['email']}):
            return jsonify({"des":"Email Address Already Registered","type":"danger"}),400
        
        if db.doctors.insert_one(user):
            return jsonify({"des": "User Has Been Registered Successfully","type":"success"}),200
        
        return jsonify({"des":"Registration failed","type":"danger"}),400
        
    
    def signin(self):
        user = {
            'email':f"{self.email}",
            "password":f"{self.password}"
        }
        
        user = db.doctors.find_one({'email':user['email']})
        
        if user:
            if pbkdf2_sha256.verify(self.password,user['password']):
                return self.start_session(user)
            else:
                return jsonify({"des":"Password is incorrect","type":"danger"}),400
        else:
            return jsonify({"des":"User not found","type":"danger"}),400
    
    @staticmethod
    def signout():
        session.clear()
