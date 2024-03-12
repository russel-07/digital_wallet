import pytest


class TestUser:

    @pytest.mark.django_db(transaction=True)
    def test_success_create_user(self, client):
        data = {'username': 'test_user', 'password': 'test_password'}
        response = client.post('/api/v1/user/', data=data)
        assert response.status_code == 201, 'Новый пользователь не создан.'

    @pytest.mark.django_db(transaction=True)
    def test_failed_create_user_with_simple_password(self, client):
        data = {'username': 'test_user', 'password': '123'}
        response = client.post('/api/v1/user/', data=data)
        assert response.status_code == 400, \
            'Создан пользователь с простым паролем.'
