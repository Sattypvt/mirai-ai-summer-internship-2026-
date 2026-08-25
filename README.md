# 🤖 MirAI AI Summer Internship 2026

```text
╔══════════════════════════════════════════════════════════════╗
║              MIRAI AI SUMMER INTERNSHIP 2026                ║
║                                                              ║
║   Python • Streamlit • Gemini API • Generative AI • GitHub  ║
╚══════════════════════════════════════════════════════════════╝
👨‍💻 Student

Satyander Bhagat

Track: AI Builder
Program: MirAI School of Technology — AI Summer Internship 2026

📌 About This Repository

This repository contains all assignments and the final capstone project completed during the MirAI School of Technology AI Summer Internship 2026.

The internship focused on building practical applications using Python, Streamlit, Generative AI, Google Gemini API, prompt engineering, Git/GitHub, data processing, and cloud deployment.

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
🚀 Live Capstone Deployment
🤖 AI Resume Critic — Tech-Roast
Live Application

👉 https://airesumecritic.streamlit.app/

The final capstone is an AI-powered resume analysis application that evaluates a candidate's resume against a target job description.

The application uses Google Gemini to act as a strict technical recruiter and provide actionable feedback.

🎯 Problem Statement
Problem Statement #17 — The AI Resume Critic (Tech-Roast)

Users provide their resume and a target job description. The AI evaluates the resume as a strict recruiter and identifies missing keywords, weak bullet points, skill gaps, and areas for improvement.

✨ Key Features
📄 Resume Analysis

Analyzes the candidate's resume content, skills, experience, and overall presentation.

🎯 Job Description Matching

Compares the resume against a target job description to determine how well the candidate matches the desired role.

🔑 Missing Keyword Detection

Identifies important keywords and technical skills from the job description that are missing from the resume.

📝 Weak Bullet Point Detection

Identifies weak, vague, or poorly written resume bullet points and provides stronger alternatives.

📊 Resume Scoring

Provides an overall assessment of the resume and its alignment with the target job.

👨‍💼 Recruiter-Style Feedback

Gemini is instructed to behave as a strict technical recruiter rather than a generic chatbot.

💡 Improvement Suggestions

Provides actionable recommendations to improve the resume for the selected position.

📥 PDF Report

Generates a downloadable PDF report containing the resume analysis and feedback.

🧠 System Architecture
🔄 Application Data Flow
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
          ┌─────────────┐     ┌───────────────┐
          │   Resume    │     │ Job Description│
          └──────┬──────┘     └───────┬───────┘
                 │                    │
                 └──────────┬─────────┘
                            ▼
                 ┌────────────────────┐
                 │  Prompt Builder    │
                 └──────────┬─────────┘
                            │
                            ▼
                 ┌────────────────────┐
                 │   Gemini API       │
                 │  Generative AI     │
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
🧠 AI & Prompt Engineering

The application uses the Google Gemini API to perform context-aware resume evaluation.

Gemini receives:

Resume
+
Target Job Description
+
Recruiter Evaluation Criteria

The AI is instructed to behave as a specialized technical recruiter.

The analysis focuses on:

Technical skill alignment
Job-description matching
Missing keywords
Weak resume statements
Bullet-point quality
Relevant experience
Skill gaps
Actionable improvements
Overall recruiter assessment

Dynamic context is provided to the AI so that the response changes according to the resume and target job description entered by the user.

🛠️ Technology Stack
Technology	Purpose
🐍 Python	Application development
🎨 Streamlit	Web application and user interface
🤖 Google Gemini API	Generative AI and resume analysis
🐼 Pandas	Data processing
📄 ReportLab	PDF report generation
🔐 Python-dotenv	Environment configuration
🐙 Git	Version control
🐙 GitHub	Source code management
☁️ Streamlit Community Cloud	Cloud deployment
📁 Final Capstone Structure
Final-Capstone-Project/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
🔐 API Key & Secrets

The Gemini API key is not stored in the GitHub repository.

For local development, create a .env file:

GEMINI_API_KEY=YOUR_API_KEY

For Streamlit Community Cloud, the API key is stored securely using:

App Settings → Secrets

Example:

GEMINI_API_KEY = "YOUR_API_KEY"

⚠️ Never commit a real API key to GitHub.

⚙️ Local Setup
1. Clone the repository
git clone https://github.com/Sattypvt/mirai-ai-summer-internship-2026-.git
2. Open the repository
cd mirai-ai-summer-internship-2026-
3. Open the capstone project
cd Final-Capstone-Project
4. Install dependencies
pip install -r requirements.txt
5. Configure Gemini API

Create a .env file:

GEMINI_API_KEY=YOUR_API_KEY
6. Run the application
streamlit run app.py

The application will then be available locally through Streamlit.

📦 Dependencies

The capstone uses:

streamlit
pandas
google-genai
python-dotenv
pydantic
reportlab

Dependencies are defined in:

Final-Capstone-Project/requirements.txt
☁️ Cloud Deployment

The final capstone is deployed using Streamlit Community Cloud.

Deployment Flow
GitHub Repository
       │
       ▼
Streamlit Community Cloud
       │
       ▼
requirements.txt
       │
       ▼
Streamlit Application
       │
       ▼
Google Gemini API
       │
       ▼
AI Resume Analysis
Live Application

👉 https://airesumecritic.streamlit.app/

🧪 Testing

The application should be tested for the following:

 Application starts successfully
 Dependencies install successfully
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

The project follows the official MirAI Capstone evaluation criteria.

1. Technical Implementation & Architecture — 25 Points

The application uses Python and Streamlit with structured application logic, AI integration, data processing, error handling, and cloud-compatible dependencies.

2. AI Integration & Prompt Engineering — 20 Points

The application integrates Google Gemini using dynamic context and specialized recruiter instructions to produce resume-specific analysis.

3. UI/UX & Data Visualization — 20 Points

The Streamlit interface presents resume scores, feedback, keyword analysis, and recommendations in an organized dashboard-style interface.

4. Deployment & Cloud Engineering — 15 Points

The application is deployed and publicly accessible through Streamlit Community Cloud.

Live URL:
https://airesumecritic.streamlit.app/

5. Open-Source Branding — 10 Points

The repository includes project documentation, architecture, setup instructions, technology information, repository structure, and the live deployment link.

6. System Design & Documentation — 10 Points

The documentation includes:

System architecture
Application data flow
Gemini API integration
Prompt engineering strategy
Deployment architecture
Project structure
Setup instructions
📚 Internship Assignments

This repository contains the assignments completed during the MirAI AI Summer Internship 2026.

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

During the internship, I developed practical experience with:

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

The internship helped me understand how to move from an idea to a functional AI-powered web application.

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
║             🤖 AI RESUME CRITIC — TECH-ROAST                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

⭐ If you find this project useful, consider starring the repository!
