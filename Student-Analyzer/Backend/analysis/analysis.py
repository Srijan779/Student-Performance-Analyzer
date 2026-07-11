def analyze_performance(cgpa, experience, level):
    score = 0
    recommendations = []

    # 1. CGPA Calculation (Max 50 points)
    cgpa_score = (cgpa / 10.0) * 50
    score += cgpa_score

    if cgpa < 7.0:
        recommendations.append("Focus on improving core academic subjects to boost your CGPA.")
    elif cgpa >= 8.5:
        recommendations.append("Excellent academic standing. Maintain this consistency.")

    # 2. Coding Level Calculation (Max 30 points)
    if level == 'Advanced':
        score += 30
        recommendations.append("Start participating in advanced hackathons and open-source projects.")
    elif level == 'Intermediate':
        score += 20
        recommendations.append("Focus heavily on Data Structures and Algorithms (DSA).")
    else:
        score += 10
        recommendations.append("Begin with fundamental programming concepts and build small projects.")

    # 3. Experience Calculation (Max 20 points)
    exp_score = min(experience * 5, 20)
    score += exp_score

    if experience == 0:
        recommendations.append("Start coding daily. Consistency is the key to building logic.")

    # Determine Final Category
    final_score = int(score)
    if final_score >= 80:
        category = "Excellent"
    elif final_score >= 60:
        category = "Good"
    elif final_score >= 40:
        category = "Average"
    else:
        category = "Needs Improvement"

    # Ensure there is always at least one recommendation
    if len(recommendations) == 0:
        recommendations.append("You are on a great track! Keep practicing and applying for internships.")

    return {
        "overall_score": final_score,
        "category": category,
        "recommendations": recommendations
    }