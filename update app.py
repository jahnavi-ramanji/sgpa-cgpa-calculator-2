
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from PIL import Image
import os

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
# ---------------------------------------------------
# BMSCE CONTINEO STYLE UI
# ---------------------------------------------------

st.set_page_config(
    page_title="BMSCE Academic Portal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>

/* Main App */
.stApp {
    background-color: #f1f5f9;
    color: #111827;
    font-family: 'Segoe UI', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
    border-right: 2px solid #1e293b;
}

/* Sidebar Text */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Titles */
h1, h2, h3 {
    color: #0f172a;
    font-weight: 700;
}

/* Labels */
label {
    color: #1e293b !important;
    font-weight: 600;
}

/* Inputs */
.stTextInput input,
.stNumberInput input {
    background-color: white;
    color: black;
    border-radius: 10px;
    border: 1px solid #cbd5e1;
}

/* Selectbox */
.stSelectbox div[data-baseweb=\"select\"] {
    background-color: white;
    border-radius: 10px;
    color: black;
}

/* Buttons */
.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    border: none;
    height: 45px;
    font-size: 16px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #1d4ed8;
}

/* Metric Cards */
[data-testid=\"metric-container\"] {
    background: white;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #e2e8f0;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
}

/* Metric Text */
[data-testid=\"metric-container\"] * {
    color: #111827 !important;
}

/* Info Box */
.stAlert {
    border-radius: 12px;
}

/* Remove Streamlit Header/Footer */
header, footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)
# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

col1, col2 = st.columns([1,5])

with col1:
    st.image("logo.png", width=100)

with col2:
    st.markdown(
        "<h1 style='margin-top:20px;'>BMSCE Academic Analytics Portal</h1>",
        unsafe_allow_html=True
    )

st.markdown("---")

st.sidebar.image("logo.png", width=120)

st.sidebar.title("BMSCE Portal")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Student Details",
        "SGPA Calculator",
        "CGPA Calculator",
        "Target Analyzer",
        "AI Grade Predictor",
        "Analytics Dashboard",
        "Download Transcript"
    ]
)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if 'sgpa_list' not in st.session_state:
    st.session_state.sgpa_list = []

if 'student_data' not in st.session_state:
    st.session_state.student_data = {}

# ---------------------------------------------------
# GRADE MAP
# ---------------------------------------------------

grade_map = {
    "O": 10,
    "A+": 9,
    "A": 8,
    "B+": 7,
    "B": 6,
    "C": 5,
    "F": 0
}
# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------

if page == "Dashboard":

    st.header("🎓 Student Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Current CGPA", "8.74")

    with col2:
        st.metric("Credits Earned", "126")

    with col3:
        st.metric("Predicted SGPA", "9.02")

    st.markdown("---")

    st.subheader("Welcome to BMSCE Academic Portal")

    st.success("Welcome back to the BMSCE Academic Management System")

    
    )
# ---------------------------------------------------
# STUDENT DETAILS PAGE
# ---------------------------------------------------

if page == "Student Details":

    st.header("👨‍🎓 Student Details")

    name = st.text_input("Enter Student Name")
    usn = st.text_input("Enter USN")
    branch = st.text_input("Enter Branch")
    semester = st.number_input("Enter Current Semester", min_value=1, max_value=8)
    section = st.text_input("Enter Section")

    photo = st.file_uploader("Upload Student Photo", type=['png', 'jpg', 'jpeg'])

    if st.button("Save Details"):

        st.session_state.student_data = {
            'name': name,
            'usn': usn,
            'branch': branch,
            'semester': semester,
            'section': section
        }

        if photo:
            image = Image.open(photo)
            image.save("student_photo.jpg")

        st.success("Student Details Saved Successfully")

# ---------------------------------------------------
# SGPA CALCULATOR
# ---------------------------------------------------

elif page == "SGPA Calculator":

    st.header("📘 SGPA Calculator")

    num_subjects = st.number_input(
        "Enter Number of Subjects",
        min_value=1,
        max_value=15,
        step=1
    )

    total_credits = 0
    total_points = 0

    subject_data = []

    for i in range(int(num_subjects)):

        st.subheader(f"Subject {i+1}")

        subject = st.text_input(f"Subject Name {i+1}")

        credits = st.number_input(
            f"Credits {i+1}",
            min_value=1.0,
            max_value=10.0,
            step=0.5
        )

        grade = st.selectbox(
            f"Grade {i+1}",
            list(grade_map.keys()),
            key=i
        )

        points = credits * grade_map[grade]

        total_credits += credits
        total_points += points

        subject_data.append([
            subject,
            credits,
            grade,
            points
        ])

    if st.button("Calculate SGPA"):

        sgpa = total_points / total_credits

        st.success(f"Your SGPA is: {round(sgpa, 2)}")

        st.session_state.sgpa_list.append(round(sgpa, 2))

        df = pd.DataFrame(
            subject_data,
            columns=['Subject', 'Credits', 'Grade', 'Credit Points']
        )

        st.dataframe(df)

        # Performance Message
        if sgpa >= 9:
            st.success("Outstanding Performance ⭐")

        elif sgpa >= 8:
            st.info("Excellent Performance 🔥")

        elif sgpa >= 7:
            st.warning("Good Performance 👍")

        else:
            st.error("Need Improvement 📚")

# ---------------------------------------------------
# CGPA CALCULATOR
# ---------------------------------------------------

