from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER



import streamlit as st
import textwrap

# SAFE HTML RENDERER
# Dedent is important: indented HTML passed through Markdown can become a code block.
def render_html(content):
    html_content = textwrap.dedent(str(content)).strip()
    try:
        st.html(html_content)
    except AttributeError:
        st.markdown(html_content, unsafe_allow_html=True)
import pandas as pd
import json
import os
import html
from dotenv import load_dotenv
from google import genai
from google.genai import types
# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Resume Critic",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


if not API_KEY:
    st.error("❌ GEMINI_API_KEY not found.")
    st.info(
        "Create a .env file and add: "
        "GEMINI_API_KEY=YOUR_API_KEY"
    )
    st.stop()


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=API_KEY
)

MODEL_NAME = "gemini-3.6-flash"


# =========================================================
# SESSION STATE
# =========================================================

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []


# =========================================================
# PROFESSIONAL COLORFUL CSS
# =========================================================

render_html(
    """
<style>

/* =====================================================
   GLOBAL
   ===================================================== */

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(124,58,237,0.10),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(236,72,153,0.08),
            transparent 30%
        ),
        #080b14;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* =====================================================
   SIDEBAR
   ===================================================== */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #0d1122,
            #11162c,
            #080b15
        );

    border-right: 1px solid #252b48;
}

.sidebar-brand {
    padding: 20px;
    text-align: center;
}

.sidebar-logo {
    font-size: 55px;
}

.sidebar-title {
    font-size: 25px;
    font-weight: 900;

    background:
        linear-gradient(
            90deg,
            #8b5cf6,
            #ec4899,
            #38bdf8
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sidebar-subtitle {
    color: #8993b2;
    font-size: 13px;
}


/* =====================================================
   HEADER
   ===================================================== */

.dashboard-title {
    font-size: 43px;
    font-weight: 900;
    color: #ffffff;
}

.dashboard-subtitle {
    color: #929bb8;
    font-size: 16px;
    margin-bottom: 28px;
}


/* =====================================================
   HERO
   ===================================================== */

.hero-card {
    padding: 30px;
    border-radius: 24px;

    background:
        radial-gradient(
            circle at 90% 20%,
            rgba(139,92,246,0.35),
            transparent 30%
        ),
        radial-gradient(
            circle at 10% 90%,
            rgba(236,72,153,0.20),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #151a35,
            #0d1124
        );

    border: 1px solid #323960;

    box-shadow:
        0 20px 60px rgba(0,0,0,0.30);

    margin-bottom: 25px;
}

.hero-title {
    color: white;
    font-size: 30px;
    font-weight: 800;
}

.hero-text {
    color: #aab3cf;
    font-size: 15px;
    line-height: 1.7;
}


/* =====================================================
   METRIC CARDS
   ===================================================== */

.metric-card {
    min-height: 175px;
    padding: 22px;

    border-radius: 20px;

    border: 1px solid rgba(255,255,255,0.09);

    background:
        linear-gradient(
            145deg,
            rgba(29,35,68,0.95),
            rgba(12,16,34,0.98)
        );

    box-shadow:
        0 15px 40px rgba(0,0,0,0.25);

    position: relative;
    overflow: hidden;
}

.metric-purple {
    border-top: 3px solid #8b5cf6;
}

.metric-green {
    border-top: 3px solid #22c55e;
}

.metric-orange {
    border-top: 3px solid #f59e0b;
}

.metric-blue {
    border-top: 3px solid #38bdf8;
}

.metric-icon {
    font-size: 31px;
}

.metric-label {
    color: #929bb8;
    font-size: 13px;
    font-weight: 600;
    margin-top: 8px;
}

.metric-value {
    color: white;
    font-size: 31px;
    font-weight: 900;
    margin-top: 4px;
}

.metric-description {
    color: #6ee7b7;
    font-size: 12px;
}


/* =====================================================
   GENERAL CARD
   ===================================================== */

.dashboard-card {
    padding: 25px;
    border-radius: 20px;

    background:
        linear-gradient(
            145deg,
            #11172c,
            #0b1020
        );

    border: 1px solid #252c49;

    box-shadow:
        0 12px 35px rgba(0,0,0,0.20);

    margin-bottom: 20px;
}

.card-title {
    color: white;
    font-size: 21px;
    font-weight: 800;
}

.card-subtitle {
    color: #8993b2;
    font-size: 13px;
}


/* =====================================================
   SECTION TITLES
   ===================================================== */

.section-label {
    color: white;
    font-size: 26px;
    font-weight: 850;
    margin-top: 30px;
    margin-bottom: 18px;
}


/* =====================================================
   SKILL TAGS
   ===================================================== */

.skill-tag {
    display: inline-block;

    padding: 8px 13px;

    margin: 5px 4px;

    border-radius: 25px;

    color: #86efac;

    background: rgba(34,197,94,0.10);

    border: 1px solid rgba(34,197,94,0.35);

    font-size: 13px;
    font-weight: 700;
}

.missing-tag {
    display: inline-block;

    padding: 8px 13px;

    margin: 5px 4px;

    border-radius: 25px;

    color: #fca5a5;

    background: rgba(239,68,68,0.10);

    border: 1px solid rgba(239,68,68,0.35);

    font-size: 13px;
    font-weight: 700;
}


/* =====================================================
   ROAST
   ===================================================== */

.roast-box {
    padding: 30px;

    border-radius: 22px;

    background:
        radial-gradient(
            circle at 90% 10%,
            rgba(236,72,153,0.20),
            transparent 30%
        ),
        linear-gradient(
            145deg,
            #251329,
            #130d19
        );

    border: 1px solid rgba(236,72,153,0.35);

    border-left: 6px solid #ec4899;

    box-shadow:
        0 20px 55px rgba(236,72,153,0.08);
}

.roast-title {
    color: white;
    font-size: 23px;
    font-weight: 800;
}

.roast-text {
    color: #e5e7eb !important;
    font-size: 17px;
    line-height: 1.8;
}


/* =====================================================
   BULLET REWRITER
   ===================================================== */

.original-box {
    padding: 18px;
    border-radius: 15px;

    background: rgba(239,68,68,0.08);

    border: 1px solid rgba(239,68,68,0.25);
}

.improved-box {
    padding: 18px;
    border-radius: 15px;

    background: rgba(34,197,94,0.08);

    border: 1px solid rgba(34,197,94,0.25);
}

.original-label {
    color: #fca5a5;
    font-weight: 800;
}

.improved-label {
    color: #86efac;
    font-weight: 800;
}


/* =====================================================
   UPLOAD
   ===================================================== */

[data-testid="stFileUploader"] {
    background: #11172c;
    border-radius: 16px;
    padding: 10px;
    border: 1px solid #2a3151;
}


/* =====================================================
   BUTTON
   ===================================================== */

.stButton > button {
    border-radius: 13px;

    border: none;

    background:
        linear-gradient(
            90deg,
            #7c3aed,
            #ec4899
        );

    color: white;

    font-weight: 800;

    padding: 13px 25px;

    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 12px 35px rgba(139,92,246,0.35);
}


/* =====================================================
   PROGRESS
   ===================================================== */

.stProgress > div > div > div > div {
    background:
        linear-gradient(
            90deg,
            #7c3aed,
            #ec4899
        );
}


/* =====================================================
   FOOTER
   ===================================================== */

.footer {
    text-align: center;
    color: #59627f;
    padding: 35px;
    font-size: 13px;
}


.nav-link {
    display: block;
    text-decoration: none !important;
    color: #d9def0 !important;
    background: rgba(255,255,255,0.04);
    border: 1px solid #252c49;
    border-radius: 12px;
    padding: 11px 13px;
    margin: 7px 0;
    font-weight: 700;
    transition: all 0.2s ease;
}

.nav-link:hover {
    background: rgba(139,92,246,0.18);
    border-color: #8b5cf6;
    color: white !important;
}
</style>
""",
    
)




# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    render_html(
        """
        <div class="sidebar-brand">
            <div class="sidebar-logo">🤖</div>
            <div class="sidebar-title">AI Resume<br>Critic</div>
            <div class="sidebar-subtitle">Get Hired Faster.</div>
        </div>
        """,
        
    )

    st.divider()
    st.markdown("### 🧭 Navigation")

    render_html(
        """
        <a class="nav-link" href="#dashboard">🏠 Dashboard</a>
        <a class="nav-link" href="#resume-analysis">📄 Resume Analysis</a>
        <a class="nav-link" href="#job-matching">💼 Job Matching</a>
        <a class="nav-link" href="#recruiter-roast">🔥 Recruiter Roast</a>
        <a class="nav-link" href="#interview-prep">🎤 Interview Prep</a>
        """,
        
    )

    st.divider()
    st.markdown("### ⚙️ Analysis Settings")

    analysis_mode = st.selectbox(
        "Analysis Mode",
        ["Balanced", "ATS Focused", "Recruiter Focused"],
        index=0
    )

    experience_level = st.selectbox(
        "Experience Level",
        ["Student / Fresher", "Internship", "Entry Level", "Experienced"],
        index=0
    )

# HEADER
# =========================================================

render_html(
    """
<div class="hero-card"><div style="font-size:55px;">🤖📄🚀</div><div class="hero-title">AI Resume Critic</div><div class="hero-text">Analyze your resume against a real job description using Gemini AI. Discover your ATS score, missing skills, weaknesses, recruiter feedback and ways to improve your chances of getting shortlisted.</div></div>
""",
    
)

