from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class MatchRun(db.Model):
    __tablename__ = "match_runs"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    filename = db.Column(db.String(255), nullable=False)

    score_percent = db.Column(db.Integer, nullable=False)
    score_float = db.Column(db.Float, nullable=False)

    matched_keywords = db.Column(db.Text, nullable=True)   # comma-separated
    missing_keywords = db.Column(db.Text, nullable=True)   # comma-separated

    # Keep only previews (privacy + smaller DB)
    resume_preview = db.Column(db.Text, nullable=True)
    job_preview = db.Column(db.Text, nullable=True)

    # Suggestions (optional, but nice to save)
    grouped_missing = db.Column(db.Text, nullable=True)  # store as string for now
    bullets = db.Column(db.Text, nullable=True)          # newline-separated
    learning_plan = db.Column(db.Text, nullable=True)    # newline-separated