elif page == "CGPA Calculator":

    st.header("📗 CGPA Calculator")

    if len(st.session_state.sgpa_list) == 0:
        st.warning("Please calculate SGPA first")

    else:

        st.write("Semester-wise SGPA")

        for i, val in enumerate(st.session_state.sgpa_list):
            st.write(f"Semester {i+1}: {val}")

        cgpa = sum(st.session_state.sgpa_list) / len(st.session_state.sgpa_list)

        st.success(f"Your CGPA is: {round(cgpa, 2)}")

# ---------------------------------------------------
# TARGET ANALYZER
# ---------------------------------------------------

elif page == "Target Analyzer":

    st.header("🎯 What-If Target Analyzer")

    current_cgpa = st.number_input(
        "Current CGPA",
        min_value=0.0,
        max_value=10.0,
        step=0.1
    )

    target_cgpa = st.number_input(
        "Target CGPA",
        min_value=0.0,
        max_value=10.0,
        step=0.1
    )

    completed_sem = st.number_input(
        "Completed Semesters",
        min_value=1,
        max_value=8
    )

    total_sem = 8

    if st.button("Analyze"):

        remaining = total_sem - completed_sem

        required_sgpa = (
            (target_cgpa * total_sem) - (current_cgpa * completed_sem)
        ) / remaining

        st.success(
            f"Required SGPA in Remaining Semesters: {round(required_sgpa,2)}"
        )

        if required_sgpa <= 8:
            st.success("Target is Easily Achievable ✅")

        elif required_sgpa <= 9:
            st.warning("Need Consistent Hard Work ⚡")

        else:
            st.error("Very Difficult Target 🚨")

# ---------------------------------------------------
# AI GRADE PREDICTOR
# ---------------------------------------------------

elif page == "AI Grade Predictor":

    st.header("🤖 AI/ML Grade Predictor")

    sem1 = st.number_input("Semester 1 SGPA", 0.0, 10.0)
    sem2 = st.number_input("Semester 2 SGPA", 0.0, 10.0)
    sem3 = st.number_input("Semester 3 SGPA", 0.0, 10.0)

    if st.button("Predict Future SGPA"):

        X = np.array([1, 2, 3]).reshape(-1, 1)
        y = np.array([sem1, sem2, sem3])

        model = LinearRegression()
        model.fit(X, y)

        prediction = model.predict([[4]])

        st.success(
            f"Predicted SGPA for Next Semester: {round(prediction[0],2)}"
        )

        # Graph
        semesters = [1,2,3,4]
        values = [sem1, sem2, sem3, prediction[0]]

        fig = px.line(
            x=semesters,
            y=values,
            markers=True,
            title="Academic Performance Prediction"
        )

        st.plotly_chart(fig)

# ---------------------------------------------------
# ANALYTICS DASHBOARD
# ---------------------------------------------------

elif page == "Analytics Dashboard":

    st.header("📊 Analytics Dashboard")

    if len(st.session_state.sgpa_list) == 0:
        st.warning("No Data Available")

    else:

        semesters = []

        for i in range(len(st.session_state.sgpa_list)):
            semesters.append(f"Sem {i+1}")

        df = pd.DataFrame({
            'Semester': semesters,
            'SGPA': st.session_state.sgpa_list
        })

        st.subheader("Bar Graph")

        fig = px.bar(
            df,
            x='Semester',
            y='SGPA',
            text='SGPA'
        )

        st.plotly_chart(fig)

        st.subheader("Line Chart")

        fig2 = px.line(
            df,
            x='Semester',
            y='SGPA',
            markers=True
        )

        st.plotly_chart(fig2)

# ---------------------------------------------------
# PDF TRANSCRIPT
# ---------------------------------------------------

elif page == "Download Transcript":

    st.header("📄 Download Academic Transcript")

    if st.button("Generate PDF"):

        doc = SimpleDocTemplate(
            "BMSCE_Transcript.pdf",
            pagesize=letter
        )

        styles = getSampleStyleSheet()
        elements = []

        title = Paragraph(
            "BMSCE Academic Transcript",
            styles['Title']
        )

        elements.append(title)
        elements.append(Spacer(1, 20))

        student = st.session_state.student_data

        details = [
            ["Name", student.get('name', '')],
            ["USN", student.get('usn', '')],
            ["Branch", student.get('branch', '')],
            ["Semester", student.get('semester', '')],
            ["Section", student.get('section', '')]
        ]

        detail_table = Table(details)

        detail_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold')
        ]))

        elements.append(detail_table)
        elements.append(Spacer(1, 20))

        sgpa_data = [["Semester", "SGPA"]]

        for i, val in enumerate(st.session_state.sgpa_list):
            sgpa_data.append([f"Semester {i+1}", val])

        table = Table(sgpa_data)

        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.gray),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold')
        ]))

        elements.append(table)

        cgpa = 0

        if len(st.session_state.sgpa_list) > 0:
            cgpa = sum(st.session_state.sgpa_list) / len(st.session_state.sgpa_list)

        elements.append(Spacer(1, 20))

        cgpa_para = Paragraph(
            f"Final CGPA: {round(cgpa,2)}",
            styles['Heading2']
        )

        elements.append(cgpa_para)

        doc.build(elements)

        with open("BMSCE_Transcript.pdf", "rb") as file:

            st.download_button(
                label="Download Transcript PDF",
                data=file,
                file_name="BMSCE_Transcript.pdf",
                mime="application/pdf"
            )

        st.success("PDF Generated Successfully")