render_html(
    '<div class="dashboard-title">Resume Analyzer</div>',
    
)

render_html(
    '<div class="dashboard-subtitle">Upload your resume and let AI evaluate your application.</div>',
    
)
# =========================================================
# INPUT FORM
# =========================================================

render_html('<div id="resume-analysis"></div>')

st.markdown("### 📄 Resume Analysis")

with st.form("resume_analysis_form"):

    input_col1, input_col2 = st.columns(2)

    with input_col1:

        st.subheader("📄 Upload Resume")

        resume_file = st.file_uploader(
            "Upload your resume PDF",
            type=["pdf"],
            help="Upload a PDF version of your resume."
        )

        if resume_file:

            st.success(
                f"✅ {resume_file.name}"
            )

            st.caption(
                f"File size: "
                f"{resume_file.size / 1024:.1f} KB"
            )

    with input_col2:

        st.subheader("💼 Target Job Description")

        job_description = st.text_area(
            "Paste the complete job description",
            height=300,
            placeholder=(
                "Example:\n\n"
                "Software Engineer Intern\n\n"
                "Requirements:\n"
                "Python\n"
                "C++\n"
                "Data Structures and Algorithms\n"
                "SQL\n"
                "REST APIs\n"
                "Git\n"
                "Docker..."
            )
        )

        if job_description:
            st.caption(f"Job description: {len(job_description)} characters")

    st.divider()

    analyze = st.form_submit_button(
        "🔥 ANALYZE MY RESUME",
        use_container_width=True
    )


# =========================================================
# GEMINI ANALYSIS FUNCTION
# =========================================================

