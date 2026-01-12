import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestAPIEndpoints:
    """Tests para endpoints de la API"""
    
    def test_list_algorithms(self, client):
        response = client.get('/api/algorithms')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
        assert 'algorithms' in data
    
    def test_run_algorithm(self, client):
        response = client.post('/api/run', json={
            'algorithm': 'bubble_sort',
            'data': [3, 1, 4, 1, 5, 9, 2, 6]
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
        assert 'result' in data
    
    def test_run_algorithm_missing_data(self, client):
        response = client.post('/api/run', json={
            'algorithm': 'bubble_sort'
        })
        assert response.status_code == 400
    
    def test_run_algorithm_invalid(self, client):
        response = client.post('/api/run', json={
            'algorithm': 'nonexistent',
            'data': [1, 2, 3]
        })
        assert response.status_code == 400
    
    def test_generate_data(self, client):
        response = client.post('/api/generate', json={
            'type': 'random',
            'size': 10
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
        assert len(data['data']) == 10
    
    def test_compare_algorithms(self, client):
        response = client.post('/api/compare', json={
            'algorithms': ['bubble_sort', 'merge_sort'],
            'data': [3, 1, 4, 1, 5, 9, 2, 6]
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
        assert 'results' in data
    
    def test_get_history(self, client):
        response = client.get('/api/history')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] == True
        assert 'history' in data

class TestWebPages:
    """Tests para páginas web"""
    
    def test_index_page(self, client):
        response = client.get('/')
        assert response.status_code == 200
    
    def test_compare_page(self, client):
        response = client.get('/compare')
        assert response.status_code == 200
