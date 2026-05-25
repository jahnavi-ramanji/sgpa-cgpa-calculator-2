import streamlit as st
import pandas as pd
import numpy as np

# --- PAGE SETUP ---
st.set_page_config(page_title="BMSCE Result Portal", page_icon="🎓", layout="wide")

# --- GRADE TO POINT DICTIONARY (Standard 10-Point Scale) ---
grade_points = {
    "O (Outstanding)": 10,
    "A+ (Excellent)": 9,
    "A (Very Good)": 8,
    "B+ (Good)": 7,
    "B (Above Average)": 6,
    "C (Average)": 5,
    "P (Pass)": 4,
    "F (Fail)": 0
}

# --- SIDEBAR NAVIGATION ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/f/f8/BMS_College_of_Engineering_logo.svg/1200px-BMS_College_of_Engineering_logo.svg.png", width=150)
st.sidebar.title("Student Portal")
page = st.sidebar.radio("Navigate to:", ["SGPA & Analytics", "Target CGPA Analyzer (What-If)"])

st.sidebar.markdown("---")
st.sidebar.info("Developed by AI/ML Dept")

# --- PAGE 1: SGPA & ANALYTICS ---
if page == "SGPA & Analytics":
    st.title("🎓 Semester Result & Analytics")
    st.write("Enter your marks to generate your SGPA and visualize your performance.")

    # Student Info
    col1, col2 = st.columns(2)
    with col1:
        student_name = st.text_input("Student Name")
    with col2:
        usn = st.text_input("USN (e.g., 1BM22AI001)")

    st.markdown("### Subject Details")
    num_subjects = st.number_input("Number of Subjects", min_value=1, max_value=10, value=5, step=1)

    # Create dynamic inputs for subjects
    subjects = []
    credits = []
    grades = []

    # UI for entering subject data
    for i in range(int(num_subjects)):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            subj = st.text_input(f"Subject {i+1} Name", key=f"sub_{i}")
        with c2:
            cred = st.number_input(f"Credits", min_value=1, max_value=5, value=3, key=f"cred_{i}")
        with c3:
            grade = st.selectbox(f"Grade", options=list(grade_points.keys()), key=f"grade_{i}")
        
        subjects.append(subj if subj else f"Subject {i+1}")
        credits.append(cred)
        grades.append(grade)

    if st.button("Generate Result & Analytics", type="primary"):
        # Calculations
        total_credits = sum(credits)
        earned_points = sum([credits[i] * grade_points[grades[i]] for i in range(len(credits))])
        
        sgpa = earned_points / total_credits if total_credits > 0 else 0

        st.markdown("---")
        st.header(f"Result for {student_name} ({usn})")
        
        # Display SGPA in a prominent metric box
        st.metric(label="Calculated SGPA", value=f"{sgpa:.2f}")

        # Visual Analytics
        st.subheader("Performance Analytics")
        
        # Create a dataframe for the charts
        df = pd.DataFrame({
            "Subject": subjects,
            "Credits": credits,
            "Grade Points": [grade_points[g] for g in grades]
        })

        # Display Bar Chart
        st.bar_chart(data=df, x="Subject", y="Grade Points", use_container_width=True)

        # Downloadable "Invoice" (CSV format for Streamlit simplicity)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Result Report (CSV)",
            data=csv,
            file_name=f"{usn}_result.csv",
            mime="text/csv",
        )

# --- PAGE 2: TARGET CGPA ANALYZER ---
elif page == "Target CGPA Analyzer (What-If)":
    st.title("🎯 The 'What-If' Target Analyzer")
    st.write("Plan your future semesters to hit your graduation goals.")

    col1, col2 = st.columns(2)
    with col1:
        current_cgpa = st.number_input("Current CGPA", min_value=0.0, max_value=10.0, value=7.5, step=0.01)
        credits_completed = st.number_input("Total Credits Completed So Far", min_value=1, max_value=200, value=40)
    
    with col2:
        target_cgpa = st.number_input("Target CGPA for Graduation", min_value=0.0, max_value=10.0, value=8.5, step=0.01)
        credits_remaining = st.number_input("Total Credits Remaining in Degree", min_value=1, max_value=160, value=120)

    if st.button("Analyze Target", type="primary"):
        # Math for What-If
        current_total_points = current_cgpa * credits_completed
        required_total_points = target_cgpa * (credits_completed + credits_remaining)
        points_needed = required_total_points - current_total_points
        
        required_sgpa_average = points_needed / credits_remaining

        st.markdown("---")
        if required_sgpa_average > 10:
            st.error(f"**Target Impossible:** You would need an average SGPA of {required_sgpa_average:.2f} in your remaining semesters, which is above 10.0. Consider revising your target.")
        elif required_sgpa_average < 0:
            st.success(f"**Target Secured:** You have already secured enough points to maintain this target even if you fail everything (though we don't recommend that!).")
        else:
            st.success(f"**Target Achievable:** You need to maintain an average SGPA of **{required_sgpa_average:.2f}** over your remaining {credits_remaining} credits to graduate with a {target_cgpa} CGPA.")
            
            # Progress bar visualization
            st.progress(required_sgpa_average / 10.0)
