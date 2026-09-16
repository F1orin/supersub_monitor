"""Domain-specific application errors."""


class UrbanSoccerAuthenticationError(RuntimeError):
    """Raised when UrbanSoccer rejects the configured authentication token."""
