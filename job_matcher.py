import re
from collections import Counter

STOPWORDS = {
    "a","an","the","and","or","to","of","in","on","for","with","as",
    "is","are","was","were","be","been","being","at","by","from",
    "this","that","these","those","it","its","we","you","your","our",
    "they","their","will","can","may","should","must","have","has","had",
    "do","does","did","want","looking","plus","using"
}

# ✅ MUST be defined before use
ALIASES = {
    "rest": "rest_api",
    "restful": "rest_api",
    "restapi": "rest_api",
    "apis": "api",
    "k8s": "kubernetes",
    "js": "javascript",
    "py": "python",
    "cicd": "ci_cd",
    "ci/cd": "ci_cd",
    "dockerized": "docker",
    "container": "docker",
    "containers": "docker",
    "containerization": "docker",
}

SKILL_GROUPS = {
    "cloud": {"aws", "azure", "gcp"},
    "containers": {"docker", "kubernetes"},
    "backend": {"flask", "django", "fastapi", "node", "nodejs"},
    "databases": {"sql", "postgresql", "mysql", "mongodb"},
    "testing": {"pytest", "unittest"},
    "devops": {"ci_cd"},
    "apis": {"rest_api", "api"},
}

BULLET_TEMPLATES = {
    "docker": [
        "Containerized a Flask application using Docker, enabling consistent local development and deployment.",
        "Created Dockerfiles and optimized image size by minimizing layers and using lightweight base images."
    ],
    "kubernetes": [
        "Deployed a containerized service to Kubernetes, configuring Deployments, Services, and scaling policies.",
        "Implemented health checks (liveness/readiness probes) to improve application reliability on Kubernetes."
    ],
    "aws": [
        "Deployed application components on AWS (e.g., EC2/S3/IAM), applying least-privilege access controls.",
        "Configured AWS services to support hosting/storage with basic monitoring and logging."
    ],
    "rest_api": [
        "Designed and implemented REST APIs (CRUD), including request validation and clear error handling.",
        "Documented API endpoints and tested them using Postman/cURL for consistent integration."
    ],
    "pytest": [
        "Wrote unit tests with pytest to validate core logic and prevent regressions.",
        "Added automated tests for tokenization and scoring logic using parametrized pytest cases."
    ],
    "ci_cd": [
        "Implemented a CI/CD workflow to automate tests and builds on every commit.",
        "Integrated automated checks into CI/CD to improve code quality and reliability."
    ],
}

LEARN_RESOURCES = {
    "docker": "Learn Docker basics: images, containers, Dockerfile; then containerize this Flask app.",
    "kubernetes": "Learn Kubernetes: pods, deployments, services; then deploy your Dockerized app.",
    "aws": "Learn AWS fundamentals: IAM, EC2, S3, CloudWatch; then host or store results.",
    "rest_api": "Learn REST: status codes, validation; then add an API endpoint to this app.",
    "pytest": "Learn pytest; then add unit tests for job_matcher + resume_parser.",
    "ci_cd": "Learn CI/CD basics; then add GitHub Actions to run tests automatically.",
}

def _tokenize(text: str) -> list[str]:
    text = (text or "").lower()
    tokens = re.findall(r"[a-z0-9_+#\.\/]+", text)

    cleaned = []
    for t in tokens:
        t = t.strip(".")
        if len(t) < 2:
            continue
        if t in STOPWORDS:
            continue
        t = ALIASES.get(t, t)
        cleaned.append(t)
    return cleaned


def _group_skills(skills: list[str]) -> dict:
    grouped = {k: [] for k in SKILL_GROUPS.keys()}
    other = []

    for s in skills:
        placed = False
        for group, vals in SKILL_GROUPS.items():
            if s in vals:
                grouped[group].append(s)
                placed = True
                break
        if not placed:
            other.append(s)

    grouped["other"] = other
    return grouped


def _build_bullet_suggestions(missing: list[str], limit: int = 6) -> list[str]:
    suggestions = []
    for s in missing:
        if s in BULLET_TEMPLATES:
            for b in BULLET_TEMPLATES[s]:
                suggestions.append(f"[Use only if true] {b}")
        if len(suggestions) >= limit:
            break
    return suggestions[:limit]


def _build_learning_plan(missing: list[str], limit: int = 6) -> list[str]:
    plan = []
    for s in missing:
        if s in LEARN_RESOURCES:
            plan.append(f"{s}: {LEARN_RESOURCES[s]}")
        if len(plan) >= limit:
            break
    return plan[:limit]


def calculate_match_score(resume_text: str, job_description: str, top_k: int = 30) -> dict:
    resume_tokens = set(_tokenize(resume_text))
    job_tokens = _tokenize(job_description)

    job_counts = Counter(job_tokens)
    top_job_keywords = job_counts.most_common(top_k)
    top_job_set = {k for k, _ in top_job_keywords}

    matched = sorted(list(top_job_set.intersection(resume_tokens)))
    missing = sorted(list(top_job_set.difference(resume_tokens)))

    score_float = len(matched) / max(len(top_job_set), 1)
    score_percent = int(round(score_float * 100))

    grouped_missing = _group_skills(missing)
    resume_bullets_to_add = _build_bullet_suggestions(missing, limit=6)
    learning_plan = _build_learning_plan(missing, limit=6)

    return {
        "score_percent": score_percent,
        "score_float": round(score_float, 3),
        "matched_keywords": matched,
        "missing_keywords": missing,
        "top_job_keywords": top_job_keywords,
        "grouped_missing": grouped_missing,
        "resume_bullets_to_add": resume_bullets_to_add,
        "learning_plan": learning_plan,
    }
