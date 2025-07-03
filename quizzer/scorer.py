def calculate_score(quiz_data, user_answers):
    """Calculate quiz score"""
    questions = quiz_data["questions"]
    correct_count = 0
    total_questions = len(questions)
    
    for i, question_data in enumerate(questions):
        correct_answer = question_data["correct_answer"]
        user_answer = user_answers.get(i, "")
        
        if user_answer == correct_answer:
            correct_count += 1
    
    percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    
    return {
        "correct": correct_count,
        "total": total_questions,
        "percentage": percentage
    }

def get_performance_message(score):
    """Get performance message based on score"""
    percentage = score["percentage"]
    
    if percentage >= 90:
        return "🎉 Excellent! Outstanding performance!"
    elif percentage >= 80:
        return "👏 Great job! Very good understanding!"
    elif percentage >= 70:
        return "👍 Good work! Room for improvement."
    elif percentage >= 60:
        return "📚 Fair performance. Consider reviewing the material."
    else:
        return "📖 Keep studying! You'll do better next time."
