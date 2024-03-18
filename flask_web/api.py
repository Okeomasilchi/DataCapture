#!/usr/bin/env python3
import requests


class APIClient:
    def __init__(self, base_url=None):
      if not base_url:
        raise ValueError("base_url Must be provided to initialize the API Client.")
      else:
        self.base_url = base_url

    def status(self):
        url = f"{self.base_url}/status"
        response = requests.get(url)
        return response.json()[0]

    def stats(self):
        url = f"{self.base_url}/stats"
        response = requests.get(url)
        return response.json()

    def get_users(self):
        url = f"{self.base_url}/users"
        response = requests.get(url)
        return response.json()

    def get_user_by_id(self, user_id):
        url = f"{self.base_url}/users/{user_id}"
        response = requests.get(url)
        return response.json()

    def delete_user(self, user_id):
        url = f"{self.base_url}/users/{user_id}"
        response = requests.delete(url)
        return response.status_code

    def create_user(self, user_data):
        url = f"{self.base_url}/users"
        response = requests.post(url, json=user_data)
        return response.json(), response.status_code

    def update_user(self, user_id, user_data):
        url = f"{self.base_url}/users/{user_id}"
        response = requests.put(url, json=user_data)
        return response.json(), response.status_code

    def login_user(self, login_data):
        url = f"{self.base_url}/users/login"
        response = requests.post(url, json=login_data)
        return response.json(), response.status_code

    def validate_user_email(self, email_data):
        url = f"{self.base_url}/users/validate"
        response = requests.get(url, json=email_data)
        return response.json(), response.status_code

    def get_survey_by_id(self, survey_id):
        url = f"{self.base_url}/survey/{survey_id}"
        response = requests.get(url)
        return response.json()

    def get_surveys_by_user_id(self, user_id):
        url = f"{self.base_url}/users/survey/{user_id}"
        response = requests.get(url)
        return response.json()

    def delete_survey_by_id(self, survey_id):
        url = f"{self.base_url}/survey/{survey_id}"
        response = requests.delete(url)
        return response.status_code

    def create_survey(self, survey_data):
        url = f"{self.base_url}/survey"
        response = requests.post(url, json=survey_data)
        return response.json(), response.status_code

    def update_survey_by_id(self, survey_id, survey_data):
        url = f"{self.base_url}/survey/{survey_id}"
        response = requests.put(url, json=survey_data)
        return response.json(), response.status_code

    def get_survey_dashboard(self, survey_id):
        url = f"{self.base_url}/dashboard/{survey_id}"
        response = requests.get(url)
        return response.json()

    def log_response(self, survey_id, response_data):
        url = f"{self.base_url}/response/{survey_id}"
        response = requests.post(url, json=response_data)
        return response.json(), response.status_code

    def get_responses_by_survey_id(self, survey_id):
        url = f"{self.base_url}/response/{survey_id}"
        response = requests.get(url)
        return response.json(), response.status_code

    def update_questions(self, survey_id, questions_data):
        url = f"{self.base_url}/question/{survey_id}"
        response = requests.put(url, json=questions_data)
        return response.json(), response.status_code

    def delete_questions(self, survey_id, questions_ids):
        url = f"{self.base_url}/question/{survey_id}"
        response = requests.delete(url, json={"questions": questions_ids})
        return response.json(), response.status_code
