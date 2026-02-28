from flask import Flask, render_template, request

app = Flask(__name__)


def generate_study_plan(subjects, hours_per_day, exam_days):
    """
    Mock Study Plan Generator with Fair Hour Distribution
    """

    if isinstance(subjects, str):
        subjects = [s.strip() for s in subjects.split(",") if s.strip()]

    hours_per_day = int(hours_per_day)
    exam_days = int(exam_days)

    subject_count = len(subjects)
    plan_lines = []
    plan_lines.append("Day | Subject | Topics | Duration")

    difficulty_levels = ["Basic", "Intermediate", "Advanced"]

    for day in range(1, exam_days + 1):

        base_hours = hours_per_day // subject_count
        remainder = hours_per_day % subject_count
        start_index = (day - 1) % subject_count

        daily_distribution = {subject: base_hours for subject in subjects}

        for i in range(remainder):
            subject_index = (start_index + i) % subject_count
            daily_distribution[subjects[subject_index]] += 1

        # Last Day → Full Revision + Mock Test
        if day == exam_days:
            for subject in subjects:
                for _ in range(daily_distribution[subject]):
                    topic = "Full Revision + Mock Test"
                    plan_lines.append(f"Day {day} | {subject} | {topic} | 1 hr")
            continue

        # Every 3rd Day → Revision
        if day % 3 == 0:
            for subject in subjects:
                for _ in range(daily_distribution[subject]):
                    topic = "Revision + Practice Set"
                    plan_lines.append(f"Day {day} | {subject} | {topic} | 1 hr")
            continue

        # Gradual Difficulty
        if day <= exam_days // 3:
            difficulty = difficulty_levels[0]
        elif day <= (2 * exam_days) // 3:
            difficulty = difficulty_levels[1]
        else:
            difficulty = difficulty_levels[2]

        for subject in subjects:
            for _ in range(daily_distribution[subject]):
                topic = f"{difficulty} Concepts + Practice"
                plan_lines.append(f"Day {day} | {subject} | {topic} | 1 hr")

    return "\n".join(plan_lines)


@app.route("/", methods=["GET", "POST"])
def index():
    study_plan = None
    error = None

    if request.method == "POST":
        subjects = request.form.get("subjects", "").strip()
        hours = request.form.get("hours", "").strip()
        days = request.form.get("days", "").strip()

        # Basic validation
        if not subjects:
            error = "Please enter at least one subject."
        elif not hours.isdigit() or not days.isdigit():
            error = "Study hours and exam days must be positive whole numbers."
        else:
            hours = int(hours)
            days = int(days)

            if hours < 1 or hours > 24:
                error = "Study hours per day must be between 1 and 24."
            elif days < 1 or days > 365:
                error = "Exam days must be between 1 and 365."
            else:
                study_plan = generate_study_plan(subjects, hours, days)

    return render_template("index.html", study_plan=study_plan, error=error)


if __name__ == "__main__":
    app.run(debug=True)