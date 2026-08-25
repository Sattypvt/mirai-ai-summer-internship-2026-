

# 🤖 MirAI AI Summer Internship 2026

```text
╔══════════════════════════════════════════════════════════════╗
║              MIRAI AI SUMMER INTERNSHIP 2026                ║
║                                                              ║
║   Python • Streamlit • Gemini API • Generative AI • GitHub  ║
╚══════════════════════════════════════════════════════════════╝
👨‍💻 Student

Satyander Bhagat

Program: MirAI School of Technology — AI Summer Internship 2026
Degree: B.Tech Computer Science & Engineering

📌 About This Repository

This repository contains the assignments and final capstone project completed during the MirAI School of Technology AI Summer Internship 2026.

The internship focused on practical development using Python, Streamlit, Generative AI, Google Gemini API, prompt engineering, Git, GitHub, data processing, and cloud deployment.

The repository demonstrates the progression from individual programming assignments to a complete AI-powered web application.

📂 Repository Structure
mirai-ai-summer-internship-2026-/
│
├── 📁 Assignment 1/
├── 📁 Assignment 2/
├── 📁 Assignment 3/
├── 📁 Assignment 4/
├── 📁 Assignment 5/
├── 📁 Assignment 6/
├── 📁 Assignment 7/
│
├── 📁 Final-Capstone-Project/
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
│
├── .gitignore
├── requirements.txt
└── README.md
🚀 Final Capstone Project
🤖 AI Resume Critic — Tech-Roast
Problem Statement #17

The AI Resume Critic — Tech-Roast is an AI-powered resume analysis application.

Users provide their resume and a target job description. Google Gemini analyzes the resume from the perspective of a strict technical recruiter and provides detailed, actionable feedback.

🌐 Live Application

https://airesumecritic.streamlit.app/

🎯 Problem Statement

The application addresses the problem of understanding how effectively a resume matches a specific job description.

Instead of providing generic resume advice, the application compares the candidate's resume with the target role and identifies:

Missing technical keywords
Weak resume bullet points
Skill gaps
Job-description alignment
Areas for improvement
Recruiter-style feedback
✨ Key Features
📄 Resume Analysis

Analyzes the candidate's resume and identifies relevant skills, experience, and areas that need improvement.

🎯 Job Description Matching

Compares the resume with the target job description to determine how well the candidate matches the desired role.

🔑 Missing Keyword Detection

Identifies important skills and keywords from the target job description that are missing from the resume.

📝 Weak Bullet Point Detection

Identifies vague or weak resume statements and provides suggestions for stronger alternatives.

📊 Resume Scoring

Provides an overall evaluation of the candidate's resume.

👨‍💼 Recruiter-Style Feedback

Gemini is instructed to act as a strict technical recruiter instead of a generic chatbot.

💡 Improvement Suggestions

Provides actionable recommendations to improve the resume for the selected position.

📥 PDF Report

Generates a downloadable PDF report containing the resume analysis and recommendations.

🧠 System Architecture
                    ┌──────────────┐
                    │     USER     │
                    └──────┬───────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   Streamlit UI      │
                └──────────┬──────────┘
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
          ┌─────────────┐     ┌────────────────┐
          │   Resume    │     │ Job Description│
          └──────┬──────┘     └───────┬────────┘
                 │                    │
                 └──────────┬─────────┘
                            ▼
                 ┌────────────────────┐
                 │  Prompt Builder    │
                 └──────────┬─────────┘
                            │
                            ▼
                 ┌────────────────────┐
                 │   Google Gemini    │
                 │       API          │
                 └──────────┬─────────┘
                            │
                            ▼
                 ┌────────────────────┐
                 │ AI Resume Analysis │
                 └──────────┬─────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
          ┌────────┐   ┌──────────┐   ┌───────────┐
          │ Score  │   │ Keywords │   │ Feedback  │
          └────┬───┘   └─────┬────┘   └─────┬─────┘
               │             │              │
               └─────────────┼──────────────┘
                             ▼
                  ┌────────────────────┐
                  │ Streamlit Dashboard│
                  └──────────┬─────────┘
                             │
                             ▼
                      ┌─────────────┐
                      │ PDF Report  │
                      └─────────────┘
🔄 Application Data Flow
USER
 │
 ├── Resume
 │
 └── Target Job Description
          │
          ▼
   Streamlit Interface
          │
          ▼
    Resume Processing
          │
          ▼
    Prompt Construction
          │
          ▼
     Google Gemini API
          │
          ▼
    AI Resume Analysis
          │
     ┌────┼────┬─────────────┐
     ▼    ▼    ▼             ▼
   Score Keywords Weak Points Recommendations
     │    │    │             │
     └────┴────┴─────────────┘
                  │
                  ▼
        Streamlit Dashboard
                  │
                  ▼
             PDF Report
🏗️ Technical Design
1. User Input Layer

The application accepts two primary inputs:

Candidate Resume
Target Job Description

These inputs provide the context required for personalized resume evaluation.

2. Resume Processing Layer

The application receives and prepares the resume information for analysis.

The resume information is combined with the target job description before being passed to the AI analysis stage.

3. Prompt Engineering Layer

A dynamic prompt is constructed using:

Resume
+
Target Job Description
+
Recruiter Evaluation Criteria

The prompt instructs Gemini to behave as a strict technical recruiter.

The AI evaluates:

Technical skills
Job-description alignment
Missing keywords
Weak bullet points
Relevant experience
Skill gaps
Improvement opportunities
4. Gemini API Layer

The processed information is sent to the Google Gemini API.

Gemini performs the AI reasoning and generates the resume evaluation.

The API is accessed securely using the GEMINI_API_KEY stored in Streamlit Secrets.

The API key is not stored in the public GitHub repository.

5. Analysis Layer

The AI-generated response is presented through the Streamlit interface.

The analysis can contain:

Overall assessment
Resume score
Missing keywords
Weak bullet points
Strengths
Recommendations
Recruiter feedback
6. Report Generation Layer

The application uses ReportLab to generate a downloadable PDF report.

The generated report contains the results of the AI-powered resume evaluation.

🔌 API Integration Strategy

The application integrates the Google Gemini API as its primary AI engine.

The integration follows this flow:

Streamlit Interface
        ↓
Python Application
        ↓
Gemini API Client
        ↓
Google Gemini Model
        ↓
AI Generated Analysis
        ↓
Streamlit Dashboard

The Gemini API key is securely stored using Streamlit Secrets.

Sensitive credentials are not committed to GitHub.

🧠 Prompt Engineering Strategy

The application uses a specialized recruiter-oriented prompt.

Gemini is provided with dynamic context consisting of:

Candidate Resume
+
Target Job Description
+
Recruiter Instructions

The AI is instructed to evaluate the candidate specifically for the selected role.

The prompt focuses on:

Resume relevance
Technical skills
Missing keywords
Weak bullet points
Experience alignment
Skill gaps
Actionable improvements
Overall recruiter assessment

This approach makes the AI act as a specialized resume evaluator rather than a generic chatbot.

🧩 Logic Modules
1. User Interface Module

Handles:

Resume input
Job description input
User interactions
Buttons
Results presentation
2. Resume Processing Module

Handles the preparation of resume information for AI analysis.

3. Prompt Engineering Module

Constructs the recruiter-focused prompt using the resume and target job description.

4. Gemini Integration Module

Communicates with the Google Gemini API and receives the generated evaluation.

5. Results Module

Displays the AI-generated analysis and recommendations.

6. PDF Generation Module

Uses ReportLab to generate the downloadable resume analysis report.

🛠️ Technology Stack
Technology	Purpose
Python	Application development
Streamlit	Web application and UI
Google Gemini API	Generative AI analysis
Pandas	Data processing
ReportLab	PDF generation
Python-dotenv	Environment configuration
Git	Version control
GitHub	Source code management
Streamlit Community Cloud	Cloud deployment
📁 Final Capstone Structure
Final-Capstone-Project/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
🔐 Security & API Key Management

The Gemini API key is never hard-coded into the source code or committed to GitHub.

Local Development

Create a .env file:

GEMINI_API_KEY=YOUR_API_KEY
Streamlit Cloud

The API key is stored securely through:

Streamlit
    ↓
App Settings
    ↓
Secrets

Example:

GEMINI_API_KEY = "YOUR_API_KEY"

⚠️ Never expose or commit a real API key to GitHub.

⚙️ Local Installation
1. Clone the repository
git clone https://github.com/Sattypvt/mirai-ai-summer-internship-2026-.git
2. Enter the repository
cd mirai-ai-summer-internship-2026-
3. Enter the capstone project
cd Final-Capstone-Project
4. Install dependencies
pip install -r requirements.txt
5. Configure the Gemini API key

Create a .env file:

GEMINI_API_KEY=YOUR_API_KEY
6. Run the application
streamlit run app.py
📦 Dependencies

The final capstone uses:

streamlit
pandas
google-genai
python-dotenv
pydantic
reportlab

Dependencies are maintained in:

Final-Capstone-Project/requirements.txt
☁️ Deployment

The application is deployed using Streamlit Community Cloud.

Deployment Architecture
GitHub Repository
       │
       ▼
Streamlit Community Cloud
       │
       ▼
requirements.txt
       │
       ▼
Python Environment
       │
       ▼
Streamlit Application
       │
       ▼
Google Gemini API
       │
       ▼
AI Resume Analysis
🌐 Live Application

https://airesumecritic.streamlit.app/

🧪 Testing Checklist

The application should be tested for:

 Application startup
 Dependency installation
 Gemini API integration
 Resume input
 Job description input
 AI analysis
 Resume scoring
 Keyword analysis
 Recruiter feedback
 PDF generation
 Streamlit Cloud deployment
Edge Cases

The application should also be checked with:

Empty resume
Empty job description
Very short resume
Very long resume
Invalid input
API failure
Missing API key
📊 Capstone Evaluation Alignment

The project is designed according to the official MirAI Capstone evaluation criteria.

1. Technical Implementation & Architecture — 25 Points

The application uses Python and Streamlit with structured application logic, AI integration, data processing, error handling, and cloud-compatible dependencies.

2. AI Integration & Prompt Engineering — 20 Points

The application integrates Google Gemini using dynamic resume and job-description context with specialized recruiter instructions.

3. UI/UX & Data Visualization — 20 Points

The Streamlit interface organizes AI-generated results into a clear dashboard-style experience with scores, feedback, keyword analysis, and recommendations.

4. Deployment & Cloud Engineering — 15 Points

The application is deployed on Streamlit Community Cloud.

Live URL:

https://airesumecritic.streamlit.app/

5. Open-Source Branding — 10 Points

The repository contains:

Project documentation
Architecture
Setup instructions
Technology stack
Repository structure
Live deployment link
6. System Design & Documentation — 10 Points

The documentation includes:

System architecture
Application data flow
API integration strategy
Prompt engineering strategy
Logic modules
Deployment architecture
Security strategy
📚 Internship Assignments
Assignment	Status
Assignment 1	✅ Completed
Assignment 2	✅ Completed
Assignment 3	✅ Completed
Assignment 4	✅ Completed
Assignment 5	✅ Completed
Assignment 6	✅ Completed
Assignment 7	✅ Completed
Final Capstone Project	✅ Completed
🎓 Learning Outcomes

During the internship, I developed practical experience in:

Python programming
Streamlit application development
Generative AI
Google Gemini API
Prompt engineering
API integration
Data processing
Git and GitHub
Cloud deployment
Technical documentation

The internship provided practical experience in taking an AI project from concept and implementation to cloud deployment.

🔗 Important Links
🚀 Live Capstone

https://airesumecritic.streamlit.app/

🐙 GitHub Repository

https://github.com/Sattypvt/mirai-ai-summer-internship-2026-

👨‍💻 Author
Satyander Bhagat

B.Tech Computer Science & Engineering

Interests
Artificial Intelligence
Generative AI
Machine Learning
Python Development
Software Engineering
🙏 Acknowledgement

I would like to thank MirAI School of Technology for providing the opportunity to learn and build practical Generative AI applications during the AI Summer Internship 2026.

🏆 Project Status
╔══════════════════════════════════════════════════════════════╗
║                     PROJECT STATUS                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Assignment 1            ✅ Completed                       ║
║  Assignment 2            ✅ Completed                       ║
║  Assignment 3            ✅ Completed                       ║
║  Assignment 4            ✅ Completed                       ║
║  Assignment 5            ✅ Completed                       ║
║  Assignment 6            ✅ Completed                       ║
║  Assignment 7            ✅ Completed                       ║
║  Final Capstone           ✅ Completed                       ║
║  Gemini Integration       ✅ Completed                       ║
║  Streamlit Deployment     ✅ Live                            ║
║  Documentation            ✅ Completed                       ║
║                                                              ║
║              AI RESUME CRITIC — TECH-ROAST                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

⭐ If you find this project useful, consider starring the repository!
