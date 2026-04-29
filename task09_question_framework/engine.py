import json
import random


def load_questions():
    with open("questions.json", "r", encoding="utf-8") as file:
        return json.load(file)


def validate_question(question):
    required_fields = [
        "question_id",
        "domain",
        "difficulty",
        "topic",
        "type",
        "question_text"
    ]

    for field in required_fields:
        if field not in question:
            return False

    if len(question["question_text"].strip()) < 10:
        return False

    return True


def filter_by_domain(questions, domain):
    return [
        q for q in questions
        if q["domain"].lower() == domain.lower()
    ]


def filter_by_difficulty(questions, difficulty):
    return [
        q for q in questions
        if q["difficulty"].lower() == difficulty.lower()
    ]


def remove_previous_questions(questions, previous_context):
    return [
        q for q in questions
        if q["question_text"] not in previous_context
    ]


def smart_fallback_order(difficulty):
    difficulty = difficulty.lower()

    if difficulty == "easy":
        return ["easy", "medium", "hard"]

    elif difficulty == "medium":
        return ["medium", "easy", "hard"]

    elif difficulty == "hard":
        return ["hard", "medium", "easy"]

    return ["medium", "easy", "hard"]


def generate_question(domain, difficulty, previous_context):
    questions = load_questions()

    # Step 1: Validate dataset
    valid_questions = [
        q for q in questions
        if validate_question(q)
    ]

    # Step 2: Filter domain
    domain_questions = filter_by_domain(
        valid_questions,
        domain
    )

    if not domain_questions:
        return {
            "error": "Invalid domain selected."
        }

    # Step 3: Remove previous asked questions
    domain_questions = remove_previous_questions(
        domain_questions,
        previous_context
    )

    if not domain_questions:
        return {
            "error": "No more questions available in this domain."
        }

    # Step 4: Smart difficulty fallback
    fallback_levels = smart_fallback_order(
        difficulty
    )

    final_pool = []

    for level in fallback_levels:
        temp = filter_by_difficulty(
            domain_questions,
            level
        )

        if temp:
            final_pool = temp
            break

    if not final_pool:
        return {
            "error": "No matching question found."
        }

    # Step 5: Random question
    selected = random.choice(final_pool)

    # Step 6: Clean response
    return {
        "question_id": selected["question_id"],
        "domain": selected["domain"],
        "difficulty": selected["difficulty"],
        "topic": selected["topic"],
        "type": selected["type"],
        "question_text": selected["question_text"],
        "status": "success"
    }


# Test Run
if __name__ == "__main__":
    print(
        generate_question(
            "AI/ML",
            "medium",
            []
        )
    )