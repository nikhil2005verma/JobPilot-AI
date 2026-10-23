"""Pydantic schemas: validate everything that crosses a boundary (LLM output, files, forms)."""
from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ResumeProfileSchema(BaseModel):
    skills: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    internships: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    preferred_roles: list[str] = Field(default_factory=list)
    preferred_locations: list[str] = Field(default_factory=list)
    experience_level: str = "Fresher"

    @field_validator("skills", "preferred_roles", "preferred_locations")
    @classmethod
    def _clean(cls, values: list[str]) -> list[str]:
        seen, out = set(), []
        for v in values:
            v = v.strip()
            if v and v.lower() not in seen:
                seen.add(v.lower())
                out.append(v)
        return out


class JobSchema(BaseModel):
    source: str
    external_id: str | None = None
    title: str
    company: str
    description: str = ""
    required_skills: list[str] = Field(default_factory=list)
    location: str = ""
    work_mode: Literal["Remote", "Hybrid", "On-site", ""] = ""
    experience: str = ""
    salary: str | None = None
    posted_at: date | None = None
    url: str
    apply_instructions: str = ""

    @field_validator("url")
    @classmethod
    def _https_only(cls, v: str) -> str:
        if not v.startswith(("https://", "http://")):
            raise ValueError("Job URL must be http(s)")
        return v


class JobMatchSchema(BaseModel):
    score: float = Field(ge=0, le=100)
    matching_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    eligibility_concerns: list[str] = Field(default_factory=list)
    explanation: str = ""
    recommended_action: str = ""
