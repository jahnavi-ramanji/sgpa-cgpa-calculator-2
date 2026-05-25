import streamlit as st
import pandas as pd

# --- PAGE SETUP ---
st.set_page_config(page_title="BMSCE Student Portal", page_icon="🎓", layout="centered")

# --- SESSION STATE SETUP (The Memory) ---
# This tells the app which screen to show. It starts on 'welcome'.
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'welcome'

# --- NAVIGATION FUNCTIONS ---
def go_to_calculator():
    st.session_state.current_screen = 'calculator'

def go_to_results(student_name, usn, df, sgpa):
    # Save the data into memory before switching screens
    st.session_state.student_name = student_name
    st.session_state.usn = usn
    st.session_state.df = df
    st.session_state.sgpa = sgpa
    st.session_state.current_screen = 'result'

def start_over():
    st.session_state.current_screen = 'welcome'

# --- GRADE DICTIONARY ---
grade_points = {"O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5, "P": 4, "F": 0}

# ==========================================
# SCREEN 1: THE WELCOME PORTAL
# ==========================================
if st.session_state.current_screen == 'welcome':
    st.markdown("<h1 style='text-align: center;'>Welcome to BMSCE Student Portal</h1>", unsafe_allow_html=True)
    
    # Adding a placeholder for the logo
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/en/thumb/f/f8/BMS_College_of_Engineering_logo.svg/1200px-BMS_College_of_Engineering_logo.svg.png", use_container_width=True)
        st.markdown("<p style='text-align: center; color: gray;'>AI/ML Engineering Department</p>", unsafe_allow_html=True)
        
        st.write("") # Spacing
        # The start button that triggers the screen change
        st.button("Start SGPA Calculator ➔", on_click=go_to_calculator, type="primary", use_container_width=True)


# ==========================================
# SCREEN 2: THE INPUT FORM
# ==========================================
elif st.session_state.current_screen == 'calculator':
    st.title("Academic Calculator")
    st.write("Please enter your details and marks.")

    # Student Info
    col1, col2 = st.columns(2)
    with col1:
        name_input = st.text_input("Full Name")
    with col2:
        usn_input = st.text_input("USN")

    st.markdown("### Enter Subject Details")
    
    subjects, credits, grades = [], [], []
    
    # Taking 5 subjects as an example for the form
    for i in range(5):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            subj = st.text_input(f"Subject {i+1}", key=f"sub_{i}")
        with c2:
            cred = st.number_input(f"Credits", min_value=1, max_value=5, value=3, key=f"cred_{i}")
        with c3:
            grade = st.selectbox(f"Grade", options=list(grade_points.keys()), key=f"grade_{i}")
        
        subjects.append(subj if subj else f"Subject {i+1}")
        credits.append(cred)
        grades.append(grade)

    # When this is clicked, we calculate the data, save it, and swap to Screen 3
    if st.button("Generate Result Report"):
        if name_input and usn_input:
            # Math
            total_credits = sum(credits)
            earned_points = sum([credits[i] * grade_points[grades[i]] for i in range(len(credits))])
            calculated_sgpa = earned_points / total_credits if total_credits > 0 else 0
            
            # Formatting Data
            result_df = pd.DataFrame({
                "Subject": subjects,
                "Credits": credits,
                "Grade": grades,
                "Points Earned": [credits[i] * grade_points[grades[i]] for i in range(len(credits))]
            })
            
            # Switch to results page
            go_to_results(name_input, usn_input, result_df, calculated_sgpa)
        else:
            st.warning("Please enter your Name and USN before generating the result.")


# ==========================================
# SCREEN 3: THE FINAL RESULT PAGE
# ==========================================
elif st.session_state.current_screen == 'result':
    st.title("🎓 Official Result Transcript")
    
    # Display the saved data from memory
    st.markdown(f"**Student Name:** {st.session_state.student_name}")
    st.markdown(f"**USN:** {st.session_state.usn}")
    
    st.divider()
    
    # Display the final SGPA prominently
    st.metric(label="Final SGPA", value=f"{st.session_state.sgpa:.2f}")
    
    # Display the table
    st.dataframe(st.session_state.df, use_container_width=True)
    
    # Visual chart for the generated page
    st.bar_chart(data=st.session_state.df, x="Subject", y="Points Earned")
    
    st.divider()
    
    # The return button to clear and start over
    st.button("← Return to Home", on_click=start_over)
