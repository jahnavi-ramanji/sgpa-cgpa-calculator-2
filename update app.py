import streamlit as st

st.set_page_config(page_title="SGPA & CGPA Calculator")

st.title("🎓 SGPA & CGPA Calculator")

# Enter number of semesters
num_semesters = st.number_input(
    "Enter number of semesters",
    min_value=1,
    step=1
)

sgpa_list = []

# Loop through semesters
for sem in range(int(num_semesters)):

    st.header(f"Semester {sem + 1}")

    num_subjects = st.number_input(
        f"Enter number of subjects in Semester {sem + 1}",
        min_value=1,
        step=1,
        key=f"sub{sem}"
    )

    total_credits = 0
    total_credit_points = 0

    # Loop through subjects
    for i in range(int(num_subjects)):

        st.subheader(f"Subject {i + 1}")

        credits = st.number_input(
            f"Credits for Subject {i + 1} (Semester {sem + 1})",
            min_value=0.0,
            step=0.5,
            key=f"c{sem}{i}"
        )

        grade = st.number_input(
            f"Grade Point for Subject {i + 1} (Semester {sem + 1})",
            min_value=0.0,
            max_value=10.0,
            step=0.1,
            key=f"g{sem}{i}"
        )

        total_credits += credits
        total_credit_points += credits * grade

    # Calculate SGPA
    if total_credits > 0:
        sgpa = total_credit_points / total_credits
        sgpa_list.append(sgpa)

        st.success(f"SGPA of Semester {sem + 1}: {round(sgpa, 2)}")

# Calculate CGPA
if len(sgpa_list) > 0:

    cgpa = sum(sgpa_list) / len(sgpa_list)

    st.header("Final CGPA")
    st.success(f"Your CGPA is: {round(cgpa, 2)}")
