import collections


def calculate_option_percentages(question_responses, all_options, question_id):
    """Calculates the percentage of responses for each option in a question"""

    option_counts = collections.Counter()
    for response in question_responses:
        for answer in response["answers"]:
            if answer["question_id"] == question_id:
                option_counts.update(answer["response"])

    total_responses = sum(option_counts.values())

    # Create results with all options included
    options = []
    for option in all_options:
        count = option_counts[option]
        options.append(
            {
                "option": option,
                "%": (
                    round((count / total_responses) * 100) if total_responses > 0 else 0
                ),  # Round up
            }
        )

    return options, total_responses  # Return total_responses as well


def parse_survey_data(data):
    results = []
    for question in data["questions"]:
        question_id = question["id"]
        all_options = question["options"]
        question_responses = [response for response in data["responses"]]

        options, total_responses = calculate_option_percentages(
            question_responses, all_options, question_id
        )

        results.append(
            {
                "question": question["question"],
                "options": options,
                "total_responses": total_responses,  # Add total responses
            }
        )

    return results
