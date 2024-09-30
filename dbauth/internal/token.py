class Token:
    """Represents an authentication token with its expiration time."""

    def __init__(self, auth_token, expires):
        self.auth_token = auth_token
        self.expires = expires

    def get_auth_token(self):
        return self.auth_token

    def get_expires(self):
        return self.expires
