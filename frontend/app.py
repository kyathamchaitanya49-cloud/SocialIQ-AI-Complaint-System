import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SocialIQ AI Complaint System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "https://socialiq-ai-complaint-system.onrender.com/predict"

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f5f7fb;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* Main title */
    .main-title {
        font-size: 32px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 4px;
    }

    .subtitle {
        color: #6b7280;
        font-size: 15px;
        margin-bottom: 25px;
    }

    /* KPI cards */
    .kpi-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        min-height: 120px;
    }

    .kpi-title {
        color: #6b7280;
        font-size: 14px;
        font-weight: 500;
    }

    .kpi-value {
        color: #111827;
        font-size: 30px;
        font-weight: 700;
        margin-top: 8px;
    }

    .section-title {
        font-size: 21px;
        font-weight: 650;
        color: #111827;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    /* AI result cards */
    .result-card {
        background: white;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        min-height: 110px;
    }

    .result-label {
        color: #6b7280;
        font-size: 13px;
    }

    .result-value {
        color: #111827;
        font-size: 17px;
        font-weight: 650;
        margin-top: 8px;
    }

    /* Complaint details */
    .complaint-box {
        background: white;
        padding: 22px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-bottom: 15px;
    }

    /* Sidebar brand */
    .brand {
        text-align: center;
        padding: 10px 5px 25px 5px;
    }

    .brand-icon {
        font-size: 42px;
    }

    .brand-title {
        font-size: 20px;
        font-weight: 700;
        color: white;
    }

    .brand-subtitle {
        font-size: 12px;
        color: #9ca3af;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "complaints" not in st.session_state:
    st.session_state.complaints = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# ============================================================
# API FUNCTION
# ============================================================

def analyze_complaint(citizen_name, complaint):

    payload = {
        "citizen_name": citizen_name,
        "complaint": complaint
    }

    try:

        response = requests.post(
            API_URL,
            json=payload,
            timeout=120
        )

        if response.status_code == 200:

            data = response.json()

            prediction = data.get("prediction", {})

            record = {
                "Complaint ID": data.get("complaint_id", "N/A"),
                "Citizen Name": citizen_name,
                "Complaint": complaint,
                "Department": prediction.get("department", "N/A"),
                "Feedback": prediction.get("feedback_category", "N/A"),
                "Sentiment": prediction.get("sentiment", "N/A"),
                "Harmful": prediction.get("harmful", "N/A"),
                "Emergency": prediction.get("emergency", "N/A"),
                "Priority": prediction.get("priority", "N/A"),
                "Trend": prediction.get("trend", "N/A"),
                "Anomaly": prediction.get("anomaly", "N/A"),
                "Government Action": prediction.get(
                    "government_action",
                    "N/A"
                ),
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }

            # Prevent duplicate records during reruns
            existing_ids = [
                x["Complaint ID"]
                for x in st.session_state.complaints
            ]

            if record["Complaint ID"] not in existing_ids:
                st.session_state.complaints.append(record)

            st.session_state.last_result = record

            return record, None

        return None, f"Backend returned HTTP {response.status_code}: {response.text}"

    except requests.exceptions.Timeout:

        return None, (
            "The backend took too long to respond. "
            "Render may be waking up. Please try again."
        )

    except requests.exceptions.ConnectionError:

        return None, (
            "Could not connect to the SocialIQ backend."
        )

    except Exception as e:

        return None, str(e)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("""
    <div class="brand">
        <div class="brand-icon">🏛️</div>
        <div class="brand-title">SocialIQ</div>
        <div class="brand-subtitle">
            AI Government Complaint System
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📋 Complaints",
            "📊 Analytics",
            "🚨 Anomaly Detection",
            "🤖 AI Recommendations",
            "📢 Announcements",
            "⚙️ Settings"
        ]
    )

    st.markdown("---")

    st.markdown(
        "### 🟢 System Status"
    )

    st.success("Backend Online")

    st.caption(
        "FastAPI + Machine Learning + Streamlit"
    )


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">Government Complaint Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'AI-powered monitoring and analysis of citizen complaints'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # KPI DATA
    # --------------------------------------------------------

    complaints = st.session_state.complaints

    total = len(complaints)

    urgent = sum(
        1 for x in complaints
        if str(x["Priority"]).lower() == "urgent"
    )

    emergency = sum(
        1 for x in complaints
        if "emergency" in str(x["Emergency"]).lower()
        and "non" not in str(x["Emergency"]).lower()
    )

    safe = sum(
        1 for x in complaints
        if str(x["Harmful"]).lower() == "safe"
    )

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">📋 Total Complaints</div>
            <div class="kpi-value">{total}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">⚠️ Urgent Complaints</div>
            <div class="kpi-value">{urgent}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">🚨 Emergency Cases</div>
            <div class="kpi-value">{emergency}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">🛡️ Safe Complaints</div>
            <div class="kpi-value">{safe}</div>
        </div>
        """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # QUICK COMPLAINT
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📝 Analyze New Complaint</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 2])

    with col1:

        citizen_name = st.text_input(
            "Citizen Name",
            placeholder="Enter citizen name",
            key="dashboard_name"
        )

    with col2:

        complaint = st.text_area(
            "Complaint",
            placeholder="Describe the citizen complaint...",
            height=100,
            key="dashboard_complaint"
        )

    if st.button(
        "🔍 Analyze Complaint",
        type="primary",
        use_container_width=True
    ):

        if not citizen_name.strip():
            st.warning("Please enter citizen name.")

        elif not complaint.strip():
            st.warning("Please enter complaint.")

        else:

            with st.spinner(
                "🤖 AI is analyzing the complaint..."
            ):

                record, error = analyze_complaint(
                    citizen_name,
                    complaint
                )

            if error:
                st.error(error)

            else:
                st.success(
                    f"Complaint #{record['Complaint ID']} analyzed successfully."
                )

    # --------------------------------------------------------
    # RECENT COMPLAINTS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📋 Recent Complaints</div>',
        unsafe_allow_html=True
    )

    if complaints:

        df = pd.DataFrame(complaints)

        display_columns = [
            "Complaint ID",
            "Citizen Name",
            "Department",
            "Priority",
            "Emergency",
            "Sentiment"
        ]

        st.dataframe(
            df[display_columns],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No complaints analyzed yet. "
            "Submit a complaint to populate the dashboard."
        )


