from flask import Flask, render_template, request

app = Flask(__name__)

def generate_study_plan(subjects, hours_per_day, exam_days):
    if not subjects or not hours_per_day or not exam_days:
        return "Please fill all fields properly."

    try:
        hours_per_day = int(hours_per_day)
        exam_days = int(exam_days)
    except ValueError:
        return "Hours and days must be valid numbers."

    if hours_per_day <= 0 or exam_days <= 0:
        return "Hours and days must be greater than 0."

    subjects = [s.strip() for s in subjects.split(",") if s.strip()]
    if not subjects:
        return "Please enter at least one subject."

    subject_count = len(subjects)

    plan_lines = []
    plan_lines.append("Day | Subject | Topics | Duration")

    difficulty_levels = ["Basic", "Intermediate", "Advanced"]

    for day in range(1, exam_days + 1):

        # ---- Equal Distribution Logic ----
        base_hours = hours_per_day // subject_count
        extra_hours = hours_per_day % subject_count

        # Rotate extra hour fairly across days
        start_index = (day - 1) % subject_count

        daily_allocation = [base_hours] * subject_count

        for i in range(extra_hours):
            daily_allocation[(start_index + i) % subject_count] += 1

        # ---- Last Day → Full Revision ----
        if day == exam_days:
            for idx, subject in enumerate(subjects):
                for _ in range(daily_allocation[idx]):
                    plan_lines.append(
                        f"Day {day} | {subject} | Full Revision + Mock Test | 1 hr"
                    )
            continue

        # ---- Every 3rd Day → Revision ----
        if day % 3 == 0:
            for idx, subject in enumerate(subjects):
                for _ in range(daily_allocation[idx]):
                    plan_lines.append(
                        f"Day {day} | {subject} | Revision + Practice Set | 1 hr"
                    )
            continue

        # ---- Normal Study Day ----
        if day <= exam_days // 3:
            difficulty = difficulty_levels[0]
        elif day <= (2 * exam_days) // 3:
            difficulty = difficulty_levels[1]
        else:
            difficulty = difficulty_levels[2]

        for idx, subject in enumerate(subjects):
            for _ in range(daily_allocation[idx]):
                topic = f"{difficulty} Concepts + Practice"
                plan_lines.append(
                    f"Day {day} | {subject} | {topic} | 1 hr"
                )

    return "\n".join(plan_lines)


@app.route("/", methods=["GET", "POST"])
def index():
    study_plan = None

    if request.method == "POST":
        subjects = request.form.get("subjects")
        hours = request.form.get("hours")
        days = request.form.get("days")

        study_plan = generate_study_plan(subjects, hours, days)

    return render_template("index.html", study_plan=study_plan)


if __name__ == "__main__":
    app.run(debug=True)