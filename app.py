import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for

from resume_parser import extract_text_from_resume
from job_matcher import calculate_match_score
from models import db, MatchRun

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB

# ---- SQLite DB config ----
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cv_matcher.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def home():
    # score_percent=None ensures results block doesn't show on fresh load
    return render_template("index.html", score_percent=None)


@app.route("/match", methods=["GET", "POST"])
def match():
    if request.method == "GET":
        return redirect(url_for("home"))

    if "resume" not in request.files:
        return render_template("index.html", error="Please upload a resume PDF.", score_percent=None)

    resume_file = request.files["resume"]
    job_description = request.form.get("job_desc", "")

    if not resume_file or resume_file.filename == "":
        return render_template("index.html", error="No file selected.", score_percent=None)

    if not resume_file.filename.lower().endswith(".pdf"):
        return render_template("index.html", error="Only PDF files are allowed.", score_percent=None)

    if not job_description.strip():
        return render_template("index.html", error="Please paste a job description.", score_percent=None)

    # Save file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = resume_file.filename.replace(" ", "_")
    saved_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{timestamp}_{safe_name}")
    resume_file.save(saved_path)

    # Extract text
    resume_text = extract_text_from_resume(saved_path)
    if resume_text.startswith("[ERROR]"):
        return render_template("index.html", error=resume_text, score_percent=None)

    # Match (increase top_k so skills like pytest show up)
    result = calculate_match_score(resume_text, job_description, top_k=30)

    resume_preview = resume_text[:1200]
    job_preview = job_description[:1200]

    # Save to DB
    run = MatchRun(
        filename=os.path.basename(saved_path),
        score_percent=int(result["score_percent"]),
        score_float=float(result["score_float"]),
        matched_keywords=", ".join(result.get("matched_keywords", [])),
        missing_keywords=", ".join(result.get("missing_keywords", [])),
        resume_preview=resume_preview,
        job_preview=job_preview,
        grouped_missing=str(result.get("grouped_missing", {})),
        bullets="\n".join(result.get("resume_bullets_to_add", [])),
        learning_plan="\n".join(result.get("learning_plan", [])),
    )
    db.session.add(run)
    db.session.commit()

    return render_template(
        "index.html",
        score_percent=result["score_percent"],
        score_float=result["score_float"],
        matched_keywords=result.get("matched_keywords", []),
        missing_keywords=result.get("missing_keywords", []),
        top_job_keywords=result.get("top_job_keywords", []),
        grouped_missing=result.get("grouped_missing", {}),
        resume_bullets_to_add=result.get("resume_bullets_to_add", []),
        learning_plan=result.get("learning_plan", []),
        resume_preview=resume_preview,
        job_preview=job_preview,
    )


@app.route("/history", methods=["GET"])
def history():
    rows = MatchRun.query.order_by(MatchRun.id.desc()).limit(30).all()
    return render_template("history.html", rows=rows)


if __name__ == "__main__":
    print("Resume Job Matcher Project Started Successfully")
    app.run(debug=True)
