from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass(slots=True)
class Job:
    title: str
    detail_url: str
    identity_hash: str
    source_site: str = "WORK24"
    provider_name: Optional[str] = None
    external_job_id: Optional[str] = None
    company_name: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    job_type: Optional[str] = None
    salary_text: Optional[str] = None
    salary_min: Optional[Decimal] = None
    salary_max: Optional[Decimal] = None
    salary_unit: Optional[str] = None
    career_text: Optional[str] = None
    education_text: Optional[str] = None
    work_days: Optional[str] = None
    work_hours: Optional[str] = None
    deadline: Optional[date] = None
    posted_date: Optional[date] = None
    original_url: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    benefits: Optional[str] = None
    qualifications: Optional[str] = None
    work24_application: Optional[bool] = None
    company_type: Optional[str] = None
    remote_work: Optional[bool] = None
    shift_work: Optional[bool] = None
    alternate_day_work: Optional[bool] = None
    status: str = "OPEN"
