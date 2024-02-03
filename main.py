# Assuming you have a list of questions, options, and survey IDs
questions = ["What is your favorite color?", "How often do you exercise?", "Do you prefer cats or dogs?"]
options = [["Red", "Blue", "Green"], ["Every day", "Once a week", "Rarely"], ["Cats", "Dogs"]]
survey_ids = [1, 1, 2]
rand = [True, False, True]

# Generate a list of dictionaries
survey_data = [
    {"question": question, "options": options, "survey_id": survey_id, "random": rand}
    for question, options, survey_id, rand in zip(questions, options, survey_ids, rand)
]

# Print the generated list
print(survey_data)
