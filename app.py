import streamlit as st
from pathlib import Path
from datetime import date
import json
import random
import string

# -------------------- DATA HANDLING --------------------
DATABASE = "database.json"

def load_data():
    if Path(DATABASE).exists():
        with open(DATABASE) as f:
            return json.loads(f.read())
    return []

def save_data(data):
    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

def generate_scholarno():
    digits = random.choices(string.digits, k=5)
    random.shuffle(digits)
    return "".join(digits)

# -------------------- UI --------------------
st.set_page_config(page_title="Student Management System", layout="centered")
st.title("🎓 Student Management System")

menu = st.sidebar.selectbox(
    "Select an option",
    [
        "Create Profile",
        "Update Profile",
        "Report Card",
        "Delete Profile",
        "Mark Attendance",
    ]
)

# -------------------- CREATE PROFILE --------------------
if menu == "Create Profile":
    st.header("Create Student Profile")

    with st.form("create_form"):
        name = st.text_input("Name")
        grade = st.text_input("Grade")
        email = st.text_input("Email")
        password = st.text_input("Password (6 digits)", type="password")
        phoneno = st.text_input("Phone Number (10 digits)")
        submit = st.form_submit_button("Create Profile")

        if submit:
            if len(password) != 6 or not password.isdigit():
                st.error("Password must be exactly 6 digits")
            elif len(phoneno) != 10 or not phoneno.isdigit():
                st.error("Phone number must be 10 digits")
            else:
                scholarno = generate_scholarno()
                student = {
                    "name": name,
                    "grade": grade,
                    "email": email,
                    "scholarno": scholarno,
                    "password": password,
                    "phoneno": phoneno
                }
                data.append(student)
                save_data(data)
                st.success("Profile created successfully!")
                st.info(f"Your Scholar Number: {scholarno}")

# -------------------- UPDATE PROFILE --------------------
elif menu == "Update Profile":
    st.header("Update Profile")

    name = st.text_input("Name")
    scholarno = st.text_input("Scholar Number")
    grade = st.text_input("Grade")

    if st.button("Find Profile"):
        user = next(
            (i for i in data if i["name"] == name and i["scholarno"] == scholarno and i["grade"] == grade),
            None
        )

        if not user:
            st.error("User not found")
        else:
            st.success("Profile found")
            email = st.text_input("New Email", user["email"])
            password = st.text_input("New Password", user["password"])
            phoneno = st.text_input("New Phone Number", user["phoneno"])

            if st.button("Update"):
                user["email"] = email
                user["password"] = password
                user["phoneno"] = phoneno
                save_data(data)
                st.success("Profile updated successfully")

# -------------------- REPORT CARD --------------------
elif menu == "Report Card":
    st.header("Generate Report Card")

    name = st.text_input("Name")
    scholarno = st.text_input("Scholar Number")
    grade = st.text_input("Grade")

    if st.button("Generate"):
        user = next(
            (i for i in data if i["name"] == name and i["scholarno"] == scholarno and i["grade"] == grade),
            None
        )

        if not user:
            st.error("Student not found")
        else:
            maths = st.number_input("Maths", 0, 100)
            science = st.number_input("Science", 0, 100)
            english = st.number_input("English", 0, 100)
            hindi = st.number_input("Hindi", 0, 100)
            computer = st.number_input("Computer", 0, 100)

            if st.button("Submit Marks"):
                total = maths + science + english + hindi + computer
                percentage = total / 5

                grade_label = (
                    "A+" if percentage >= 90 else
                    "B+" if percentage >= 80 else
                    "C+" if percentage >= 70 else
                    "D+" if percentage >= 60 else
                    "Fail"
                )

                user["report_card"] = {
                    "maths": maths,
                    "science": science,
                    "english": english,
                    "hindi": hindi,
                    "computer": computer,
                    "total": total,
                    "percentage": percentage
                }

                save_data(data)

                st.success("Report Card Generated")
                st.write("### 📄 Report Card")
                st.write("Name:", user["name"])
                st.write("Scholar No:", user["scholarno"])
                st.write("Total:", total)
                st.write("Percentage:", percentage)
                st.write("Grade:", grade_label)

# -------------------- DELETE PROFILE --------------------
elif menu == "Delete Profile":
    st.header("Delete Student Profile")

    name = st.text_input("Name")
    scholarno = st.text_input("Scholar Number")
    grade = st.text_input("Grade")

    if st.button("Delete"):
        for i in data:
            if i["name"] == name and i["scholarno"] == scholarno and i["grade"] == grade:
                data.remove(i)
                save_data(data)
                st.success("Profile deleted successfully")
                break
        else:
            st.error("Student not found")

# -------------------- ATTENDANCE --------------------
elif menu == "Mark Attendance":
    st.header("Mark Attendance")

    name = st.text_input("Name")
    scholarno = st.text_input("Scholar Number")

    if st.button("Mark Attendance"):
        user = next(
            (i for i in data if i["name"] == name and i["scholarno"] == scholarno),
            None
        )

        if not user:
            st.error("Student not found")
        else:
            today = str(date.today())
            user.setdefault("attendance", [])

            if today in user["attendance"]:
                st.warning("Attendance already marked for today")
            else:
                user["attendance"].append(today)
                save_data(data)
                st.success(f"Attendance marked for {today}")
