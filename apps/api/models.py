import uuid 
from datetime import datetime, timezone

from sqlalchemy import String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.api.db import Base 

class Document(Base): 
    """
    Represent a stored file or document in the database.
    Inherits from the Base class defined in db.py setup. 
    """
    __tablename__ = "documents" 

    # Primary key using UUID 
    # default=uuid.uuid4 ensures a new ID is generated for every new record
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
        )
    
    # File metadata fields
    # filename: Name of the file, limited to 255 characters, cannot be null
    # mime_type: type of the file (e.g., "application/pdf"), limited to 120 characters, cannot be null
    # file_path: location where the file is stored on disk, limited to 1024 characters, cannot be null
    filename: Mapped[str] = mapped_column(String(255), nullable=False) 
    mime_type: Mapped[str] = mapped_column(String(120), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)

    # Timestamp with Timezone support
    # lambda function to ensure the time is captured at the moment of record creation, and stored in UTC to avoid timezone issues
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False) 