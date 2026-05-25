import streamlit as st
import pandas as pd

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="BMSCE SGPA & CGPA Analytics Portal",
    page_icon="🎓",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #F4F8FC;
}

/* Welcome Box */
.welcome-box {
    background-color: #003366;
    padding: 40px;
    border-radius: 15px;
    text-align: center;
    color: white;
}

/* Main Title */
.main-title {
    font-size: 42px;
    font-weight: bold;
}

/* Subtitle */
.sub-title {
    font-size: 20px;
    color: #DCE6F2;
}

/* Buttons */
.stButton > button {
    background-color: #0056B3;
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 100%;
    font-size: 18px;
    border: none;
}

.stButton > button:hover {
    background-color: #003D80;
    color: white;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background-color: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"

if "sgpa_list" not in st.session_state:
    st.session_state.sgpa_list = []

# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------

if st.session_state.page == "home":

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.image(
        "https://www.bmsce.ac.in/assets/img/bmsce-logo.png",
        width=180
    )

    st.markdown("""
    <div class="welcome-box">

        <div class="main-title">
            WELCOME TO
        </div>

        <br>

        <div class="main-title">
            BMSCE SGPA & CGPA
            ANALYTICS PORTAL
        </div>

        <br>

        <div class="sub-title">
            Student Academic Performance
            Management System
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 START PORTAL"):

        st.session_state.page = "portal"

        st.rerun()

# ---------------------------------------------------
# PORTAL PAGE
# ---------------------------------------------------

elif st.session_state.page == "portal":

    # HEADER

    col1, col2 = st.columns([1, 6])

    with col1:
        st.image(
            "https://www.bmsce.ac.in/assets/img/bmsce-logo.png",
            width=100
        )

    with col2:
        st.title(
            "🎓 BMSCE SGPA & CGPA Analytics Portal"
        )

        st.subheader(
            "Student Academic Performance Management System"
        )

    st.markdown("---")

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

    photo = st.file_uploader(
        "Upload Student Photo",
        type=["png", "jpg", "jpeg"]
    )

    st.markdown("---")

    # ---------------------------------------------------
    # SEMESTER DETAILS
    # ---------------------------------------------------

    num_semesters = st.number_input(
        "Enter Number of Semesters",
        min_value=1,
        step=1
    )

    grade_dict = {
        "O": 10,
        "A+": 9,
        "A": 8,
        "B+": 7,
        "B": 6,
        "C": 5,
        "F": 0
    }

    current_sgpas = []

    subject_table = []

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

        # SUBJECT LOOP

        for i in range(int(num_subjects)):

            st.subheader(f"Subject {i + 1}")

            subject_name = st.text_input(
                "Enter Subject Name",
                key=f"subject{sem}{i}"
            )

            credits = st.number_input(
                "Enter Credits",
                min_value=0.0,
                step=0.5,
                key=f"credits{sem}{i}"
            )

            grade_letter = st.selectbox(
                "Select Grade",
                list(grade_dict.keys()),
                key=f"grade{sem}{i}"
            )

            grade_point = grade_dict[grade_letter]

            total_credits += credits

            total_credit_points += (
                credits * grade_point
            )

            subject_table.append({

                "Semester": sem + 1,
                "Subject": subject_name,
                "Credits": credits,
                "Grade": grade_letter,
                "Grade Point": grade_point

            })

        # SGPA

        if total_credits > 0:

            sgpa = (
                total_credit_points
                / total_credits
            )

            current_sgpas.append(sgpa)

            st.success(
                f"SGPA of Semester {sem + 1}: {round(sgpa, 2)}"
            )

    # ---------------------------------------------------
    # GENERATE RESULT
    # ---------------------------------------------------

    if st.button("🎯 GENERATE RESULT"):

        st.session_state.sgpa_list = current_sgpas.copy()

        if len(st.session_state.sgpa_list) > 0:

            cgpa = (
                sum(st.session_state.sgpa_list)
                / len(st.session_state.sgpa_list)
            )

            percentage = (
                (cgpa - 0.75) * 10
            )

            st.markdown("---")

            st.header("📊 RESULT DASHBOARD")

            # PHOTO

            if photo is not None:
                st.image(photo, width=150)

            # STUDENT DETAILS

            st.subheader("👨‍🎓 Student Information")

            st.write(f"Name: {name}")
            st.write(f"USN: {usn}")
            st.write(f"Branch: {branch}")
            st.write(f"Section: {section}")
            st.write(f"Academic Year: {academic_year}")

            st.markdown("---")

            # METRICS

            col1, col2 = st.columns(2)

            col1.metric(
                "CGPA",
                round(cgpa, 2)
            )

            col2.metric(
                "Percentage",
                f"{round(percentage,2)}%"
            )

            st.markdown("---")

            # PERFORMANCE

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

            elif cgpa >= 6:

                st.warning(
                    "🙂 Average Performance"
                )

            else:

                st.error(
                    "📚 Needs Improvement"
                )

            st.markdown("---")

            # SGPA TABLE

            st.subheader(
                "📚 Semester-wise SGPA"
            )

            sgpa_df = pd.DataFrame({

                "Semester": range(
                    1,
                    len(st.session_state.sgpa_list)+1
                ),

                "SGPA": st.session_state.sgpa_list

            })

            st.table(sgpa_df)

            # SUBJECT TABLE

            st.subheader(
                "📖 Subject Details"
            )

            st.table(
                pd.DataFrame(subject_table)
            )

            st.markdown("---")

            # GRAPH

            st.subheader(
                "📉 SGPA Trend Graph"
            )

            st.line_chart(
                sgpa_df.set_index("Semester")
            )

            st.markdown("---")

            # DOWNLOAD BUTTON

            st.download_button(
                label="📥 Download Result",
                data=sgpa_df.to_csv(index=False),
                file_name="BMSCE_Result.csv",
                mime="text/csv"
            )

            # START OVER

            if st.button("🔄 START OVER"):

                st.session_state.page = "home"

                st.session_state.sgpa_list = []

                st.rerun()

    st.markdown("---")

    st.caption(
        "Developed by Jahnavi R | Department of Aerospace Engineering"
    )
