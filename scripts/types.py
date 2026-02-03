"""Type definitions for Context Manager.

This module defines the type structures used throughout the context manager.
"""

from typing import TypedDict

from typing_extensions import NotRequired


class ContextInfo(TypedDict):
    """Type definition for parsed context information.

    Attributes:
        project: Project name
        created: Creation date
        last_session: Last session date
        session_count: Total number of sessions
        status: Project status (active/paused/completed)
        category: Project category
        project_type: Technical project type
        current_focus: Current work focus
        next_steps: Next steps to take
        brief: Brief project description
        branch: Current Git branch
        stack: List of technologies used
        todos: List of pending todo items
        has_sessions: Whether session records exist
        format_version: Detected format version (v1/v2/mixed)
        path: Project directory name (not in frontmatter)
    """

    project: str
    created: str
    last_session: str
    session_count: int
    status: str
    category: str
    project_type: str
    current_focus: str
    next_steps: str
    brief: str
    branch: str
    stack: list[str]
    todos: list[str]
    has_sessions: bool
    format_version: str
    path: NotRequired[str]


class ProjectInfo(TypedDict):
    """Type definition for project listing information.

    A simplified version of ContextInfo used in project listings.
    """

    path: str
    project: str
    status: str
    last_session: str
    current_focus: str
    session_count: int
    category: str
    branch: str


# Status constants
STATUS_ACTIVE = "active"
STATUS_PAUSED = "paused"
STATUS_COMPLETED = "completed"
STATUS_UNKNOWN = "unknown"

# Category constants (in Chinese)
CATEGORY_EXPLORATORY = "探索性"
CATEGORY_PRODUCT = "产品"
CATEGORY_TEMPORARY = "临时"
CATEGORY_LEARNING = "学习"

# Format version constants
FORMAT_V1 = "v1"
FORMAT_V2 = "v2"
FORMAT_MIXED = "mixed"

# Valid status values
VALID_STATUSES = [STATUS_ACTIVE, STATUS_PAUSED, STATUS_COMPLETED, STATUS_UNKNOWN]

# Valid category values
VALID_CATEGORIES = [
    CATEGORY_EXPLORATORY,
    CATEGORY_PRODUCT,
    CATEGORY_TEMPORARY,
    CATEGORY_LEARNING,
]

# Valid fields for update command
VALID_UPDATE_FIELDS = [
    "project",
    "status",
    "category",
    "project_type",
    "current_focus",
    "next_steps",
    "brief",
    "branch",
]
