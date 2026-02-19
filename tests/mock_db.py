from app.utils.db_populate import user_dict,bill_dict,group_dict
import pytest

@pytest.fixture
def mock_user_db():
    return user_dict