import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.metrics import interview_success_rate, round_efficiency


def dashboard():

    st.title("PragyanAI Placement Intelligence Engine")

    # ---------------------------------------------------
    # LOAD DATA
    # ---------------------------------------------------

    @st.cache_data
    def load_data():

        url = "https://raw.githubusercontent.com/pragyanaischool/VTU_Internship_DataSets/refs/heads/main/student_data_placement_interview_funnel_analysis_project_10.csv"

        try:
            df = pd.read_csv(url)

        except:
            df = pd.read_csv(
                url,
                encoding='latin1',
                on_bad_lines='skip'
            )

        return df

    df = load_data()

    df.columns = df.columns.str.strip()

    # ---------------------------------------------------
    # SIDEBAR
    # ---------------------------------------------------

    st.sidebar.title("⚙ Dashboard Panel")

    st.sidebar.header("🔍 Filters")

    domain = st.sidebar.multiselect(
        "Domain",
        df["Domain"].unique()
    )

    company = st.sidebar.multiselect(
        "Company Tier",
        df["Company_Tier"].unique()
    )

    role = st.sidebar.multiselect(
        "Job Role",
        df["Job_Role"].unique()
    )

    # ---------------------------------------------------
    # APPLY FILTERS
    # ---------------------------------------------------

    if st.sidebar.button("Apply Filters"):

        if domain:
            df = df[df["Domain"].isin(domain)]

        if company:
            df = df[df["Company_Tier"].isin(company)]

        if role:
            df = df[df["Job_Role"].isin(role)]

    # ---------------------------------------------------
    # RESET FILTERS
    # ---------------------------------------------------

    if st.sidebar.button("Reset Filters"):

        st.rerun()

    # ---------------------------------------------------
    # ADMIN PANEL
    # ---------------------------------------------------

    if st.session_state.get("user") == "admin":

        st.sidebar.markdown("---")

        st.sidebar.subheader("🛠 Admin Controls")

        if st.sidebar.button("🎓 Student Management"):

            st.session_state.page = "students"

            st.rerun()

    # ---------------------------------------------------
    # LOGOUT
    # ---------------------------------------------------

    st.sidebar.markdown("---")

    if st.sidebar.button("🚪 Logout"):

        st.session_state.logged_in = False

        st.session_state.page = "landing"

        st.rerun()

    # ---------------------------------------------------
    # KPIs
    # ---------------------------------------------------

    st.subheader("📊 Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Students", len(df))

    col2.metric(
        "Success Rate",
        f"{interview_success_rate(df):.2%}"
    )

    col3.metric(
        "Efficiency",
        f"{round_efficiency(df):.2%}"
    )

    col4.metric(
        "Placed",
        df["Joined"].sum()
    )

    # ---------------------------------------------------
    # TABS
    # ---------------------------------------------------

    tab1, tab2, tab3, tab4 = st.tabs([
        "📉 Funnel",
        "🔥 Failures",
        "💼 Roles & Salary",
        "🧠 Skills"
    ])

    # ---------------------------------------------------
    # TAB 1
    # ---------------------------------------------------

    with tab1:

        st.subheader("📉 Placement Funnel")

        funnel_data = {

            "Applied": df["Applied"].sum(),
            "Shortlisted": df["Shortlisted"].sum(),
            "Interview": df["Interview_Attended"].sum(),
            "Offer": df["Offer_Received"].sum(),
            "Joined": df["Joined"].sum()

        }

        st.bar_chart(funnel_data)

    # ---------------------------------------------------
    # TAB 2
    # ---------------------------------------------------

    with tab2:

        st.subheader("🔥 Failure Stage Distribution")

        failure_data = df["Failed_Stage"].value_counts()

        st.bar_chart(failure_data)

    # ---------------------------------------------------
    # TAB 3
    # ---------------------------------------------------

    with tab3:

        st.subheader("📊 Job Roles vs Placement")

        role_data = df.groupby("Job_Role")["Joined"].sum()

        st.bar_chart(role_data)

        st.markdown("---")

        st.subheader("💰 Salary Distribution")

        fig, ax = plt.subplots()

        ax.hist(df["Salary_LPA"], bins=30)

        ax.set_title("Salary Distribution")

        ax.set_xlabel("Salary (LPA)")

        ax.set_ylabel("Frequency")

        st.pyplot(fig)

    # ---------------------------------------------------
    # TAB 4
    # ---------------------------------------------------

    with tab4:

        st.subheader("🧠 Skills Impact")

        if "Skill_Programs" in df.columns:

            skill_data = df.groupby(
                "Skill_Programs"
            )["Joined"].mean()

            st.bar_chart(skill_data)

        if "Internships" in df.columns:

            intern_data = df.groupby(
                "Internships"
            )["Joined"].mean()

            st.bar_chart(intern_data)

        if "Projects" in df.columns:

            project_data = df.groupby(
                "Projects"
            )["Joined"].mean()

            st.bar_chart(project_data)

    # ---------------------------------------------------
    # PROBABILITY CALCULATOR
    # ---------------------------------------------------

    st.markdown("## 🎯 Placement Probability Calculator")

    cgpa = st.slider("CGPA", 0.0, 10.0, 7.0)

    skills = st.slider("Skill Programs", 0, 5, 2)

    projects = st.slider("Projects", 0, 10, 3)

    internships = st.slider("Internships", 0, 5, 1)

    prob = (cgpa + skills + projects + internships) / 25

    st.metric(
        "Estimated Probability",
        f"{prob:.2%}"
    )

    # ---------------------------------------------------
    # SEARCH
    # ---------------------------------------------------

    st.subheader("🔍 Student Search")

    sid = st.text_input("Enter Student ID")

    if sid:

        result = df[df["Student_ID"].astype(str) == sid]

        result = result.drop(
            columns=["Failed_Stage"],
            errors="ignore"
        )

        st.dataframe(
            result,
            hide_index=True
        )

    # ---------------------------------------------------
    # DOWNLOAD
    # ---------------------------------------------------

    st.subheader("📥 Download Data")

    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "Download CSV",
        csv,
        "data.csv"
    )

    # ---------------------------------------------------
    # TOP STUDENTS
    # ---------------------------------------------------

    st.subheader("🏆 Top Students")

    top = df.sort_values(
        by="CGPA",
        ascending=False
    ).head(10)

    top = top.drop(
        columns=["Failed_Stage"],
        errors="ignore"
    )

    st.dataframe(
        top,
        hide_index=True
    )

    # ---------------------------------------------------
    # INSIGHTS
    # ---------------------------------------------------

    st.subheader("📌 Insights")

    st.write("Interview stage biggest bottleneck")

    st.write("Coding + Tech failures high")

    st.write("Projects + internships boost success")

    st.markdown("---")

    st.write("🚀 Built with Streamlit")
