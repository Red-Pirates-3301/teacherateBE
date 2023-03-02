import re
import random
import string
from bson import json_util
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .validators import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from pymongo.errors import DuplicateKeyError
import pymongo


client = settings.CLIENT
teacher_db = settings.TEACHER_DB

# teacher_db.create_collection("teachers", validator=teacherValidator)

# Random functions

def generate_random_string(length=16):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def generate_unique_id(length=16):
    while True:
        id = generate_random_string(length)
        teacher = teacher_db.teachers.find_one({"id": id})
        if not teacher:
            return id

def validate_number(num):
    pattern = re.compile(r'^(0(\.\d+)?|[1-4](\.\d+)?|5(\.0+)?)$')
    return bool(pattern.match(str(num)))

# Create your views here.

@api_view(['POST'])
def addTeacher(request):
    id = generate_unique_id()
    teacher_name = request.data.get("teacher_name")
    place = request.data.get("place")
    total_rating = float(0)
    rating = float(0)
    number_of_ratings = 0
    subject = request.data.get("subject")
    
    try:
        # Validator code
        teacher_db.command({'collMod': 'teachers', 'validator': teacherValidator})
        # Create a unique index on teacher_name field
        teacher_db.teachers.create_index([('id', pymongo.ASCENDING)], unique=True)
        teacher_db.teachers.create_index([('teacher_name', pymongo.ASCENDING)], unique=True)
        
        # Insert teacher document
        teacher = {"id": id, "teacher_name": teacher_name, "place": place, "total_rating": total_rating, "rating": rating, "number_of_ratings": number_of_ratings, "subject": subject}
        teacher_db.teachers.insert_one(teacher)
        
        return HttpResponse("Teacher added!")
            
    except DuplicateKeyError:
        # Handle duplicate key error
        return HttpResponse("Teacher with that name already exists!")
        
    except Exception as e:
        # Handle other errors
        return HttpResponse(e)
    
    

@api_view(["GET"])
def getTeachers(request):
    
    documents = teacher_db.teachers.find({}, {'_id': 0, 'id': 1, 'teacher_name': 1, "place": 1, 'rating': 1, 'number_of_ratings': 1, 'subject': 1})
    json_document = json_util.dumps(documents)
    return JsonResponse(json_document, safe=False)



@api_view(["POST"])
def getTeacher(request):
    id = request.data.get("id")
    teacher = teacher_db.teachers.find_one({"id": id}, {'_id': 0, 'id': 1, 'teacher_name': 1, "place": 1, 'rating': 1, 'number_of_ratings': 1, 'subject': 1})
    print(teacher)
    json_document = json_util.dumps(teacher)
    return JsonResponse(json_document, safe=False)