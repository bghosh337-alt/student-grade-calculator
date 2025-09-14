import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="🎓 Student Grade Calculator", page_icon="🎓", layout="centered")

st.title("🎓 Student Grade Calculator")

# Initialize session state
if "students" not in st.session_state:
    st.session_state["students"] = []

# Sidebar input
st.sidebar.header("Add Student Marks")
with st.sidebar.form("student_form"):
    name = st.text_input("Student Name")
    math = st.number_input("Maths Marks", min_value=0, max_value=100, value=0)
    science = st.number_input("Science Marks", min_value=0, max_value=100, value=0)
    english = st.number_input("English Marks", min_value=0, max_value=100, value=0)
    history = st.number_input("History Marks", min_value=0, max_value=100, value=0)
    geography = st.number_input("Geography Marks", min_value=0, max_value=100, value=0)

    submitted = st.form_submit_button("Add Student")
    if submitted and name.strip() != "":
        total = math + science + english + history + geography
        avg = total / 5
        if avg >= 90:
            grade = "A"
        elif avg >= 75:
            grade = "B"
        elif avg >= 60:
            grade = "C"
        elif avg >= 40:
            grade = "D"
        else:
            grade = "F"

        st.session_state["students"].append({
            "Name": name.strip(),
            "Maths": math,
            "Science": science,
            "English": english,
            "History": history,
            "Geography": geography,
            "Total": total,
            "Average": avg,
            "Grade": grade
        })
        st.success(f"Student {name} added!")

# Display table and chart
df = pd.DataFrame(st.session_state["students"])

if df.empty:
    st.info("No student data yet. Add some from the sidebar!")
else:
    st.subheader("📋 Student Results")
    st.dataframe(df)

    # Chart for a selected student
    st.subheader("📊 Student Performance Chart")
    student_names = df["Name"].tolist()
    selected_student = st.selectbox("Select a student to view chart:", student_names)

    # SAFER: get the student row
    matched = df.loc[df["Name"] == selected_student]

    if matched.empty:
        st.warning("Selected student not found.")
    else:
        student_row = matched.iloc[0]  # one student's data as Series
        subjects = ["Maths", "Science", "English", "History", "Geography"]

        # Extract marks safely
        marks = []
        for sub in subjects:
            if sub in student_row.index:
                try:
                    marks.append(float(student_row[sub]))
                except Exception:
                    marks.append(0.0)
            else:
                marks.append(0.0)

        # Plot chart
        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.bar(subjects, marks, color="skyblue")
        ax.set_ylim(0, 100)
        ax.set_ylabel("Marks")
        ax.set_title(f"Marks of {selected_student}")

        # Add labels above bars
        for i, v in enumerate(marks):
            ax.text(i, v + 1, f"{v:.0f}", ha='center')

        st.pyplot(fig)

# Footer attribution
st.markdown("---")
st.markdown(f"Made   by 🎓 Bhaskar Ghosh")
