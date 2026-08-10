from datetime import datetime
from typing import Iterable

from sqlalchemy import text
from sqlalchemy.engine import Engine

from app.work24.models import Job

INSERT_SQL = text(
    """
    INSERT INTO jobs (
        source_site, provider_name, external_job_id, identity_hash,
        company_name, title, location, employment_type, job_type,
        salary_text, salary_min, salary_max, salary_unit,
        career_text, education_text, work_days, work_hours,
        deadline, posted_date, detail_url, original_url,
        description, requirements, benefits, qualifications,
        work24_application, company_type, remote_work, shift_work,
        alternate_day_work, status, first_seen_at, last_seen_at
    ) VALUES (
        :source_site, :provider_name, :external_job_id, :identity_hash,
        :company_name, :title, :location, :employment_type, :job_type,
        :salary_text, :salary_min, :salary_max, :salary_unit,
        :career_text, :education_text, :work_days, :work_hours,
        :deadline, :posted_date, :detail_url, :original_url,
        :description, :requirements, :benefits, :qualifications,
        :work24_application, :company_type, :remote_work, :shift_work,
        :alternate_day_work, :status, :now, :now
    )
    """
)

UPDATE_SQL = text(
    """
    UPDATE jobs SET
        provider_name = :provider_name,
        company_name = :company_name,
        title = :title,
        location = :location,
        employment_type = :employment_type,
        job_type = :job_type,
        salary_text = :salary_text,
        salary_min = :salary_min,
        salary_max = :salary_max,
        salary_unit = :salary_unit,
        career_text = :career_text,
        education_text = :education_text,
        work_days = :work_days,
        work_hours = :work_hours,
        deadline = :deadline,
        posted_date = :posted_date,
        detail_url = :detail_url,
        original_url = :original_url,
        work24_application = :work24_application,
        company_type = :company_type,
        remote_work = :remote_work,
        shift_work = :shift_work,
        alternate_day_work = :alternate_day_work,
        status = :status,
        last_seen_at = :now
    WHERE identity_hash = :identity_hash
       OR (source_site = :source_site AND external_job_id = :external_job_id AND :external_job_id IS NOT NULL)
    """
)

EXISTS_SQL = text(
    """
    SELECT id FROM jobs
    WHERE identity_hash = :identity_hash
       OR (source_site = :source_site AND external_job_id = :external_job_id AND :external_job_id IS NOT NULL)
    LIMIT 1
    """
)


def _params(job: Job, now: datetime) -> dict:
    return {
        "source_site": job.source_site,
        "provider_name": job.provider_name,
        "external_job_id": job.external_job_id,
        "identity_hash": job.identity_hash,
        "company_name": job.company_name,
        "title": job.title,
        "location": job.location,
        "employment_type": job.employment_type,
        "job_type": job.job_type,
        "salary_text": job.salary_text,
        "salary_min": job.salary_min,
        "salary_max": job.salary_max,
        "salary_unit": job.salary_unit,
        "career_text": job.career_text,
        "education_text": job.education_text,
        "work_days": job.work_days,
        "work_hours": job.work_hours,
        "deadline": job.deadline,
        "posted_date": job.posted_date,
        "detail_url": job.detail_url,
        "original_url": job.original_url,
        "description": job.description,
        "requirements": job.requirements,
        "benefits": job.benefits,
        "qualifications": job.qualifications,
        "work24_application": job.work24_application,
        "company_type": job.company_type,
        "remote_work": job.remote_work,
        "shift_work": job.shift_work,
        "alternate_day_work": job.alternate_day_work,
        "status": job.status,
        "now": now,
    }


def save_jobs(engine: Engine, jobs: Iterable[Job]) -> tuple[int, int]:
    inserted = 0
    updated = 0

    with engine.begin() as connection:
        for job in jobs:
            params = _params(job, datetime.now())
            exists = connection.execute(EXISTS_SQL, params).first()
            if exists:
                connection.execute(UPDATE_SQL, params)
                updated += 1
            else:
                connection.execute(INSERT_SQL, params)
                inserted += 1

    return inserted, updated
