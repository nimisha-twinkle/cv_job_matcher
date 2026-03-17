Skill Gap Analysis & Match Scoring Tool

A Flask-based web application that compares a candidate’s resume against a job description to calculate a match score, highlight overlapping and missing skills, and suggest actionable improvements — including resume bullets and learning recommendations.

**Features**

** Resume Parsing
Upload PDF resumes and extract structured text automatically.

** Job–Resume Matching
Calculates a match score (0–100) based on keyword overlap.

** Matched Skills
Highlights skills already present in the resume.

** Missing Skills Detection
Identifies important job keywords not found in the resume.

** Grouped Skill Gaps
Groups missing skills into categories like:
Containers
Testing
CI/CD
Other technical gaps

** Resume Bullet Suggestions (Truthful Use)
Generates example bullets you may add only if you have actually done the work.

** Learning Recommendations
Suggests what to learn next based on missing skills.

** Match History (Database-backed)
Stores recent match runs with:
Timestamp
Resume name
Score
Matched & missing keywords


**Tech Stack
Backend: Python, Flask
Frontend: HTML (Jinja2 templates)
Database: SQLite (via Flask-SQLAlchemy)
Parsing: PDF text extraction
Version Control: Git & GitHub


** Project Structure
cv_job_matcher/
│
├── app.py                 # Flask application entry point
├── job_matcher.py         # Matching & scoring logic
├── resume_parser.py       # Resume PDF parsing
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── index.html
│   ├── result.html
│   └── history.html
├── .gitignore
└── README.md


Setup Instructions:
1. Clone the Repo
git clone https://github.com/nimisha-twinkle/cv_job_matcher.git
cd cv_job_matcher

2. Create & activate virtual environment
python -m venv venv
venv\Scripts\activate    # Windows

3. Install dependencies
pip install -r requirements.txt

4. Run the application
Run the application

5. python app.py
http://127.0.0.1:5000



Author:
Nimisha Twinkle Bonigala
MS Computer Science | Resume–Job Matching & Career Tools
🔗 GitHub: https://github.com/nimisha-twinkle