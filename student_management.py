import streamlit as st
import pandas as pd
import os

FILE = "students.csv"


# ---------------------------------------------------
# LOAD STUDENTS
# ---------------------------------------------------
def load_students():

    if not os.path.exists(FILE):

        df = pd.DataFrame(columns=[
            "Student_ID",
            "Name",
            "CGPA",
            "Domain",
            "Job_Role",
            "Company_Tier",
            "Skill_Programs",
            "Projects",
            "Internships"
        ])

        df.to_csv(FILE, index=False)

    return pd.read_csv(FILE)


# ---------------------------------------------------
# SAVE STUDENTS
# ---------------------------------------------------
def save_students(df):

    df.to_csv(FILE, index=False)


# ---------------------------------------------------
# MAIN PAGE
# ---------------------------------------------------
def student_management_page():

    # ---------------------------------------------------
    # PAGE STYLE
    # ---------------------------------------------------

    st.markdown("""
    <style>

    .stApp {
        background: linear-gradient(135deg, #edf2fb, #d7e3fc);
    }

    .main-title {
        text-align:center;
        font-size:40px;
        font-weight:bold;
        color:#0f172a;
        margin-bottom:20px;
    }

    .section-box {
        background:white;
        padding:25px;
        border-radius:15px;
        box-shadow:0px 0px 15px rgba(0,0,0,0.08);
        margin-bottom:20px;
    }

    .stButton button {
        width:100%;
        background:#0f172a;
        color:white;
        border:none;
        border-radius:10px;
        padding:12px;
        font-weight:bold;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div class='main-title'>🎓 Student Management System</div>",
        unsafe_allow_html=True
    )

    df = load_students()

    # ---------------------------------------------------
    # TOP BUTTONS
    # ---------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        if st.button("⬅ Back To Dashboard"):

            st.session_state.page = "dashboard"
            st.rerun()

    with col2:

        if st.button("🚪 Logout"):

            st.session_state.logged_in = False
            st.session_state.page = "landing"
            st.rerun()

    st.markdown("---")

    # ===================================================
    # ADD STUDENT
    # ===================================================

    st.markdown("<div class='section-box'>", unsafe_allow_html=True)

    st.subheader("➕ Add New Student")

    col1, col2 = st.columns(2)

    with col1:

        sid = st.text_input("Student ID")

        name = st.text_input("Student Name")

        cgpa = st.number_input(
            "CGPA",
            min_value=0.0,
            max_value=10.0,
            value=7.0,
            step=0.1
        )

        domain = st.selectbox(
            "Domain",
            [
                "AI",
                "Web Development",
                "Cloud Computing",
                "Cyber Security",
                "Data Science",
                "Machine Learning"
            ]
        )

    with col2:

        role = st.selectbox(
            "Job Role",
            [
                "Software Developer",
                "Data Analyst",
                "ML Engineer",
                "Cloud Engineer",
                "Tester"
            ]
        )

        company = st.selectbox(
            "Company Tier",
            [
                "Tier 1",
                "Tier 2",
                "Tier 3"
            ]
        )

        skills = st.slider("Skill Programs", 0, 10, 2)

        projects = st.slider("Projects", 0, 10, 2)

        internships = st.slider("Internships", 0, 5, 1)

    # ---------------------------------------------------
    # ADD BUTTON
    # ---------------------------------------------------

    if st.button("✅ ADD STUDENT"):

        sid = str(sid).strip()

        if sid == "" or name == "":

            st.error("Please fill all required fields")

        elif sid in df["Student_ID"].astype(str).values:

            st.error("Student ID already exists")

        else:

            new_student = pd.DataFrame([{

                "Student_ID": sid,
                "Name": name,
                "CGPA": cgpa,
                "Domain": domain,
                "Job_Role": role,
                "Company_Tier": company,
                "Skill_Programs": skills,
                "Projects": projects,
                "Internships": internships

            }])

            df = pd.concat([df, new_student], ignore_index=True)

            save_students(df)

            st.success("Student Added Successfully ✅")

            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # ===================================================
    # REMOVE STUDENT
    # ===================================================

    st.markdown("<div class='section-box'>", unsafe_allow_html=True)

    st.subheader("❌ Remove Student")

    remove_id = st.text_input("Enter Student ID To Remove")

    if st.button("🗑 REMOVE STUDENT"):

        remove_id = str(remove_id).strip()

        if remove_id in df["Student_ID"].astype(str).values:

            df = df[df["Student_ID"].astype(str) != remove_id]

            save_students(df)

            st.success("Student Removed Successfully ✅")

            st.rerun()

        else:

            st.error("Student ID Not Found")

    st.markdown("</div>", unsafe_allow_html=True)

    # ===================================================
    # STUDENT SEARCH
    # ===================================================

    st.markdown("<div class='section-box'>", unsafe_allow_html=True)

    st.subheader("🔍 Search Student")

    search_id = st.text_input("Enter Student ID")

    if search_id:

        result = df[df["Student_ID"].astype(str) == search_id]

        if result.empty:

            st.warning("No Student Found")

        else:

            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

    # ===================================================
    # ALL STUDENTS
    # ===================================================

    st.markdown("<div class='section-box'>", unsafe_allow_html=True)

    st.subheader("📋 All Students")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # ===================================================
    # DOWNLOAD
    # ===================================================

    st.markdown("<div class='section-box'>", unsafe_allow_html=True)

    st.subheader("📥 Download Student Data")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download CSV",
        csv,
        "students.csv",
        "text/csv"
    )

    st.markdown("</div>", unsafe_allow_html=True)
