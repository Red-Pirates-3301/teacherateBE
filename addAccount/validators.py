accountValidator = {
  "$jsonSchema": {
    "bsonType": "object",
    "required": ["ip", "userID", "rated_teachers"],
    "properties": {
      "ip": {
        "bsonType": "string",
        "description": "must be a string and is required"
      },
      "userID": {
        "bsonType": "string",
        "minimum": 0,
        "maximum": 20,
        "description": "user id || length 20"
      },
      "rated_teachers": {
        "bsonType":"array",
        "items": {
          "bsonType": "string"
        },
        "maxItems": 9999,
        "description": "rated teacher list"
      }
    }
  }
}