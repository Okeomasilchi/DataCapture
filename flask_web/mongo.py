from mongoengine import connect, Document, StringField, EmailField, DateTimeField
import datetime

# Establish a connection to the MongoDB database
connect("admin")

# Define the User document class
class User(Document):
    first_name = StringField(required=True, max_length=50, min_length=2)
    last_name = StringField(required=True, max_length=50, min_length=2)
    email = EmailField(required=True, max_length=100, min_length=13, unique=True)
    password = StringField(required=True, max_length=100, min_length=8)
    role = StringField(required=True, default="user", choices=["admin", "user", "guest"])
    created_at = DateTimeField(default=datetime.datetime.utcnow, required=True)
