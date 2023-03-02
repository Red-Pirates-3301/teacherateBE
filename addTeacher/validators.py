teacherValidator = {
  "$jsonSchema": {
    "bsonType": "object",
    "required": ["id", "teacher_name", "total_rating", "rating", "number_of_ratings", "subject"],
    "properties": {
      "id": {
        "bsonType": "string",
        "description": "must be a string and is required"
      },
      "teacher_name": {
        "bsonType": "string",
        "description": "must be a string and is required"
      },
      "place": {
        "bsonType": "string",
        "description": "must be a string and is required"
      },
      "rating": {
        "bsonType": "double",
        "minimum": 0,
        "maximum": 5,
        "description": "must be a number between 0 and 5 and is required" 
      },
      "total_rating": {
        "bsonType": "double",
        "minimum": 0,
        "maximum": 9999,
        "description": "must be a number between 0 and 9999 and is required"
      },
      "number_of_ratings": {
        "bsonType": "int",
        "minimum": 0,
        "maximum": 9999,
        "description": "must be an integer between 0 and 9999 and is required"
      },
      "subject": {
        "bsonType": "string",
        "description": "must be a string and is required"
      }
    }
  }
}