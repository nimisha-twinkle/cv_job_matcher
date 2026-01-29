# Resume–Job Matcher with Skill Gap Analysis

A full-stack Flask application that analyzes a resume against a job description, computes a match score, identifies missing skills, and provides actionable resume improvement and learning suggestions. The app also persists match history using a relational database for analytics and tracking.

---

## 🚀 Features

- **Resume Parsing**
  - Extracts text from PDF resumes using `pdfplumber`

- **Job Matching Engine**
  - Keyword normalization & alias handling (e.g., REST ↔ REST API)
  - Match score calculation (0–100)
  - Identifies matched vs missing skills

- **Skill Gap Intelligence**
  - Groups missing skills (e.g., Containers, Testing, DevOps)
  - Suggests resume bullets (truthfully)
  - Recommends learning steps for missing skills

- **Persistent Storage**
  - Stores match history using SQLite + SQLAlchemy
  - Tracks score, matched skills, missing skills, and timestamps

- **History View**
  - View past resume–job matches with scores and gaps

---

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite, SQLAlchemy
- **NLP / Text Processing:** Regex, keyword normalization
- **PDF Parsing:** pdfplumber
- **Frontend:** HTML, CSS (Jinja2 templates)

---

## Project Structure

