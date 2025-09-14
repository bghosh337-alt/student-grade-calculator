import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config and custom CSS for styling
st.set_page_config(
    page_title="🎓 Student Grade Calculator",
    page_icon="🎓",
    layout="centered",
)

# Inject custom CSS for stylish cards, colored grades, sidebar
st.markdown("""
    <style>
        .main {background-color: #f0f4fa;}
        .stApp {background: #f0f4fa;}
        .grade-A {color: #008000; font-weight: bold;}
        .grade-B {color: #0055aa; font-weight: bold;}
        .grade-C {color: #ffb300; font-weight: bold;}
        .grade-D {color: #ff7c06; font-weight: bold;}
        .grade-F {color: #c20000; font-weight: bold;}
        .stTable {background: #ffffff;}
        .student-card {
            background: #e8eff8;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 2px 12px #cdddeb;
            margin-bottom: 10px;
        }
        .sidebar .stForm {background: #e4edfc; padding:1rem;border-radius:10px;}
    </style>
""", unsafe_allow_html=True)

st.title("🎓 Student Grade Calculator")
st.write("Effortlessly calculate grades and visualize performance with a sleek, modern dashboard!")

# Initialize session state for students
if "students" not in st.session_state:
    st.session_state["students"] = []

# Sidebar input - clearer design, emojis for subjects
st.sidebar.header("➕ Add Student Marks")
with st.sidebar.form("student_form"):
    name = st.text_input("👩‍🎓 Student Name")
    math = st.number_input("📐 Maths Marks", min_value=0, max_value=100, value=0)
    science = st.number_input("🧪 Science Marks", min_value=0, max_value=100, value=0)
    english = st.number_input("📚 English Marks", min_value=0, max_value=100, value=0)
    history = st.number_input("🏛️ History Marks", min_value=0, max_value=100, value=0)
    geography = st.number_input("🌍 Geography Marks", min_value=0, max_value=100, value=0)
    submitted = st.form_submit_button("Add Student")
    if submitted and name.strip() != "":
        total = math + science + english + history + geography
        avg = total / 5
        if avg >= 90:
            grade = "A"
            grade_class = "grade-A"
        elif avg >= 75:
            grade = "B"
            grade_class = "grade-B"
        elif avg >= 60:
            grade = "C"
            grade_class = "grade-C"
        elif avg >= 40:
            grade = "D"
            grade_class = "grade-D"
        else:
            grade = "F"
            grade_class = "grade-F"
        st.session_state["students"].append({
            "Name": name,
            "Maths": math,
            "Science": science,
            "English": english,
            "History": history,
            "Geography": geography,
            "Total": total,
            "Average": avg,
            "Grade": f'<span class="{grade_class}">{grade}</span>'
        })
        st.success(f"🎉 Student {name} added!")

df = pd.DataFrame(st.session_state["students"])

if not df.empty:
    st.subheader("📋 Student Results")

    # Show stylish student cards with grade coloring
    for i, row in df.iterrows():
        st.markdown(f"""
        <div class="student-card">
            <h4>{row['Name']}</h4>
            <b>Total Marks:</b> {row['Total']}<br>
            <b>Average:</b> {row['Average']:.2f}<br>
            <b>Grade:</b> {row['Grade']}
        </div>
        """, unsafe_allow_html=True)

    # Display dataframe with clickable sorting and colored grades
    styled_df = df.copy()
    styled_df["Grade"] = styled_df["Grade"].apply(lambda x:
        x if x.startswith('<span') else f'<span class="grade-F">{x}</span>')
    st.write(
        styled_df.to_html(escape=False, index=False), unsafe_allow_html=True
    )

    # Chart for a selected student - animated effect
    st.subheader("📊 Student Performance Chart")
    student_names = df["Name"].tolist()
    selected_student = st.selectbox("Select a student to view chart:", student_names)
    student_data = df[df["Name"] == selected_student].iloc
    subjects = ["Maths", "Science", "English", "History", "Geography"]
    marks = [student_data[sub] for sub in subjects]
    fig, ax = plt.subplots()
    bars = ax.bar(subjects, marks, color=["#6ca0dc", "#ffce78", "#58c7b8", "#fa7251", "#b998f8"])
    ax.set_ylim(0, 100)
    ax.set_ylabel("Marks")
    ax.set_title(f"Marks of {selected_student}")
    for bar, mark in zip(bars, marks):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()-7, str(int(mark)), 
                ha='center', color='white', fontweight='bold')
    st.pyplot(fig)
else:
    st.info("No student data yet. Add some from the sidebar! 🎈")
# Footer attribution
st.markdown("""
    <hr style="border-top: 1px solid #bbb;">
    <div style="text-align: center; font-size: 18px; color: #555;">
        <b>Made by Bhaskar Ghosh</b> 🎓
    </div>
""", unsafe_allow_html=True)
