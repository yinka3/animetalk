from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from src.utils import JobStatus


class JobApplicationBaseSchema(BaseModel):
    cover_letter: Optional[str] = Field(None, description="The seller's explanation of their suitability for the job.")
    bid_amount: float = Field(..., description="The amount bid by the seller for the job.")

    class Config:
        from_attributes = True


class JobApplicationsSchema(JobApplicationBaseSchema):
    id: UUID = Field(..., description="The unique ID of the job application.")
    created_at: datetime = Field(..., description="The date and time when the application was created.")
    status: JobStatus = Field(..., description="The current status of the application.")


class CreateJobApplicationSchema(JobApplicationBaseSchema):
    job_id: UUID = Field(..., description="The ID of the job being applied for.")
    seller_id: UUID = Field(..., description="The ID of the seller applying for the job.")


class UpdateJobApplicationSchema(BaseModel):
    cover_letter: Optional[str] = Field(None, description="An updated explanation of the seller's suitability for the job.")
    bid_amount: Optional[float] = Field(None, description="The updated amount the seller is bidding for the job.")
    status: Optional[JobStatus] = Field(None, description="The updated status of the application (e.g., 'Accepted', 'Rejected').")

    class Config:
        from_attributes = True


class JobBaseSchema(BaseModel):
    title: str = Field(..., description="The title of the job.")
    description: str = Field(..., description="A detailed description of the job.")
    budget: float = Field(..., description="The budget allocated for the job.")
    deadline: str = Field(..., description="The deadline for the job.")

    class Config:
        from_attributes = True


class JobsSchema(JobBaseSchema):
    pass

class CreateJobResponseSchema(JobBaseSchema):
    buyer_id: UUID = Field(..., description="The ID of the buyer posting the job.")



class UpdateJobSchema(BaseModel):
    title: Optional[str] = Field(..., description="The updated title of the job.")
    description: Optional[str] = Field(..., description="An updated detailed description of the job.")
    budget: Optional[float] = Field(..., description="The updated budget allocated for the job.")
    deadline: Optional[datetime] = Field(..., description="The updated deadline for the job.")

    class Config:
        from_attributes = True

class JobSummarySchema(BaseModel):
    id: UUID = Field(..., description="The unique ID of the job.")
    title: str = Field(..., description="The title of the job.")
    budget: Optional[float] = Field(None, description="The budget allocated for the job.")

    class Config:
        from_attributes = True

class SearchFilter(BaseModel):
    skill: Optional[str] = Field(..., description="The name of the skill.")
    rating: Optional[int] = Field(..., description="The rating of the seller.")