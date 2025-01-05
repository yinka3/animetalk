from datetime import datetime

from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

from src.utils import ContentType


# TODO: Will need to create a tag for comments, post, and fanart each

class BaseCommentSchema(BaseModel):
    content: str = Field(..., description="The content of the comment.")
    likes: Optional[int] = Field(0, description="The number of likes on the comment.")
    dislikes: Optional[int] = Field(0, description="The number of dislikes on the comment.")
    is_deleted: Optional[bool] = Field(False, description="Whether the comment has been deleted.")

    class Config:
        from_attributes = True

class UpdateCommentSchema(BaseModel):
    content: Optional[str] = Field(None, description="The updated content of the comment.")
    is_deleted: Optional[bool] = Field(None, description="Mark the comment as deleted.")

    class Config:
        from_attributes = True


class BasePostSchema(BaseModel):
    title: str = Field(..., description="The title of the post.")
    description: Optional[str] = Field(None, description="The description of the post.")
    file_path: str = Field(..., description="The file path of the uploaded content.")
    file_name: str = Field(..., description="The file name of the uploaded content.")

    class Config:
        from_attributes = True

class UpdatePostSchema(BasePostSchema):
    pass


class BaseFanArtSchema(BaseModel):
    title: str = Field(..., description="The title of the fan art.")
    description: Optional[str] = Field(None, description="The description of the fan art.")
    file_path: str = Field(..., description="The file path of the uploaded content.")
    file_name: str = Field(..., description="The file name of the uploaded content.")

    class Config:
        from_attributes = True

class UpdateFanArtSchema(BaseFanArtSchema):
    pass

class BaseSavedContentSchema(BaseModel):
    content_id: UUID = Field(..., description="The ID of the saved content.")
    content_type: str = Field(..., description="The type of the saved content (e.g., 'POST', 'FANART').")

    class Config:
        from_attributes = True

class BaseReviewSchema(BaseModel):
    rating: int = Field(..., description="The rating given by the reviewer.")
    content: str = Field(..., description="The content of the review.")

    class Config:
        from_attributes = True

class BaseTagSchema(BaseModel):
    tagged_user_id: UUID = Field(..., description="The ID of the user being tagged.")
    content_id: UUID = Field(..., description="The ID of the associated content.")
    content_type: ContentType = Field(..., description="The type of the associated content (e.g., 'POST', 'FANART').")

    class Config:
        from_attributes = True

class UpdateTagSchema(BaseModel):
    content_id: Optional[UUID] = Field(None, description="The updated ID of the associated content.")
    content_type: Optional[ContentType] = Field(None, description="The updated type of the associated content (e.g., 'POST', 'FANART').")

    class Config:
        from_attributes = True


class TagSummarySchema(BaseModel):
    tagged_user_id: UUID = Field(..., description="The ID of the user being tagged.")
    content_id: UUID = Field(..., description="The ID of the associated content.")
    content_type: ContentType = Field(..., description="The type of the associated content (e.g., 'POST', 'FANART').")

    class Config:
        from_attributes = True

class CommentSchema(BaseCommentSchema):
    id: UUID = Field(..., description="The unique identifier of the comment.")
    user_id: UUID = Field(..., description="The ID of the user who created the comment.")
    username: str = Field(..., description="The username of the user who created the comment.")
    created_at: datetime = Field(..., description="The timestamp when the comment was created.")
    updated_at: Optional[datetime] = Field(None, description="The timestamp when the comment was last updated.")

class CreateCommentSchema(BaseCommentSchema):
    parent_comment_id: Optional[UUID] = Field(None, description="The ID of the parent comment, if any.")
    post_id: Optional[UUID] = Field(None, description="The ID of the associated post.")
    fanArt_id: Optional[UUID] = Field(None, description="The ID of the associated fan art.")

class PostSchema(BasePostSchema):
    id: UUID = Field(..., description="The unique identifier of the post.")
    user_id: UUID = Field(..., description="The ID of the user who created the post.")
    username: str = Field(..., description="The username of the user who created the post.")
    created_at: datetime = Field(..., description="The timestamp when the post was created.")
    updated_at: Optional[datetime] = Field(None, description="The timestamp when the post was last updated.")

class CreatePostSchema(BasePostSchema):
    user_id: UUID = Field(..., description="The ID of the user creating the post.")

class FanArtSchema(BaseFanArtSchema):
    id: UUID = Field(..., description="The unique identifier of the fan art.")
    user_id: UUID = Field(..., description="The ID of the user who created the fan art.")
    username: str = Field(..., description="The username of the user who created the fan art.")
    created_at: datetime = Field(..., description="The timestamp when the fan art was created.")
    updated_at: Optional[datetime] = Field(None, description="The timestamp when the fan art was last updated.")

class CreateFanArtSchema(BaseFanArtSchema):
    user_id: UUID = Field(..., description="The ID of the user creating the fan art.")

class SavedContentSchema(BaseSavedContentSchema):
    id: UUID = Field(..., description="The unique identifier of the saved content.")
    user_id: UUID = Field(..., description="The ID of the user who saved the content.")
    saved_at: datetime = Field(..., description="The timestamp when the content was saved.")

class CreateSavedContentSchema(BaseSavedContentSchema):
    user_id: UUID = Field(..., description="The ID of the user saving the content.")

class ReviewSchema(BaseReviewSchema):
    id: UUID = Field(..., description="The unique identifier of the review.")
    seller_id: int = Field(..., description="The ID of the seller being reviewed.")
    buyer_id: int = Field(..., description="The ID of the buyer being reviewed.")
    reviewer_id: int = Field(..., description="The ID of the reviewer.")
    created_at: datetime = Field(..., description="The timestamp when the review was created.")

class CreateReviewSchema(BaseReviewSchema):
    seller_id: int = Field(..., description="The ID of the seller being reviewed.")
    buyer_id: int = Field(..., description="The ID of the buyer being reviewed.")
    reviewer_id: int = Field(..., description="The ID of the reviewer.")

class TagSchema(BaseTagSchema):
    id: UUID = Field(..., description="The unique identifier of the tag.")
    created_at: datetime = Field(..., description="The timestamp when the tag was created.")


class CreateTagSchema(BaseTagSchema):
    pass

