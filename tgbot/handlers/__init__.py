"""Import all routers and add them to routers_list."""

from .chat_admins import chat_admins_router
from .group_approval import group_approval_router

routers_list = [
    # spam_router, Disabled for now
    group_approval_router,
    chat_admins_router,
]

__all__ = [
    "routers_list",
]
