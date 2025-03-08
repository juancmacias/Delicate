import pytest

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Configure the test environment to handle the 'type' table name issue.
    This changes the table name only during test execution.
    """
    # Import the Type model
    from delicate_apps.type.models import Type
    
    # Store the original db_table value
    original_db_table = Type._meta.db_table
    
    # Change the table name temporarily
    Type._meta.db_table = 'commerce_type'
    
    # Let the tests run
    yield
    
    # Restore the original table name
    Type._meta.db_table = original_db_table