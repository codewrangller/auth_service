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
        """Generate a random token and store it in Redis with the user's email."""
        token = secrets.token_urlsafe(32)  # Generate a secure random token
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

    