def analyze_resume(
    resume_file,
    job_description,
    analysis_mode,
    experience_level
):
    """Analyze the uploaded resume PDF with Gemini.

    The PDF is sent as inline bytes instead of using the Gemini Files API.
    This keeps the workflow to one API request and avoids creating a local
    temporary PDF file.
    """

    try:
        pdf_bytes = resume_file.getvalue()

        if not pdf_bytes:
            return {"error": "The uploaded PDF is empty."}

        if len(pdf_bytes) > 50 * 1024 * 1024:
            return {
                "error": "The PDF is larger than 50 MB. Please upload a smaller PDF."
            }

        prompt = f"""
You are an expert technical recruiter, ATS specialist, resume reviewer,
and career coach.

Analyze the uploaded resume PDF against the target job description.

CURRENT YEAR: 2026

Candidate experience level:
{experience_level}

Analysis mode:
{analysis_mode}

TARGET JOB DESCRIPTION:
{job_description}

========================
ANALYSIS RULES
========================

1. Read the entire resume carefully.
2. Read the entire job description carefully.
3. NEVER invent information.
4. NEVER assume the candidate has a skill, internship, job, certification,
   degree, achievement, or experience that is not present in the resume.
5. A project is NOT an internship.
6. A project is NOT employment.
7. Do not change dates found in the resume.
8. Use 2026 as the current year.
9. If a date looks unusual, flag it rather than changing it.
10. If a skill is not demonstrated in the resume, say "not demonstrated".
11. Compare the candidate specifically against this job description.
12. Prioritize skills explicitly required by the job.
13. Do not reward unrelated technologies.
14. Do not give artificially high scores.
15. Do not give artificially low scores.
16. The recruiter roast should be humorous, direct, and constructive.
17. The roast must criticize the resume, NOT the candidate personally.
18. Never invent timelines.
19. Do not invent numbers or achievements when rewriting bullet points.
20. Preserve the original meaning of every rewritten bullet.
21. Interview questions should be based on the resume and target job.
22. If information is unavailable, say so instead of guessing.

========================
SCORING
========================

ATS SCORE:
90-100 = Excellent
80-89 = Very strong
70-79 = Good
60-69 = Moderate
50-59 = Significant gaps
Below 50 = Poor

JOB MATCH SCORE:
90-100 = Excellent
80-89 = Strong
70-79 = Good
60-69 = Partial
50-59 = Weak
Below 50 = Poor

========================
OUTPUT
========================

Return ONLY valid JSON using exactly this structure:

{{
    "ats_score": 0,
    "job_match_score": 0,
    "resume_strength": "Excellent",
    "matching_skills": [
        {{"skill": "Python", "match": "Strong"}}
    ],
    "missing_skills": [
        {{"skill": "Docker", "priority": "High"}}
    ],
    "strengths": [
        "Specific strength from resume"
    ],
    "weaknesses": [
        "Specific weakness from resume"
    ],
    "recruiter_roast": "Humorous but constructive recruiter critique",
    "improvements": [
        "Specific improvement"
    ],
    "bullet_rewrites": [
        {{
            "original": "Actual resume bullet",
            "improved": "Improved version"
        }}
    ],
    "interview_questions": [
        "Relevant interview question"
    ]
}}

Before returning the response verify:
- No invented experience
- No invented dates
- No invented numbers
- Projects are not called internships
- Missing skills actually relate to the job
- Scores are realistic
- Roast is based on actual resume problems
- JSON is valid
"""

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                types.Part.from_bytes(
                    data=pdf_bytes,
                    mime_type="application/pdf"
                ),
                prompt
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        if not response or not response.text:
            return {"error": "Gemini returned an empty response."}

        try:
            result = json.loads(response.text)
        except json.JSONDecodeError as error:
            return {
                "error": f"Gemini returned invalid JSON: {error}"
            }

        # Basic validation so the UI never crashes because Gemini omitted a field.
        result.setdefault("ats_score", 0)
        result.setdefault("job_match_score", 0)
        result.setdefault("resume_strength", "Unknown")
        result.setdefault("matching_skills", [])
        result.setdefault("missing_skills", [])
        result.setdefault("strengths", [])
        result.setdefault("weaknesses", [])
        result.setdefault("recruiter_roast", "No recruiter roast generated.")
        result.setdefault("improvements", [])
        result.setdefault("bullet_rewrites", [])
        result.setdefault("interview_questions", [])

        return result

    except Exception as error:
        message = str(error)

        if "10013" in message or "socket" in message.lower():
            return {
                "error": (
                    "Windows blocked the network connection to Gemini (WinError 10013). "
                    "The Python code is running, but Windows/firewall/VPN/network settings "
                    "are preventing the Gemini API connection."
                )
            }

        return {"error": message}


# =========================================================
# PDF REPORT GENERATOR
# =========================================================

