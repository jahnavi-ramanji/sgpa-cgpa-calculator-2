import streamlit as st

st.set_page_config(page_title="SGPA & CGPA Calculator")

st.title("🎓 SGPA & CGPA Calculator")

# Store SGPA values
if "sgpa_list" not in st.session_state:
    st.session_state.sgpa_list = []

st.header("SGPA Calculator")

num_subjects = st.number_input(
    "Enter number of subjects",
    min_value=1,
    step=1
)

total_credits = 0
total_credit_points = 0

for i in range(int(num_subjects)):
    st.subheader(f"Subject {i+1}")

    credits = st.number_input(
        f"Credits for Subject {i+1}",
        min_value=0.0,
        step=0.5,
        key=f"c{i}"
    )

    grade = st.number_input(
        f"Grade Point for Subject {i+1}",
        min_value=0.0,
        max_value=10.0,
        step=0.1,
        key=f"g{i}"
    )

    total_credits += credits
    total_credit_points += credits * grade

if st.button("Calculate SGPA"):
    if total_credits > 0:
        sgpa = total_credit_points / total_credits
        st.success(f"Your SGPA is: {round(sgpa,2)}")

        st.session_state.sgpa_list.append(sgpa)

# CGPA Section
st.header("CGPA Calculator")

if st.button("Calculate CGPA"):
    if len(st.session_state.sgpa_list) > 0:
        cgpa = sum(st.session_state.sgpa_list) / len(st.session_state.sgpa_list)
        st.success(f"Your CGPA is: {round(cgpa,2)}")

# Display stored SGPAs
if st.session_state.sgpa_list:
    st.sidebar.header("Saved SGPA Records")

    for idx, value in enumerate(st.session_state.sgpa_list, start=1):
        st.sidebar.write(f"Semester {idx}: {round(value,2)}")
