"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
import pytest
from src import app
from src import status
from flask import jsonify

@pytest.fixture()
def client():
    """Fixture for Flask test client"""
    return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndpoints:
    """Test cases for Counter API"""

    def test_create_counter(self, client):
        """It should create a counter"""
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREATED

    # Generate 404 Error for non-existent counter - Ernesto Lara
    def test_non_existent_counter(self, client):
        # Create a counter
        client.post('/counters/foo')

        # Get counter
        result = client.get('/counters/notfoo')

        # Assert error 404
        assert result.status_code == status.HTTP_404_NOT_FOUND


    # Prevent duplicate counters - Tszchoi Siu
    def test_prevent_duplicate_counters(self, client):
        # Try to create the same counter again
        result = client.post("/counters/foo")
        assert result.status_code == status.HTTP_409_CONFLICT

    # Write Failing Test - Brian
    def test_read_counter(self, client):
        """It should read a counter"""
        # 1. Create a counter first (so we have something to read)
        client.post('/counters/foo')
        
        # 2. Read the counter
        result = client.get('/counters/foo')
        
        # 3. Assert valid return
        assert result.status_code == status.HTTP_200_OK
        assert result.get_json() == {"foo": 0}
    
    # Increment a counter - Donald Hunter
    def test_increment_a_counter(self,client):
        """It should increment a counter"""

        # LOCAL IMPORT to keep my changes inside this function and
        # avoid  name conflicts (foo)
        from src.counter import COUNTERS
        COUNTERS.clear() 
        
        # Create a counter
        client.post('/counters/foo')

        # Check the initial value is 0
        initial_res = client.get('/counters/foo')
        assert initial_res.get_json()['foo'] == 0

        # Increment the counter
        result = client.put('/counters/foo')
        assert result.status_code == status.HTTP_200_OK

        # Confirm counter is at 1
        assert result.get_json()['foo'] == 1

        # Reset to avoid name conflicts
        COUNTERS.clear()

    # Reset all counters - Alvaro
    def test_reset_all_counters(self, client):
        """It should reset all counters"""

        # LOCAL IMPORT to keep my changes inside this function and
        # avoid  name conflicts (foo, bar)
        from src.counter import COUNTERS
        COUNTERS.clear() 

        # step 1: Create two counters
        client.post('/counters/foo')
        client.post('/counters/bar')

        # step 2: Increment both counters to ensure they are not at 0
        client.put('/counters/foo')
        client.put('/counters/bar')

        # Step 3: Check that both counters are at 1
        # initial_res = client.get('/counters')
        # assert initial_res.get_json() == {"foo": 1, "bar": 1}

        # Step 4: Reset all counters
        client.post('/counters/reset')

        # Confirm both counters are reset to 0
        result = client.get('/counters')
        assert result.get_json() == {"foo": 0, "bar": 0}


@pytest.mark.usefixtures("client")
def test_list_all_counters(client):
    #test to list all of the counters

    client.post('/counters/foo')
    client.post('/counters/bar')

    result = client.get('/counters')

    assert result.status_code == status.HTTP_200_OK
    assert result.get_json() == {"foo": 0, "bar": 0}

