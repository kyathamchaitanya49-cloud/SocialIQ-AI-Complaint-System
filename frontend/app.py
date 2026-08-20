import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SocialIQ AI Complaint Management System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# BACKEND
# ============================================================

API_URL = "https://socialiq-ai-complaint-system.onrender.com/predict"

# ============================================================
# SESSION STATE
# ============================================================

if "complaints" not in st.session_state:
    st.session_state.complaints = []

if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #0e1117;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #171a24;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }

    /* Sidebar text */
    .sidebar-title {
        font-size: 22px;
        font-weight: 700;
        color: white;
        text-align: center;
    }

    .sidebar-subtitle {
        font-size: 12px;
        color: #b8bcc8;
        text-align: center;
        line-height: 1.5;
    }

    /* Main title */
    .main-title {
        font-size: 32px;
        font-weight: 800;
        color: #1683e8;
        margin-bottom: 3px;
    }

    .main-subtitle {
        color: #aeb4c0;
        font-size: 14px;
        margin-bottom: 20px;
    }

    /* Result cards */
    .result-card {
        padding: 11px 14px;
        border-radius: 5px;
        margin-bottom: 10px;
        min-height: 45px;
        font-size: 14px;
        font-weight: 500;
    }

    .green-card {
        background-color: #123c2c;
        color: #52e89a;
    }

    .blue-card {
        background-color: #143453;
        color: #55a9ff;
    }

    .yellow-card {
        background-color: #414313;
        color: #e6e85b;
    }

    .red-card {
        background-color: #45252b;
        color: #ff8c9a;
    }

    /* Section headings */
    .section-title {
        font-size: 21px;
        font-weight: 700;
        margin-top: 18px;
        margin-bottom: 12px;
    }

    /* Status box */
    .status-online {
        background-color: #123c2c;
        color: #52e89a;
        padding: 15px;
        border-radius: 8px;
        font-weight: 600;
    }

    /* Project module */
    .module {
        color: #c7cad3;
        font-size: 12px;
        line-height: 1.8;
    }

    /* Hide Streamlit menu elements */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🏛️")
    st.markdown(
        '<div class="sidebar-title">SocialIQ</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'AI Complaint<br>Management System'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### Navigation")

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📋 Complaints",
            "📊 Analytics",
            "📈 Trend Forecasting",
            "⚠️ Anomaly Detection",
            "🤖 AI Predictions",
            "ℹ️ System Information"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### 📌 Quick Status")

    st.markdown(
        '<div class="status-online">🟢 FastAPI Backend<br><br>'
        'Backend Online</div>',
        unsafe_allow_html=True
    )

    st.markdown("")

    st.write("🤖 AI Modules")

    st.write("🗄️ PostgreSQL")

    st.write(
        f"📋 Complaints: {len(st.session_state.complaints)}"
    )

    st.divider()

    st.markdown("### 🔧 Project Modules")

    modules = [
        "1. Complaint Reason",
        "2. Department",
        "3. Sentiment",
        "4. Feedback Category",
        "5. Priority",
        "6. Emergency",
        "7. Harmful Content",
        "8. Trend Forecasting",
        "9. Anomaly Detection",
        "10. Government Action"
    ]

    for module in modules:
        st.markdown(
            f'<div class="module">{module}</div>',
            unsafe_allow_html=True
        )

    st.divider()

    st.caption("© 2026 SocialIQ AI Project")

# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    '🏛️ SocialIQ AI Complaint Management System'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'Artificial Intelligence Powered Citizen Complaint Classification Dashboard'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    # --------------------------------------------------------
    # TOP METRICS
    # --------------------------------------------------------

    total_complaints = len(st.session_state.complaints)

    urgent_count = sum(
        1 for x in st.session_state.complaints
        if x.get("priority") == "Urgent"
    )

    emergency_count = sum(
        1 for x in st.session_state.complaints
        if x.get("emergency") == "Emergency"
    )

    safe_count = sum(
        1 for x in st.session_state.complaints
        if x.get("harmful") == "Safe"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "📋 Total Complaints",
            total_complaints
        )

    with c2:
        st.metric(
            "⚠️ Urgent Complaints",
            urgent_count
        )

    with c3:
        st.metric(
            "🚨 Emergency Cases",
            emergency_count
        )

    with c4:
        st.metric(
            "🛡️ Safe Complaints",
            safe_count
        )

    st.markdown("")

    # --------------------------------------------------------
    # REGISTER NEW COMPLAINT
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📝 Register New Complaint</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 2])

    with col1:

        citizen_name = st.text_input(
            "Citizen Name",
            placeholder="Enter citizen name"
        )

    with col2:

        complaint = st.text_area(
            "Complaint",
            placeholder="Describe your complaint here...",
            height=100
        )

    if st.button(
        "🚀 Analyze Complaint",
        use_container_width=True
    ):

        if not citizen_name.strip():

            st.warning(
                "Please enter the citizen name."
            )

        elif not complaint.strip():

            st.warning(
                "Please enter the complaint."
            )

        else:

            payload = {
                "citizen_name": citizen_name,
                "complaint": complaint
            }

            with st.spinner(
                "🤖 AI is analyzing the complaint..."
            ):

                try:

                    response = requests.post(
                        API_URL,
                        json=payload,
                        timeout=120
                    )

                    if response.status_code == 200:

                        data = response.json()

                        prediction = data.get(
                            "prediction",
                            {}
                        )

                        complaint_id = data.get(
                            "complaint_id",
                            "N/A"
                        )

                        record = {
                            "Complaint ID": complaint_id,
                            "Citizen": citizen_name,
                            "Complaint": complaint,
                            "Department": prediction.get(
                                "department",
                                "N/A"
                            ),
                            "Priority": prediction.get(
                                "priority",
                                "N/A"
                            ),
                            "Sentiment": prediction.get(
                                "sentiment",
                                "N/A"
                            ),
                            "Feedback": prediction.get(
                                "feedback_category",
                                "N/A"
                            ),
                            "Emergency": prediction.get(
                                "emergency",
                                "N/A"
                            ),
                            "Harmful": prediction.get(
                                "harmful",
                                "N/A"
                            ),
                            "Trend": prediction.get(
                                "trend",
                                "N/A"
                            ),
                            "Anomaly": prediction.get(
                                "anomaly",
                                "N/A"
                            ),
                            "Government Action": prediction.get(
                                "government_action",
                                "N/A"
                            ),
                            "Time": datetime.now().strftime(
                                "%d-%m-%Y %H:%M:%S"
                            )
                        }

                        st.session_state.complaints.append(
                            record
                        )

                        st.session_state.last_prediction = record

                        st.success(
                            f"✅ Complaint #{complaint_id} "
                            "analyzed successfully."
                        )

                    else:

                        st.error(
                            f"❌ Backend returned HTTP "
                            f"{response.status_code}"
                        )

                        st.code(response.text)

                except requests.exceptions.Timeout:

                    st.error(
                        "⏳ Backend took too long to respond. "
                        "Render may be waking up. Please try again."
                    )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "❌ Could not connect to the "
                        "SocialIQ backend."
                    )

                except Exception as e:

                    st.error(
                        f"❌ Unexpected error: {str(e)}"
                    )

    # --------------------------------------------------------
    # AI PREDICTION RESULTS
    # --------------------------------------------------------

    if st.session_state.last_prediction:

        r = st.session_state.last_prediction

        st.divider()

        st.markdown(
            '<div class="section-title">'
            '🤖 AI Prediction Results'
            '</div>',
            unsafe_allow_html=True
        )

        # Row 1
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f'<div class="result-card green-card">'
                f'🏢 <b>Department:</b> '
                f'{r["Department"]}'
                f'</div>',
                unsafe_allow_html=True
            )

        with col2:
            emergency_class = (
                "red-card"
                if r["Emergency"] == "Emergency"
                else "green-card"
            )

            st.markdown(
                f'<div class="result-card {emergency_class}">'
                f'🚨 <b>Emergency:</b> '
                f'{r["Emergency"]}'
                f'</div>',
                unsafe_allow_html=True
            )

        # Row 2
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f'<div class="result-card blue-card">'
                f'⭐ <b>Priority:</b> '
                f'{r["Priority"]}'
                f'</div>',
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f'<div class="result-card blue-card">'
                f'📈 <b>Trend Forecast:</b> '
                f'{r["Trend"]}'
                f'</div>',
                unsafe_allow_html=True
            )

        # Row 3
        col1, col2 = st.columns(2)

        with col1:
            sentiment = r["Sentiment"]

            sentiment_class = (
                "red-card"
                if sentiment == "Negative"
                else "yellow-card"
                if sentiment == "Neutral"
                else "green-card"
            )

            st.markdown(
                f'<div class="result-card {sentiment_class}">'
                f'😊 <b>Sentiment:</b> '
                f'{sentiment}'
                f'</div>',
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f'<div class="result-card yellow-card">'
                f'⚠️ <b>Anomaly Detection:</b> '
                f'{r["Anomaly"]}'
                f'</div>',
                unsafe_allow_html=True
            )

        # Row 4
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f'<div class="result-card blue-card">'
                f'💬 <b>Feedback Category:</b> '
                f'{r["Feedback"]}'
                f'</div>',
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f'<div class="result-card green-card">'
                f'🏛️ <b>Government Action:</b> '
                f'{r["Government Action"]}'
                f'</div>',
                unsafe_allow_html=True
            )

        # Row 5
        col1, col2 = st.columns(2)

        with col1:

            harmful_class = (
                "red-card"
                if r["Harmful"] != "Safe"
                else "green-card"
            )

            st.markdown(
                f'<div class="result-card {harmful_class}">'
                f'🛡️ <b>Harmful Content:</b> '
                f'{r["Harmful"]}'
                f'</div>',
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                f'<div class="result-card blue-card">'
                f'🆔 <b>Complaint ID:</b> '
                f'{r["Complaint ID"]}'
                f'</div>',
                unsafe_allow_html=True
            )

    # --------------------------------------------------------
    # COMPLAINT HISTORY
    # --------------------------------------------------------

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '📊 Complaint History'
        '</div>',
        unsafe_allow_html=True
    )

    if st.session_state.complaints:

        history_df = pd.DataFrame(
            st.session_state.complaints
        )

        display_columns = [
            "Complaint ID",
            "Citizen",
            "Complaint",
            "Department",
            "Priority",
            "Sentiment",
            "Feedback",
            "Emergency",
            "Harmful",
            "Trend",
            "Anomaly",
            "Government Action",
            "Time"
        ]

        st.dataframe(
            history_df[display_columns],
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # DOWNLOAD CSV
        # ----------------------------------------------------

        csv_data = history_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download CSV Report",
            data=csv_data,
            file_name="socialiq_complaint_history.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:

        st.info(
            "No complaints have been analyzed yet."
        )

# ============================================================
# COMPLAINTS PAGE
# ============================================================

elif page == "📋 Complaints":

    st.header("📋 Government Complaints")

    st.write(
        "View all complaints analyzed by the SocialIQ AI system."
    )

    if st.session_state.complaints:

        df = pd.DataFrame(
            st.session_state.complaints
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No complaints available.")

# ============================================================
# ANALYTICS PAGE
# ============================================================

elif page == "📊 Analytics":

    st.header("📊 Complaint Analytics")

    if not st.session_state.complaints:

        st.info(
            "Analyze some complaints first to view analytics."
        )

    else:

        df = pd.DataFrame(
            st.session_state.complaints
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Complaints",
                len(df)
            )

        with col2:
            st.metric(
                "Urgent",
                len(
                    df[df["Priority"] == "Urgent"]
                )
            )

        with col3:
            st.metric(
                "Emergency",
                len(
                    df[df["Emergency"] == "Emergency"]
                )
            )

        st.subheader("Department Distribution")

        department_counts = (
            df["Department"]
            .value_counts()
        )

        st.bar_chart(
            department_counts
        )

        st.subheader("Sentiment Distribution")

        sentiment_counts = (
            df["Sentiment"]
            .value_counts()
        )

        st.bar_chart(
            sentiment_counts
        )

# ============================================================
# TREND FORECASTING
# ============================================================

elif page == "📈 Trend Forecasting":

    st.header("📈 Trend Forecasting")

    if st.session_state.complaints:

        for complaint in st.session_state.complaints:

            st.info(
                f'Complaint #{complaint["Complaint ID"]}: '
                f'{complaint["Trend"]}'
            )

    else:

        st.info(
            "No trend information available yet."
        )

# ============================================================
# ANOMALY DETECTION
# ============================================================

elif page == "⚠️ Anomaly Detection":

    st.header("⚠️ Anomaly Detection")

    if st.session_state.complaints:

        for complaint in st.session_state.complaints:

            st.warning(
                f'Complaint #{complaint["Complaint ID"]}: '
                f'{complaint["Anomaly"]}'
            )

    else:

        st.info(
            "No complaints available for anomaly analysis."
        )

# ============================================================
# AI PREDICTIONS
# ============================================================

elif page == "🤖 AI Predictions":

    st.header("🤖 AI Prediction Results")

    if st.session_state.complaints:

        df = pd.DataFrame(
            st.session_state.complaints
        )

        st.dataframe(
            df[
                [
                    "Complaint ID",
                    "Department",
                    "Priority",
                    "Sentiment",
                    "Feedback",
                    "Emergency",
                    "Harmful",
                    "Trend",
                    "Anomaly",
                    "Government Action"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No AI predictions available."
        )

# ============================================================
# SYSTEM INFORMATION
# ============================================================

elif page == "ℹ️ System Information":

    st.header("ℹ️ System Information")

    st.markdown(
        """
        ### 🏛️ SocialIQ AI Complaint Management System

        An AI-powered citizen complaint classification system.

        ### 🤖 AI Modules

        - Complaint Classification
        - Department Prediction
        - Sentiment Analysis
        - Feedback Classification
        - Priority Detection
        - Emergency Detection
        - Harmful Content Detection
        - Trend Forecasting
        - Anomaly Detection
        - Government Action Recommendation

        ### ⚙️ Technology Stack

        - Python
        - FastAPI
        - Machine Learning
        - Streamlit
        - PostgreSQL
        - Pandas
        - Scikit-learn

        ### 🔗 Backend

        SocialIQ FastAPI backend is hosted on Render.
        """
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SocialIQ AI Complaint Management System • "
    "FastAPI + Machine Learning + Streamlit"
)