import streamlit as st
import pandas as pd

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="BMSCE SGPA & CGPA Analytics Portal",
    page_icon="🎓",
    layout="centered"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
    color: white;
}

h1, h2, h3, h4 {
    color: #FFFFFF;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOGO AND TITLE
# ---------------------------------------------------

st.image(
    "https://www.bmsce.ac.in/assets/img/bmsce-logo.png",
    width=140
)

st.title("🎓 BMSCE SGPA & CGPA Analytics Portal")

st.subheader(
    "Student Academic Performance Management System"
)

st.markdown("---")

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "sgpa_list" not in st.session_state:
    st.session_state.sgpa_list = []

# ---------------------------------------------------
# STUDENT DETAILS
# ---------------------------------------------------

st.header("👨‍🎓 Student Details")

name = st.text_input("Enter Student Name")

usn = st.text_input("Enter USN")

branch = st.selectbox(
    "Select Branch",
    [
        "Aerospace Engineering",
        "CSE",
        "ISE",
        "ECE",
        "EEE",
        "Mechanical",
        "Civil",
        "AIML"
    ]
)

section = st.selectbox(
    "Select Section",
    ["A", "B", "C"]
)

academic_year = st.selectbox(
    "Academic Year",
    ["2025-26", "2026-27"]
)

st.markdown("---")

# ---------------------------------------------------
# CLEAR BUTTON
# ---------------------------------------------------

if st.button("🗑 Clear All Records"):

    st.session_state.sgpa_list = []

    st.success("All records cleared successfully!")

# ---------------------------------------------------
# NUMBER OF SEMESTERS
# ---------------------------------------------------

num_semesters = st.number_input(
    "Enter Number of Semesters",
    min_value=1,
    step=1
)

# ---------------------------------------------------
# GRADE DICTIONARY
# ---------------------------------------------------

grade_dict = {
    "O": 10,
    "A+": 9,
    "A": 8,
    "B+": 7,
    "B": 6,
    "C": 5,
    "F": 0
}

# ---------------------------------------------------
# SGPA STORAGE
# ---------------------------------------------------

current_sgpas = []

# ---------------------------------------------------
# SEMESTER LOOP
# ---------------------------------------------------

for sem in range(int(num_semesters)):

    st.header(f"📘 Semester {sem + 1}")

    num_subjects = st.number_input(
        f"Enter Number of Subjects in Semester {sem + 1}",
        min_value=1,
        step=1,
        key=f"subjects{sem}"
    )

    total_credits = 0
    total_credit_points = 0

    # ---------------------------------------------------
    # SUBJECT LOOP
    # ---------------------------------------------------

    for i in range(int(num_subjects)):

        st.subheader(f"Subject {i + 1}")

        subject_name = st.text_input(
            f"Enter Subject Name",
            key=f"subject_name{sem}{i}"
        )

        credits = st.number_input(
            f"Credits for {subject_name if subject_name else 'Subject'}",
            min_value=0.0,
            step=0.5,
            key=f"credits{sem}{i}"
        )

        grade_letter = st.selectbox(
            f"Select Grade for {subject_name if subject_name else 'Subject'}",
            list(grade_dict.keys()),
            key=f"grade{sem}{i}"
        )

        grade_point = grade_dict[grade_letter]

        total_credits += credits

        total_credit_points += (
            credits * grade_point
        )

    # ---------------------------------------------------
    # SGPA CALCULATION
    # ---------------------------------------------------

    if total_credits > 0:

        sgpa = total_credit_points / total_credits

        current_sgpas.append(sgpa)

        st.success(
            f"✅ SGPA of Semester {sem + 1}: {round(sgpa, 2)}"
        )

# ---------------------------------------------------
# SAVE BUTTON
# ---------------------------------------------------

if st.button("💾 Save SGPA Records"):

    st.session_state.sgpa_list = current_sgpas.copy()

    st.success("SGPA records saved successfully!")

# ---------------------------------------------------
# CGPA SECTION
# ---------------------------------------------------

st.markdown("---")

st.header("📊 CGPA Analytics")

if st.button("🎯 Calculate CGPA"):

    if len(st.session_state.sgpa_list) > 0:

        cgpa = (
            sum(st.session_state.sgpa_list)
            / len(st.session_state.sgpa_list)
        )

        percentage = (
            (cgpa - 0.75) * 10
        )

        # ---------------------------------------------------
        # RESULT METRICS
        # ---------------------------------------------------

        col1, col2 = st.columns(2)

        col1.metric(
            "CGPA",
            round(cgpa, 2)
        )

        col2.metric(
            "Percentage",
            f"{round(percentage, 2)}%"
        )

        st.markdown("---")

        # ---------------------------------------------------
        # PERFORMANCE ANALYSIS
        # ---------------------------------------------------

        st.subheader("📈 Performance Analysis")

        if cgpa >= 9:

            st.success(
                "🌟 Outstanding Performance"
            )

        elif cgpa >= 8:

            st.success(
                "🎯 Excellent Performance"
            )

        elif cgpa >= 7:

            st.info(
                "👍 Good Performance"
            )

        else:

            st.warning(
                "📚 Needs Improvement"
            )

        # ---------------------------------------------------
        # SGPA GRAPH
        # ---------------------------------------------------

        st.subheader(
            "📉 Semester-wise SGPA Trend"
        )

        chart_data = pd.DataFrame({

            "Semester": range(
                1,
                len(st.session_state.sgpa_list) + 1
            ),

            "SGPA": st.session_state.sgpa_list

        })

        st.line_chart(
            chart_data.set_index("Semester")
        )

        # ---------------------------------------------------
        # STUDENT SUMMARY
        # ---------------------------------------------------

        st.markdown("---")

        st.subheader("📄 Student Summary")

        st.write(f"👤 Name: {name}")

        st.write(f"🆔 USN: {usn}")

        st.write(f"🏫 Branch: {branch}")

        st.write(f"📚 Section: {section}")

        st.write(f"📅 Academic Year: {academic_year}")

    else:

        st.warning(
            "Please save SGPA records first!"
        )

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

if st.session_state.sgpa_list:

    st.sidebar.header("📚 Saved SGPA Records")

    for idx, value in enumerate(
        st.session_state.sgpa_list,
        start=1
    ):

        st.sidebar.write(
            f"Semester {idx}: {round(value, 2)}"
        )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "Developed by Jahnavi R | Department of Aerospace Engineering"
)