def create_pdf_report(result, ats, match, strength):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "PDFTitle",
        parent=styles["Title"],
        fontSize=24,
        leading=28,
        alignment=TA_CENTER,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "PDFSubtitle",
        parent=styles["BodyText"],
        fontSize=11,
        leading=15,
        alignment=TA_CENTER,
        spaceAfter=18
    )

    heading_style = ParagraphStyle(
        "PDFHeading",
        parent=styles["Heading2"],
        fontSize=15,
        leading=18,
        spaceBefore=14,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        "PDFBody",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14,
        spaceAfter=5
    )

    story = []

    story.append(Paragraph("AI Resume Critic", title_style))
    story.append(Paragraph("AI-Powered Resume Analysis Report", subtitle_style))

    story.append(Paragraph("Resume Dashboard", heading_style))

    score_data = [
        ["Metric", "Result"],
        ["ATS Compatibility", f"{ats}/100"],
        ["Job Match", f"{match}%"],
        ["Resume Strength", str(strength)],
    ]

    score_table = Table(score_data, colWidths=[250, 180])
    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4f46e5")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(score_table)

    story.append(Paragraph("Matching Skills", heading_style))
    matching = result.get("matching_skills", [])
    if matching:
        for skill in matching:
            story.append(Paragraph(
                f"✓ {skill.get('skill', '')} — {skill.get('match', '')}",
                body_style
            ))
    else:
        story.append(Paragraph("No matching skills identified.", body_style))

    story.append(Paragraph("Missing Skills", heading_style))
    missing = result.get("missing_skills", [])
    if missing:
        for skill in missing:
            story.append(Paragraph(
                f"✕ {skill.get('skill', '')} — {skill.get('priority', '')}",
                body_style
            ))
    else:
        story.append(Paragraph("No major missing skills identified.", body_style))

    story.append(Paragraph("Strengths", heading_style))
    for item in result.get("strengths", []):
        story.append(Paragraph(f"✓ {html.escape(str(item))}", body_style))

    story.append(Paragraph("Weaknesses", heading_style))
    for item in result.get("weaknesses", []):
        story.append(Paragraph(f"• {html.escape(str(item))}", body_style))

    story.append(Paragraph("Recruiter Roast", heading_style))
    story.append(Paragraph(
        html.escape(str(result.get("recruiter_roast", "No recruiter roast generated."))),
        body_style
    ))

    story.append(Paragraph("Recommended Improvements", heading_style))
    for number, item in enumerate(result.get("improvements", []), start=1):
        story.append(Paragraph(f"{number}. {html.escape(str(item))}", body_style))

    story.append(Paragraph("AI Bullet Rewriter", heading_style))
    for number, bullet in enumerate(result.get("bullet_rewrites", []), start=1):
        story.append(Paragraph(f"<b>Bullet {number}</b>", body_style))
        story.append(Paragraph(
            f"<b>Original:</b> {html.escape(str(bullet.get('original', '')))}",
            body_style
        ))
        story.append(Paragraph(
            f"<b>Improved:</b> {html.escape(str(bullet.get('improved', '')))}",
            body_style
        ))

    story.append(Paragraph("AI Interview Preparation", heading_style))
    for number, question in enumerate(result.get("interview_questions", []), start=1):
        story.append(Paragraph(f"{number}. {html.escape(str(question))}", body_style))

    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "Generated by AI Resume Critic · Powered by Gemini",
        ParagraphStyle(
            "PDFFooter",
            parent=body_style,
            alignment=TA_CENTER,
            fontSize=9
        )
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer


# =========================================================
# RUN ANALYSIS
# =========================================================

if analyze:

    if resume_file is None:

        st.error(
            "❌ Please upload your resume PDF."
        )

    elif not job_description.strip():

        st.error(
            "❌ Please paste the target job description."
        )

    else:

        with st.spinner(
            "🤖 Gemini is reading your resume..."
        ):

            result = analyze_resume(
                resume_file,
                job_description,
                analysis_mode,
                experience_level
            )

        if "error" in result:

            st.error(
                f"❌ Analysis failed: {result['error']}"
            )

        else:

            st.session_state.analysis_done = True

            st.session_state.analysis_result = result

            st.session_state.analysis_history.append(
                {
                    "ATS Score": result.get("ats_score", 0),
                    "Job Match": result.get("job_match_score", 0),
                    "Missing Skills":
                        len(result.get("missing_skills", [])),
                    "Mode": analysis_mode
                }
            )

            st.success(
                "✅ Resume analysis completed!"
            )


# =========================================================
# RESULTS
# =========================================================

render_html('<div id="dashboard"></div>')

result = st.session_state.get("analysis_result")

if not result:
    st.stop()

try:
    ats = max(0, min(100, int(result.get("ats_score", 0))))
