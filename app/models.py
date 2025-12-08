"""
Data models for the application.
Optional module for structured data representation.
"""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class AppInfo:
    """Represents basic app information from the store."""
    app_id: str
    title: str
    developer: str
    rating: Optional[float] = None
    reviews_count: Optional[int] = None
    installs: Optional[str] = None
    description: Optional[str] = None


@dataclass
class Review:
    """Represents a single app review."""
    review_id: str
    user_name: str
    rating: int
    text: str
    thumbs_up: int
    date: str
    reply_text: Optional[str] = None
    reply_date: Optional[str] = None
