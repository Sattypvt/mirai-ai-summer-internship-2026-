import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Life-OS",
    page_icon="⚡",
    layout="wide"
)


# ---------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

   .life-title {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1px;
    margin: 0;
    padding-top: 8px;
    line-height: 1.3;
   }
    

    .life-subtitle {
        color: #888;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .system-online {
    display: inline-block;
    padding: 7px 14px;
    border: 1px solid #2ecc71;
    border-radius: 20px;
    color: #2ecc71;
    font-size: 12px;
    font-weight: 600;
    line-height: 1.2;
    margin-top: 12px;
    white-space: nowrap;
}

    .coach-box {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-top: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# DATA
# ---------------------------------------------------------

@st.cache_data
def load_data():
    data = pd.read_csv("screentime.csv")
    data["Date"] = pd.to_datetime(data["Date"])
    return data


df = load_data()


# ---------------------------------------------------------
# GEMINI CLIENT
# ---------------------------------------------------------

def get_api_key():
    """
    First check Streamlit secrets for deployment.
    Then fall back to .env for local development.
    """

    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return os.getenv("GEMINI_API_KEY")


@st.cache_resource
def get_gemini_client(api_key):
    return genai.Client(api_key=api_key)


# ---------------------------------------------------------
# DATA BRIDGE
# ---------------------------------------------------------

def prepare_day_summary(day_data):
    category_summary = (
        day_data
        .groupby("Category")["Minutes_Used"]
        .sum()
        .sort_values(ascending=False)
    )

    app_summary = (
        day_data
        .groupby("App_Name")["Minutes_Used"]
        .sum()
        .sort_values(ascending=False)
    )

    summary = f"""
CATEGORY USAGE
{category_summary.to_string()}

APP USAGE
{app_summary.to_string()}

TOTAL SCREEN TIME
{day_data["Minutes_Used"].sum()} minutes
"""

    return summary


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

header_left, header_right = st.columns([5, 1])

with header_left:
    st.markdown(
        '<p class="life-title">LIFE-OS ⚡</p>',
        unsafe_allow_html=True
    )

   
    

with header_right:
    st.markdown(
        """
        <div style="text-align: right; padding-top: 10px; padding-right: 10px;">
            <span class="system-online">● SYSTEM ONLINE</span>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.title("⚙️ Control Center")

available_dates = sorted(df["Date"].dt.date.unique(), reverse=True)

# Read shared date from URL
shared_date = st.query_params.get("date")

default_index = 0

if shared_date:
    try:
        shared_date = pd.to_datetime(shared_date).date()

        if shared_date in available_dates:
            default_index = available_dates.index(shared_date)

    except Exception:
        pass

selected_date = st.sidebar.selectbox(
    "Select Day",
    available_dates,
    index=default_index
)

daily_goal_hours = st.sidebar.slider(
    "Daily Screen-Time Goal",
    min_value=1.0,
    max_value=10.0,
    value=5.0,
    step=0.5
)

daily_goal_minutes = daily_goal_hours * 60


# ---------------------------------------------------------
# FILTER SELECTED DAY
# ---------------------------------------------------------

day_data = df[df["Date"].dt.date == selected_date]

total_minutes = int(day_data["Minutes_Used"].sum())

hours = total_minutes // 60
minutes = total_minutes % 60


# ---------------------------------------------------------
# MOST USED APP
# ---------------------------------------------------------

app_usage = (
    day_data
    .groupby("App_Name")["Minutes_Used"]
    .sum()
    .sort_values(ascending=False)
)

most_used_app = app_usage.index[0]


# ---------------------------------------------------------
# GOAL DIFFERENCE
# ---------------------------------------------------------

goal_difference = total_minutes - daily_goal_minutes

if goal_difference > 0:
    goal_text = f"+{int(goal_difference)} min"
else:
    goal_text = f"{int(goal_difference)} min"


# ---------------------------------------------------------
# SHAREABLE ACCOUNTABILITY LINK
# ---------------------------------------------------------

st.query_params["date"] = str(selected_date)
st.query_params["screen_time"] = total_minutes


# ---------------------------------------------------------
# KPI SECTION
# ---------------------------------------------------------

st.markdown("### 📊 Today's Command Center")

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric(
        "Total Screen Time",
        f"{hours}h {minutes}m"
    )

with kpi2:
    st.metric(
        "Most Used App",
        most_used_app
    )

with kpi3:
    st.metric(
        "Daily Goal",
        f"{daily_goal_hours:g} hours",
        delta=goal_text,
        delta_color="inverse"
    )


st.divider()


# ---------------------------------------------------------
# CHARTS
# ---------------------------------------------------------

left_chart, right_chart = st.columns(2)


with left_chart:

    st.subheader("📈 14-Day Screen-Time Trend")

    daily_trend = (
        df.groupby("Date")["Minutes_Used"]
        .sum()
        .sort_index()
    )

    st.line_chart(daily_trend)


with right_chart:

    st.subheader("📱 Today's Category Breakdown")

    category_data = (
        day_data.groupby("Category")["Minutes_Used"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_data)


st.divider()


# ---------------------------------------------------------
# ACCOUNTABILITY SECTION
# ---------------------------------------------------------

st.subheader("🔗 Accountability Mode")

st.write(
    "The selected date and total screen time are stored "
    "inside the page URL using `st.query_params`."
)

st.code(
    f"date={selected_date}&screen_time={total_minutes}",
    language=None
)

st.caption(
    "Copy the browser URL and send it to an accountability "
    "partner to share your selected day's stats."
)


# ---------------------------------------------------------
# AI COACH
# ---------------------------------------------------------

st.divider()

st.subheader("🧠 AI Life Coach")

day_summary = prepare_day_summary(day_data)

api_key = get_api_key()


if not api_key:

    st.warning(
        "Gemini API key not configured. "
        "Add GEMINI_API_KEY to your .env file locally "
        "or Streamlit Secrets after deployment."
    )

else:

    prompt = f"""
You are Life-OS, a brutal-but-fair digital wellbeing,
productivity and lifestyle coach.

Analyze the user's screen-time behavior.

SCREEN-TIME DATA:

{day_summary}

USER'S DAILY SCREEN-TIME GOAL:
{daily_goal_minutes:.0f} minutes

Your job is NOT to simply tell the user to use their phone less.

Analyze:

1. Which apps and categories are consuming the most time.
2. Whether the screen usage appears productive or distracting.
3. Which behavior is the biggest problem.
4. What time could realistically be reclaimed.

For distracting screen time, suggest specific physical,
real-world replacements.

Examples include:

- walking
- gym or home exercise
- stretching
- cooking or meal preparation
- reading a physical book
- cleaning the room
- outdoor sports
- meeting friends or family
- journaling
- meditation
- sleeping earlier

Do NOT shame or insult the user.

Be direct, specific, practical and slightly tough.

Return the response in Markdown with exactly these sections:

### Reality Check

### What's Working

### Biggest Time Leak

### Real-World Replacement

### Tomorrow's Challenge

Keep the complete response concise.
"""


    if st.button(
        "⚡ Analyze My Day",
        type="primary",
        use_container_width=True
    ):

        try:

            client = get_gemini_client(api_key)

            with st.spinner(
                "Life-OS is analyzing your digital behavior..."
            ):

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )

            if total_minutes > daily_goal_minutes * 1.25:

                st.warning(
                    "⚠️ High screen-time day detected."
                )

            elif total_minutes > daily_goal_minutes:

                st.warning(
                    "You're above your screen-time goal today."
                )

            else:

                st.info(
                    "✅ You're within your daily screen-time goal."
                )

            st.markdown(
                '<div class="coach-box">',
                unsafe_allow_html=True
            )

            st.markdown(response.text)

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

        except Exception as error:

            st.error(
                "Gemini couldn't generate the analysis."
            )

            st.exception(error)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "LIFE-OS • AI-Powered Digital Wellbeing Dashboard • 2026"
)