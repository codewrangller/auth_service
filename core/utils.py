import redis
from django.conf import settings
import secrets
from datetime import timedelta
import os
from typing import Union

# Initialize Redis client using connection string
redis_url = os.environ.get('REDIS_URI', 'redis://localhost:6379/1')
redis_client = redis.from_url(
    url=redis_url,
    decode_responses=True  # Automatically decode responses to strings
)



class RedisTokenManager:
    @staticmethod
    def generate_password_reset_token(user_email: str) -> str:
        """Generate a reset token or return existing active token for the user."""
        # First check if user already has an active token in order to prevent redis from getting clogged up with tokens
        pattern = f"password_reset:*"
        for key in redis_client.scan_iter(pattern):
            email = redis_client.get(key)
            if email == user_email:
                # Extract token from key
                existing_token = key.split(':')[1]
                # Get TTL of existing token
                ttl = redis_client.ttl(key)
                if ttl > 0:  # Token is still valid
                    return existing_token

        # No active token found, generate new one
        token = secrets.token_urlsafe(32)
        key = f"password_reset:{token}"
        # Store token with email and set expiry to 10 minutes
        redis_client.setex(
            name=key,
            time=timedelta(minutes=10),
            value=user_email
        )
        return token

    @staticmethod
    def verify_password_reset_token(token: str) -> Union[str, None]:
        """Verify if token exists and return associated email if valid."""
        key = f"password_reset:{token}"
        email = redis_client.get(key)
        if email:
            # Delete the token after verification to prevent reuse
            redis_client.delete(key)
        return email

    
