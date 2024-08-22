import pytest
from flask_testing import TestCase
from app import app, executor

class TestWeatherAPI(TestCase):
    def create_app(self):
        return app

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.cities_collection.drop()  # Clears the test collection before each test
        self.db = self.app.cities_collection

    def test_multiple_users(self):
        # Tests data collection for multiple users
        user_ids = [i for i in range(10)]
        for user_id in user_ids:
            print(f"USER: {user_id}")
            self.client.post('/weather', json={"user_id": user_id})

        # Waits 10 seconds to allow data collection
        import time
        time.sleep(10)  # Checks the progress for each user

        # Verifica o progresso para cada usuário
        for user_id in user_ids:
            response = self.client.get(f'/weather/{user_id}')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['user_id'], user_id)
            self.assertTrue('progress' in data)
            
        print(f"Connected to database: {self.app.config['MONGO_URI']}")
        print(self.app.cities_collection.count_documents({}))


if __name__ == '__main__':
    pytest.main()
