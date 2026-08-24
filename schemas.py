from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime

try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:
        def __init__(self, **kwargs):
            # Resolve class annotations / defaults
            for key, val in self.__class__.__dict__.items():
                if not key.startswith("__") and not callable(val):
                    setattr(self, key, val() if callable(val) else val)
            for k, v in kwargs.items():
                setattr(self, k, v)
            if hasattr(self, "audit_logs") and (self.audit_logs is None or type(self.audit_logs).__name__ == "Field"):
                self.audit_logs = []

        def dict(self):
            return self.__dict__

    def Field(default=None, default_factory=None, description=""):
        if default_factory is not None:
            return default_factory()
        return default




class PostStatus(str, Enum):
    PLANNING = "PLANNING"
    DRAFTED = "DRAFTED"
    DESIGNED = "DESIGNED"
    SUPERVISOR_APPROVED = "SUPERVISOR_APPROVED"
    PENDING_HUMAN_APPROVAL = "PENDING_HUMAN_APPROVAL"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"
    REVISION_REQUESTED = "REVISION_REQUESTED"
    REJECTED = "REJECTED"

class PostCategory(str, Enum):
    JLPT = "JLPT"
    PRACTICAL_JAPANESE = "PRACTICAL_JAPANESE"
    STUDY_IN_JAPAN = "STUDY_IN_JAPAN"
    EVENT_COMMUNITY = "EVENT_COMMUNITY"

class TargetLevel(str, Enum):
    N5 = "N5"
    N4 = "N4"
    N3 = "N3"
    ALL = "ALL"
    VISA_SEEKER = "VISA_SEEKER"

class PostMetadata(BaseModel):
    category: PostCategory
    target_level: TargetLevel = TargetLevel.ALL
    goal: str = Field(description="例: LEAD_DM, SAVE_ENGAGEMENT, EVENT_BOOKING")
    topic_summary: str

class SlidePlan(BaseModel):
    slide_index: int
    headline: str
    body_text_ja: str
    body_text_es: str
    notes_for_designer: Optional[str] = None

class PostPlan(BaseModel):
    post_id: str
    metadata: PostMetadata
    title_ja: str
    title_es: str
    slides_outline: List[SlidePlan]

class PostContent(BaseModel):
    title_ja: str
    title_es: str
    caption_full: str
    hook_es: str
    body_es: str
    cta_trigger_word: str = "JLPT"
    hashtags: List[str]

class VisualSlide(BaseModel):
    slide_index: int
    image_path: str
    headline: str
    caption_overlay: Optional[str] = None

class PostVisuals(BaseModel):
    media_type: str = "CAROUSEL_ALBUM"  # or IMAGE, REEL
    source: str = "GENERATED"            # or GOOGLE_DRIVE, HYBRID
    drive_source_folder: Optional[str] = None
    slides: List[VisualSlide]

class ApprovalState(BaseModel):
    whatsapp_message_id: Optional[str] = None
    status: PostStatus = PostStatus.PENDING_HUMAN_APPROVAL
    review_comments: Optional[str] = None
    reviewed_at: Optional[datetime] = None

class InstagramPostPackage(BaseModel):
    post_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    scheduled_publish_time: Optional[datetime] = None
    status: PostStatus = PostStatus.PLANNING
    metadata: PostMetadata
    content: Optional[PostContent] = None
    visuals: Optional[PostVisuals] = None
    approval: Optional[ApprovalState] = None
    audit_logs: List[str] = Field(default_factory=list)

    def log(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.audit_logs.append(f"[{timestamp}] {message}")