except (TypeError, ValueError):
    ats = 0

try:
    match = max(0, min(100, int(result.get("job_match_score", 0))))
except (TypeError, ValueError):
    match = 0
strength = result.get("resume_strength", "Unknown")


# DASHBOARD HEADER
    # =====================================================

st.divider()

render_html(
        '<div class="section-label">'
        '📊 Resume Dashboard'
        '</div>',
        
    )


# =====================================================
# METRIC CARDS
    # =====================================================

c1, c2, c3, c4 = st.columns(4)


with c1:

        render_html(f"""
<div class="metric-card metric-purple">
    <div class="metric-icon">🎯</div>
    <div class="metric-label">ATS SCORE</div>
    <div class="metric-value">{ats}/100</div>
</div>
""")
# =====================================================
# PERFORMANCE + AI ASSISTANT
    # =====================================================
render_html(
        '<div class="section-label">'
        '🤖 AI Analysis'
        '</div>',
        
    )

col1, col2 = st.columns(
        [1.4, 1]
    )

with col1:

        render_html(f"""
<div class="dashboard-card">

    <div class="card-title">
        📈 Resume Performance
    </div>

    <div class="card-subtitle">
        Your resume against the target role
    </div>

    <br>

    <b style="color:#d8def0;">
        ATS Compatibility – {ats}/100
    </b>

    <div style="
        height:12px;
        background:#202641;
        border-radius:10px;
        margin-top:8px;
        margin-bottom:22px;
    ">
        <div style="
            width:{ats}%;
            height:100%;
            background:linear-gradient(
                90deg,
                #7c3aed,
                #06b6d4
            );
            border-radius:10px;
        "></div>
    </div>

</div>
""")

with col2:

        render_html(f"""
<div class="dashboard-card">

    <div style="
        font-size:55px;
        text-align:center;
    ">
        🤖🚀
    </div>

    <div class="card-title">
        AI Career Assistant
    </div>

    <p class="card-subtitle" style="line-height:1.7;">
        Gemini has compared your resume with the target job
        and identified your strongest opportunities for
        improvement.
    </p>

    <div style="
        color:#c084fc;
        font-weight:700;
        margin-top:15px;
    ">
        🚀 Keep improving and keep applying!
    </div>

</div>
""")

# =====================================================
# SKILLS
    # =====================================================

# =========================================================



    # =====================================================
   # =========================================================
# SKILLS INTELLIGENCE
# =========================================================
# =========================================================
# SKILLS INTELLIGENCE
# =========================================================

render_html('<div id="job-matching"></div>')
st.markdown("### 🧠 Skills Intelligence")

skill_col1, skill_col2 = st.columns(2)

# ---------------- MATCHING ----------------

with skill_col1:

    render_html("""
    <div class="dashboard-card">
        <div class="card-title">
            🟢 Matching Skills
        </div>
        <div class="card-subtitle">
            Skills found in your resume
        </div>
    </div>
    """)

    for skill in result.get("matching_skills", []):

        name = html.escape(
            str(skill.get("skill", ""))
        )

        level = html.escape(
            str(skill.get("match", "Good"))
        )

        render_html(
            f"""
            <div class="skill-tag">
                ✓ {name} · {level}
            </div>
            """,
            
        )


# ---------------- MISSING ----------------

with skill_col2:

    render_html("""
    <div class="dashboard-card">
        <div class="card-title">
            🔴 Missing Skills
        </div>
        <div class="card-subtitle">
            Important skills not demonstrated
        </div>
    </div>
    """)

    for skill in result.get("missing_skills", []):

        name = html.escape(
            str(skill.get("skill", ""))
        )

        priority = html.escape(
            str(skill.get("priority", "Medium"))
        )

        render_html(
            f"""
            <div class="missing-tag">
                ✕ {name} · {priority}
            </div>
            """,
            
        )


# =========================================================
# RECRUITER ROAST
# =========================================================

render_html('<div id="recruiter-roast"></div>')
st.markdown("### 🔥 Recruiter Roast")

roast = result.get(
    "recruiter_roast",
    "No recruiter roast generated."
)

