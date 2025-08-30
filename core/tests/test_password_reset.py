import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
import fakeredis

# Mock Redis client for testing
@pytest.fixture(autouse=True)
def mock_redis(monkeypatch):
    fake_redis = fakeredis.FakeStrictRedis(decode_responses=True, version=6)
    import core.utils
    monkeypatch.setattr(core.utils, 'redis_client', fake_redis)
    return fake_redis

@pytest.fixture
def test_user(db):
    User = get_user_model()
    return User.objects.create_user(
        username='testuser',  # Username is required
        email='test@example.com',
        password='testpass123',
        full_name='Test User'
    )

@pytest.mark.django_db
class TestPasswordReset:
    def test_request_password_reset_valid_email(self, client, test_user):
        """Test requesting password reset with valid email"""
        url = reverse('password_reset_request')
        response = client.post(url, {'email': test_user.email})
        
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data
        assert response.data['email'] == test_user.email

    def test_request_password_reset_invalid_email(self, client):
        """Test requesting password reset with invalid email"""
        url = reverse('password_reset_request')
        response = client.post(url, {'email': 'nonexistent@example.com'})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_confirm_password_reset_valid_token(self, client, test_user, mock_redis):
        """Test confirming password reset with valid token"""
        # First request a reset token
        request_url = reverse('password_reset_request')
        request_response = client.post(request_url, {'email': test_user.email})
        token = request_response.data['token']
        
        # Now try to reset password with the token
        confirm_url = reverse('password_reset_confirm')
        response = client.post(confirm_url, {
            'token': token,
            'new_password': 'newpass123',
            'confirm_password': 'newpass123'
        })
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify user can login with new password
        test_user.refresh_from_db()
        assert test_user.check_password('newpass123')

    def test_confirm_password_reset_invalid_token(self, client):
        """Test confirming password reset with invalid token"""
        url = reverse('password_reset_confirm')
        response = client.post(url, {
            'token': 'invalid_token',
            'new_password': 'newpass123',
            'confirm_password': 'newpass123'
        })
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_confirm_password_reset_passwords_dont_match(self, client, test_user, mock_redis):
        """Test confirming password reset with mismatched passwords"""
        # First request a reset token
        request_url = reverse('password_reset_request')
        request_response = client.post(request_url, {'email': test_user.email})
        token = request_response.data['token']
        
        # Try to reset with mismatched passwords
        confirm_url = reverse('password_reset_confirm')
        response = client.post(confirm_url, {
            'token': token,
            'new_password': 'newpass123',
            'confirm_password': 'different123'
        })
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
