from django.shortcuts import render
import json
import time
from django.middleware.csrf import get_token
from bson import json_util
from django.http import JsonResponse
import string
import hashlib
import re
import random
from django.conf import settings
from .validators import *
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import pymongo
from django.http import HttpResponse, HttpRequest
from rest_framework.decorators import api_view

client = settings.CLIENT
account_db = settings.ACCOUNT_DB
teacher_db = settings.TEACHER_DB

# account_db.create_collection("accounts", validator=accountValidator)

# Random functions

def generate_random_string(length=16):
    characters = string.ascii_letters + string.digits + '!@#$%^&*()_+-='
    characters = ''.join(random.choice(characters) for i in range(length))
    return f"anonymous{characters}"

def generate_unique_user_id(length=16):
    while True:
        userID = generate_random_string(length)
        account = account_db.accounts.find_one({"userID": userID})
        if not account:
            return userID

def validate_ipv4_address(ip):
    pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return bool(re.match(pattern, ip))

def hash_ip(ip_address):
    hashed_ip = hashlib.sha256(ip_address.encode()).hexdigest()
    return hashed_ip

def validate_number(num):
    pattern = re.compile(r'^(0(\.\d+)?|[1-4](\.\d+)?|5(\.0+)?)$')
    return bool(pattern.match(str(num)))

# Create your views here.
@csrf_protect
@api_view(["POST"])
def addAccount(request):
    ip = request.data.get("ip")
    hashed_ip = hash_ip(ip)
    userID = generate_unique_user_id()
    rated_teachers = []
    
    try:
        # Validator code
        account_db.command({'collMod': 'accounts', 'validator': accountValidator})
        # Create a unique index on userID field
        account_db.accounts.create_index([('ip', pymongo.ASCENDING)], unique=True)
        account_db.accounts.create_index([('userID', pymongo.ASCENDING)], unique=True)
        
        # Insert account document
        account = {"ip": hashed_ip, "userID": userID, "rated_teachers": rated_teachers}
        account_db.accounts.insert_one(account)
        
        return JsonResponse({"userID": userID})
            
    except Exception as e:
        # Handle other errors
        return HttpResponse(e)



    
    
@csrf_protect
@api_view(["POST"])
def retrieve(request):
    ip = request.data.get("ip")
    hashed_ip = hash_ip(ip)
    # userID = request.data.get("userID")
    
    if validate_ipv4_address(ip):
            account_by_ip = account_db.accounts.find_one({"ip": hashed_ip}, {'_id': 0, 'userID': 1, 'rated_teachers': 1})
            
            if not account_by_ip:    
                return JsonResponse({"status":404})
            
            else:
                json_document_ip = json_util.dumps(account_by_ip)
                return JsonResponse(json_document_ip, safe=False)
            
    else:
        return HttpResponse("Invalid IP")
    
    
    

@csrf_protect
@api_view(["POST"])
def addRating(request):
    userID = request.data.get("userID")
    teacher_id = request.data.get("teacher_id")
    rating = request.data.get("rating")
    
    account = account_db.accounts.find_one({"userID": userID})
    
    json_document = json_util.dumps(account["rated_teachers"])
    array = json.loads(json_document)
    
#     if teacher_id in array:
#         return HttpResponse("Teacher already rated.")
    
    if(validate_number(rating) != True):
        return HttpResponse("Rating is invalid")
    
#     print("ACCOUNT", account["rated_teachers"])
    
    try:
        teacher = teacher_db.teachers.find_one({"id": teacher_id})
        
        # If no teacher was found with the given ID, return an error message
        if not teacher:
            return HttpResponse(f"Teacher not found")
        
        # Increment the teacher's rating and number of ratings
        teacher['total_rating'] +=  int(round(float(rating)))
        teacher['number_of_ratings'] += 1
        teacher['rating'] = teacher['total_rating'] / teacher['number_of_ratings']
        
        # Save the updated teacher document back to the database
        teacher_db.teachers.update_one({"id": teacher_id}, {"$set": teacher})
    
        # Edit the user's data
        
        if not account:
            return HttpResponse(f"Account not found")
        
        account_db.accounts.update_one({"userID": userID}, {"$push": {"rated_teachers": teacher["id"]}})
        return HttpResponse("Rating added!")
        
    except Exception as e:
        # Handle other errors
        print(e)
        return HttpResponse(e)



@api_view(["GET"])
def generate_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrf_token': token})