render_html(
    f"""
    <div class="roast-box">

        <div style="font-size:50px;">
            🎙️🔥
        </div>

        <div class="roast-title">
            The recruiter has spoken.
        </div>

        <p class="roast-text">
            {html.escape(str(roast))}
        </p>

        <div style="
            color:#c084fc;
            font-weight:700;
            margin-top:15px;
        ">
            💡 Take the criticism. Improve the resume.
        </div>

    </div>
    """,
    
)


# =========================================================
# RECOMMENDED IMPROVEMENTS
# =========================================================

st.markdown("### 🚀 Recommended Improvements")

for number, item in enumerate(
    result.get("improvements", []),
    start=1
):

    render_html(
        f"""
        <div class="dashboard-card">

            <span style="
                color:#a78bfa;
                font-weight:900;
                font-size:20px;
            ">
                {number}
            </span>

            <span style="
                color:#d9def0;
                margin-left:12px;
            ">
                {html.escape(str(item))}
            </span>

        </div>
        """,
        
    )


# =========================================================
# AI BULLET REWRITER
# =========================================================

st.markdown("### ✍️ AI Bullet Rewriter")

bullets = result.get(
    "bullet_rewrites",
    []
)

if bullets:

    for number, bullet in enumerate(
        bullets,
        start=1
    ):

        original = html.escape(
            str(
                bullet.get(
                    "original",
                    ""
                )
            )
        )

        improved = html.escape(
            str(
                bullet.get(
                    "improved",
                    ""
                )
            )
        )

        with st.expander(
            f"📝 Resume Bullet {number}"
        ):

            c1, c2 = st.columns(2)

            with c1:

                render_html(
                    f"""
                    <div class="original-box">

                        <div class="original-label">
                            ❌ ORIGINAL
                        </div>

                        <p style="
                            color:#e5e7eb;
                            line-height:1.6;
                        ">
                            {original}
                        </p>

                    </div>
                    """,
                    
                )

            with c2:

                render_html(
                    f"""
                    <div class="improved-box">

                        <div class="improved-label">
                            ✨ AI IMPROVED
                        </div>

                        <p style="
                            color:#e5e7eb;
                            line-height:1.6;
                        ">
                            {improved}
                        </p>

                    </div>
                    """,
                    
                )

else:

    st.info("No bullet rewrites generated.")


# =========================================================
# AI INTERVIEW PREPARATION
# =========================================================

render_html('<div id="interview-prep"></div>')
st.markdown("### 🎤 AI Interview Preparation")

questions = result.get(
    "interview_questions",
    []
)

for number, question in enumerate(
    questions,
    start=1
):

    with st.expander(
        f"❓ Question {number}"
    ):

        st.write(question)

        st.text_area(
            "Your answer",
            key=f"interview_answer_{number}",
            height=120,
            placeholder="Write your answer here..."
        )


# =========================================================
# DETAILED SKILL DATA
# =========================================================

st.markdown("### 📋 Detailed Skill Data")

matching_df = pd.DataFrame(
    result.get(
        "matching_skills",
        []
    )
)

missing_df = pd.DataFrame(
    result.get(
        "missing_skills",
        []
    )
)

table_col1, table_col2 = st.columns(2)

with table_col1:

    st.markdown("### 🟢 Matching")

    if not matching_df.empty:

        st.dataframe(
            matching_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No matching skill data.")


with table_col2:

    st.markdown("### 🔴 Missing")

    if not missing_df.empty:

        st.dataframe(
            missing_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No missing skill data.")


# =========================================================
# PDF EXPORT — LAST SECTION
# =========================================================

st.markdown("### 📥 Export Your Analysis")

pdf_file = create_pdf_report(
    result,
    ats,
    match,
    strength
)

st.download_button(
    label="📥 DOWNLOAD PDF REPORT",
    data=pdf_file,
    file_name="AI_Resume_Critic_Report.pdf",
    mime="application/pdf",
    use_container_width=True
)


# =========================================================
# FOOTER
# =========================================================

render_html(
    """
    <div class="footer">
        🤖 AI Resume Critic · Powered by Gemini
        <br><br>
        Analyze smarter · Improve faster · Get hired
    </div>
    """,
    
)