# ============================================================
# COMPLAINTS
# ============================================================

elif page == "📋 Complaints":

    st.markdown(
        '<div class="main-title">Government Complaints</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'View, search and analyze citizen complaints'
        '</div>',
        unsafe_allow_html=True
    )

    complaints = st.session_state.complaints

    if not complaints:

        st.info(
            "No complaints available yet."
        )

    else:

        df = pd.DataFrame(complaints)

        # ----------------------------------------------------
        # SEARCH & FILTER
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">🔎 Search & Filters</div>',
            unsafe_allow_html=True
        )

        f1, f2, f3 = st.columns(3)

        with f1:

            search = st.text_input(
                "Search Complaint / Citizen",
                placeholder="Search..."
            )

        with f2:

            departments = [
                "All"
            ] + sorted(
                df["Department"].dropna().unique().tolist()
            )

            department_filter = st.selectbox(
                "Department",
                departments
            )

        with f3:

            priorities = [
                "All"
            ] + sorted(
                df["Priority"].dropna().unique().tolist()
            )

            priority_filter = st.selectbox(
                "Priority",
                priorities
            )

        f4, f5 = st.columns(2)

        with f4:

            emergency_filter = st.selectbox(
                "Emergency",
                ["All", "Emergency", "Non Emergency"]
            )

        with f5:

            sentiment_filter = st.selectbox(
                "Sentiment",
                ["All"] + sorted(
                    df["Sentiment"].dropna().unique().tolist()
                )
            )

        # ----------------------------------------------------
        # FILTER DATA
        # ----------------------------------------------------

        filtered = df.copy()

        if search:

            filtered = filtered[
                filtered["Citizen Name"]
                .astype(str)
                .str.contains(
                    search,
                    case=False,
                    na=False
                )
                |
                filtered["Complaint"]
                .astype(str)
                .str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        if department_filter != "All":

            filtered = filtered[
                filtered["Department"] == department_filter
            ]

        if priority_filter != "All":

            filtered = filtered[
                filtered["Priority"] == priority_filter
            ]

        if emergency_filter != "All":

            filtered = filtered[
                filtered["Emergency"]
                .astype(str)
                .str.contains(
                    emergency_filter,
                    case=False,
                    na=False
                )
            ]

        if sentiment_filter != "All":

            filtered = filtered[
                filtered["Sentiment"] == sentiment_filter
            ]

        st.write(
            f"📊 **Complaints Found: {len(filtered)}**"
        )

        display_columns = [
            "Complaint ID",
            "Citizen Name",
            "Department",
            "Priority",
            "Emergency",
            "Sentiment",
            "Harmful"
        ]

        st.dataframe(
            filtered[display_columns],
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # COMPLAINT DETAILS
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">📄 Complaint Details</div>',
            unsafe_allow_html=True
        )

        selected_id = st.selectbox(
            "Select Complaint",
            filtered["Complaint ID"].tolist()
        )

        selected = filtered[
            filtered["Complaint ID"] == selected_id
        ].iloc[0]

        st.markdown(
            f"""
            <div class="complaint-box">
                <h3>📋 Complaint #{selected['Complaint ID']}</h3>
                <b>Citizen:</b> {selected['Citizen Name']}<br><br>
                <b>Complaint:</b><br>
                {selected['Complaint']}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-title">🤖 AI Analysis</div>',
            unsafe_allow_html=True
        )

        r1, r2, r3 = st.columns(3)

        with r1:
            st.metric(
                "🏢 Department",
                selected["Department"]
            )

        with r2:
            st.metric(
                "📂 Feedback",
                selected["Feedback"]
            )

        with r3:
            st.metric(
                "😊 Sentiment",
                selected["Sentiment"]
            )

        r4, r5, r6 = st.columns(3)

        with r4:
            st.metric(
                "🛡️ Harmful",
                selected["Harmful"]
            )

        with r5:
            st.metric(
                "🚨 Emergency",
                selected["Emergency"]
            )

        with r6:
            st.metric(
                "⚠️ Priority",
                selected["Priority"]
            )

        r7, r8 = st.columns(2)

        with r7:

            st.info(
                f"📈 **Trend**\n\n"
                f"{selected['Trend']}"
            )

        with r8:

            st.info(
                f"🔎 **Anomaly**\n\n"
                f"{selected['Anomaly']}"
            )

        st.success(
            f"🏛️ **Recommended Government Action:** "
            f"{selected['Government Action']}"
        )


# ============================================================
# ANALYTICS
# ============================================================

elif page == "📊 Analytics":

    st.markdown(
        '<div class="main-title">Complaint Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'AI-powered insights from citizen complaints'
        '</div>',
        unsafe_allow_html=True
    )

    complaints = st.session_state.complaints

    if not complaints:

        st.info(
            "Submit complaints to generate analytics."
        )

    else:

        df = pd.DataFrame(complaints)

        # ----------------------------------------------------
        # DEPARTMENT
        # ----------------------------------------------------

        c1, c2 = st.columns(2)

        with c1:

            dept_counts = (
                df["Department"]
                .value_counts()
                .reset_index()
            )

            dept_counts.columns = [
                "Department",
                "Complaints"
            ]

            fig = px.bar(
                dept_counts,
                x="Department",
                y="Complaints",
                title="🏢 Complaints by Department"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # SENTIMENT
        # ----------------------------------------------------

        with c2:

            sentiment_counts = (
                df["Sentiment"]
                .value_counts()
                .reset_index()
            )

            sentiment_counts.columns = [
                "Sentiment",
                "Complaints"
            ]

            fig = px.pie(
                sentiment_counts,
                names="Sentiment",
                values="Complaints",
                title="😊 Sentiment Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # PRIORITY
        # ----------------------------------------------------

        c3, c4 = st.columns(2)

        with c3:

            priority_counts = (
                df["Priority"]
                .value_counts()
                .reset_index()
            )

            priority_counts.columns = [
                "Priority",
                "Complaints"
            ]

            fig = px.bar(
                priority_counts,
                x="Priority",
                y="Complaints",
                title="⚠️ Priority Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # EMERGENCY
        # ----------------------------------------------------

        with c4:

            emergency_counts = (
                df["Emergency"]
                .value_counts()
                .reset_index()
            )

            emergency_counts.columns = [
                "Emergency",
                "Complaints"
            ]

            fig = px.pie(
                emergency_counts,
                names="Emergency",
                values="Complaints",
                title="🚨 Emergency Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # HARMFUL
        # ----------------------------------------------------

        harmful_counts = (
            df["Harmful"]
            .value_counts()
            .reset_index()
        )

        harmful_counts.columns = [
            "Harmful",
            "Complaints"
        ]

        fig = px.bar(
            harmful_counts,
            x="Harmful",
            y="Complaints",
            title="🛡️ Harmful vs Safe Complaints"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# ANOMALY DETECTION
# ============================================================

elif page == "🚨 Anomaly Detection":

    st.markdown(
        '<div class="main-title">Anomaly Detection</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Identify unusual complaint patterns using AI'
        '</div>',
        unsafe_allow_html=True
    )

    complaints = st.session_state.complaints

    if not complaints:

        st.info(
            "No complaint data available."
        )

    else:

        df = pd.DataFrame(complaints)

        anomaly_mask = ~df["Anomaly"].str.contains(
            "no anomaly",
            case=False,
            na=False
        )

        anomaly_df = df[anomaly_mask]

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "📋 Total Complaints",
                len(df)
            )

        with c2:
            st.metric(
                "🚨 Anomalies Detected",
                len(anomaly_df)
            )

        with c3:
            st.metric(
                "✅ Normal Complaints",
                len(df) - len(anomaly_df)
            )

        st.markdown(
            '<div class="section-title">🚨 Anomaly Results</div>',
            unsafe_allow_html=True
        )

        if len(anomaly_df) > 0:

            st.dataframe(
                anomaly_df[
                    [
                        "Complaint ID",
                        "Department",
                        "Priority",
                        "Anomaly"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

        else:

            st.success(
                "No anomalies detected in the available complaints."
            )


# ============================================================
# AI RECOMMENDATIONS
# ============================================================

elif page == "🤖 AI Recommendations":

    st.markdown(
        '<div class="main-title">AI Government Recommendations</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'AI-generated recommended government actions'
        '</div>',
        unsafe_allow_html=True
    )

    complaints = st.session_state.complaints

    if not complaints:

        st.info(
            "No recommendations available yet."
        )

    else:

        df = pd.DataFrame(complaints)

        grouped = (
            df.groupby(
                "Department"
            )
            .agg(
                Complaints=("Complaint ID", "count"),
                Urgent=("Priority",
                        lambda x: sum(
                            str(v).lower() == "urgent"
                            for v in x
                        ))
            )
            .reset_index()
        )

        for _, row in grouped.iterrows():

            department = row["Department"]

            department_df = df[
                df["Department"] == department
            ]

            actions = department_df[
                "Government Action"
            ].dropna().unique()

            with st.expander(
                f"🏢 {department} — "
                f"{row['Complaints']} complaints"
            ):

                st.write(
                    f"**Urgent complaints:** {row['Urgent']}"
                )

                st.write("### 🏛️ Recommended Actions")

                for action in actions:

                    st.success(
                        str(action)
                    )


# ============================================================
# ANNOUNCEMENTS
# ============================================================

elif page == "📢 Announcements":

    st.markdown(
        '<div class="main-title">Government Announcements</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Important public service announcements'
        '</div>',
        unsafe_allow_html=True
    )

    st.error(
        "🔴 Urgent Notice\n\n"
        "Monitor urgent and emergency complaints immediately."
    )

    st.warning(
        "🟡 Service Monitoring\n\n"
        "Departments with increasing complaint volumes should "
        "review the latest AI recommendations."
    )

    st.info(
        "🔵 System Update\n\n"
        "SocialIQ AI Complaint System is currently operational."
    )

    st.success(
        "🟢 Backend Status\n\n"
        "FastAPI prediction service is connected."
    )


# ============================================================
# SETTINGS
# ============================================================

elif page == "⚙️ Settings":

    st.markdown(
        '<div class="main-title">System Settings</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'SocialIQ system configuration and status'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        "### 🔗 Backend Configuration"
    )

    st.code(API_URL)

    st.success(
        "🟢 Backend API configured"
    )

    st.markdown(
        "### 🤖 AI Services"
    )

    services = {
        "Department": "department",
        "Feedback": "feedback_category",
        "Sentiment": "sentiment",
        "Harmful": "harmful",
        "Emergency": "emergency",
        "Priority": "priority",
        "Trend": "trend",
        "Anomaly": "anomaly",
        "Government Action": "government_action"
    }

    for service in services:

        st.write(
            f"✅ {service}"
        )

    st.markdown(
        "### 📦 Technology Stack"
    )

    st.write(
        """
        - FastAPI
        - Python
        - Scikit-learn
        - SQLAlchemy
        - PostgreSQL / Supabase
        - Streamlit
        - Plotly
        """
    )

    st.markdown(
        "### 📊 Current Session"
    )

    st.write(
        f"Complaints analyzed: "
        f"**{len(st.session_state.complaints)}**"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "SocialIQ AI Complaint System • "
    "AI-powered Government Complaint Management"
)