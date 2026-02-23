from app.utils.db_populate import user_dict,bill_dict,group_dict
import pytest

@pytest.fixture
def mock_user_db():
    return user_dict

@pytest.fixture
def mock_bill_db():
    return bill_dict