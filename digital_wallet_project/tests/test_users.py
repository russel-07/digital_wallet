import pytest


class TestUser:

    @pytest.mark.django_db(transaction=True)
    def test_success_create_user(self, client, user_url,
                                 post_success_user_data):
        response = client.post(user_url, data=post_success_user_data)
        assert response.status_code == 201

    @pytest.mark.django_db(transaction=True)
    def test_failed_create_user_with_simple_password(
            self, client, user_url, post_failed_user_data):
        response = client.post(user_url, data=post_failed_user_data)
        assert response.status_code == 400
