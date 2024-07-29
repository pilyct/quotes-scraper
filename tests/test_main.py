import pytest
import requests
from unittest.mock import patch, MagicMock
import pandas as pd
from main import get_author_details, page_scraping, connect_to_db, save_to_db

# Mock environment variables
@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv('USERNAME', 'testuser')
    monkeypatch.setenv('PASSWORD', 'testpassword')
    monkeypatch.setenv('HOST', 'localhost')
    monkeypatch.setenv('PORT', '5432')
    monkeypatch.setenv('DATABASE', 'testdb')

# Test database connection
def test_connect_to_db(mock_env):
    try:
        connect_to_db()
    except Exception:
        pytest.fail("connect_to_db() raised an exception")

# Mock to_sql method for save_to_db
@patch('main.pd.DataFrame.to_sql')
def test_save_to_db(mock_to_sql, mock_env):
    df = pd.DataFrame({
        'quote': ['Quote'],
        'author': ['Author'],
        'tags': ['tag1, tag2'],
        'born_date': ['Born Date'],
        'born_location': ['Born Location'],
        'demainion': ['Demainion']
    })
    
    try:
        save_to_db(df)
        mock_to_sql.assert_called_once()
    except Exception:
        pytest.fail("save_to_db() raised an exception")

# Mock requests.get for get_author_details
@patch('main.requests.get')
def test_get_author_details(mock_get):
    print("Starting test_get_author_details")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = """
    <div class="author-details">
        <h3 class="author-title">Author Name</h3>
        <span class="author-born-date">Born Date</span>
        <span class="author-born-location">Born Location</span>
        <div class="author-description">Description</div>
    </div>
    """
    mock_get.return_value = mock_response
    
    author_info = get_author_details('author-url')
    assert author_info == {
        'author': 'Author Name',
        'born_date': 'Born Date',
        'born_location': 'Born Location',
        'description': 'Description'
    }
    print("Finished test_get_author_details")

# Mock requests.get for get_author_details_missing_elemets
@patch('main.requests.get')
def test_get_author_details_missing_elements(mock_get):
    print("Starting test_get_author_details_missing_elements")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = """
    <div class="author-details">
        <h3 class="author-title">Author Name</h3>
        <!-- Missing other elements -->
    </div>
    """
    mock_get.return_value = mock_response
    
    author_info = get_author_details('author-url')
    assert author_info == {
        'author': 'Author Name',
        'born_date': 'Unknown',
        'born_location': 'Unknown',
        'description': 'No description'
    }
    print("Finished test_get_author_details_missing_elements")


# Mock requests.get for page_scraping
@patch('main.requests.get')
def test_page_scraping(mock_get):
    # Mock response for first page
    mock_response_first_page = MagicMock()
    mock_response_first_page.status_code = 200
    mock_response_first_page.text = """
    <div class="quote">
        <span class="text">Quote text</span>
        <small class="author">Author Name</small>
        <a class="tag">tag1</a>
        <a class="tag">tag2</a>
    </div>
    """
    # Mock response for subsequent pages
    mock_response_no_more_pages = MagicMock()
    mock_response_no_more_pages.status_code = 200
    mock_response_no_more_pages.text = ""

    mock_get.side_effect = [mock_response_first_page, mock_response_no_more_pages]

    with patch('main.get_author_details') as mock_get_author_details:
        mock_get_author_details.return_value = {
            'author': 'Author Name',
            'born_date': 'Born Date',
            'born_location': 'Born Location',
            'description': 'Description'
        }
        df = page_scraping()
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert len(df) == 1  # Ensure we only got one quote


