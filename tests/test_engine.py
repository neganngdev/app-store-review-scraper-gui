"""
Unit tests for the scraping engine.
"""

import unittest
from app.engine import fetch_app_info, fetch_app_reviews


class TestEngine(unittest.TestCase):
    """Test cases for engine.py functions."""

    def test_fetch_app_info_basic(self):
        """Test basic app info fetching."""
        # Using a well-known app ID for testing
        app_id = "com.google.android.youtube"
        result = fetch_app_info(app_id, lang="en", country="us")
        
        self.assertIsInstance(result, dict)
        self.assertIn("app_id", result)
        self.assertEqual(result["app_id"], app_id)

    def test_fetch_reviews_basic(self):
        """Test basic review fetching."""
        app_id = "com.google.android.youtube"
        result = fetch_app_reviews(app_id, count=5, lang="en", country="us")
        
        self.assertIsInstance(result, list)
        self.assertLessEqual(len(result), 5)

    def test_invalid_app_id(self):
        """Test handling of invalid app ID."""
        result = fetch_app_info("invalid.app.id.12345", lang="en", country="us")
        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()
