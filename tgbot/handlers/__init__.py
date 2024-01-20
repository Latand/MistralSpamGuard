"""Import all routers and add them to routers_list."""

from .spam import spam_router

routers_list = [
    spam_router,
]

__all__ = [
    "routers_list",
]
