
def score_quiz(user_answers, quiz_data):
    """
    Compare user answers with correct answers and return score and result list.
    """
    score = 0
    result = []
    for i, q in enumerate(quiz_data):
        correct = q['answer'].strip().lower()
        user = user_answers[i].strip().lower()
        is_correct = correct == user or user in correct
        result.append(is_correct)
        if is_correct:
            score += 1
    return score, result
