# Topic 2, Day 3 Homework
# Dicts, safe lookups with .get(), and set-style membership checking

student_grades = {
    "Praveen": 90,
    "Raj": 85,
    "Shreya": 92,
    "Bharat": 78
}

student_grades["Bharat"] += 10      # update an existing score
student_grades["Sanyam"] = 87        # add a 5th student

# Safe lookup with a fallback message instead of crashing
print(student_grades.get("Minal", "Not exist"))

# Membership check without a manual loop
print("Praveen" in set(student_grades.keys()))
# Note: "Praveen" in student_grades works identically and is more idiomatic --
# dict keys already support fast membership checks on their own.
