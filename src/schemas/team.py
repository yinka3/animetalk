from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class CreateTeamMemberSchema(BaseModel):
    user_id: UUID = Field(..., description="The unique identifier of the user to be added as a team member.")

    class Config:
        from_attributes = True


class TeamMemberSchema(BaseModel):
    user_id: UUID = Field(..., description="The ID of the user in the team.")

    class Config:
        from_attributes = True


class TeamBaseSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50, description="The name of the team.")
    members: Optional[List[CreateTeamMemberSchema]] = Field(
        None, description="A list of user IDs to be added or updated in the team."
    )

    class Config:
        from_attributes = True


class CreateTeamSchema(TeamBaseSchema):
    name: str = Field(..., description="The name of the team.")


class UpdateTeamSchema(TeamBaseSchema):
    pass


class TeamSchema(TeamBaseSchema):
    id: UUID = Field(..., description="The unique identifier of the team.")
    created_at: datetime = Field(..., description="The date and time when the team was created.")
    members: List[TeamMemberSchema] = Field(..., description="A list of team members.")


class TeamSummarySchema(BaseModel):
    id: UUID = Field(..., description="The unique identifier of the team.")
    name: str = Field(..., description="The name of the team.")
    created_at: datetime = Field(..., description="The creation date of the team.")

    class Config:
        from_attributes = True