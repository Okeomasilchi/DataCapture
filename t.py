#!/usr/bin/python3
import jwt
import datetime
import os
from dotenv import load_dotenv
import time

load_dotenv("./.env")

sec = os.getenv("SECRET_KEY")

class Token:
    @staticmethod
    def get(id=None):
        current_time = datetime.datetime.now()
        target_time = current_time + datetime.timedelta(minutes=10)
        # Convert expiration time to Unix timestamp
        exp_time = int(target_time.timestamp())
        payload = {
            "id": id,
            "exp": exp_time
        }
        token = jwt.encode(payload, sec, algorithm='HS256')
        return token

    @staticmethod
    def validate(token):
        try:
            payload = jwt.decode(token, sec, algorithms=['HS256'])
            user_id = payload["id"]
            exp_time = payload["exp"]

            current_time = datetime.datetime.now()
            current_time_unix = int(current_time.timestamp())

            if current_time_unix > exp_time:
                # print(f"current_time_unix: {current_time_unix} > exp_time: {exp_time}")
                return None

            return user_id
        except jwt.ExpiredSignatureError as e:
            # print(e, "ExpiredSignatureError")
            return None
        except jwt.DecodeError as e:
            # print(e, "DecodeError")
            return None
        except jwt.InvalidTokenError as e:
            # print(e, "InvalidTokenError")
            return None
        except Exception as e:
            # print(e, "Exception")
            return None
