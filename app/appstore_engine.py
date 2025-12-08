"""
Apple App Store scraping engine using iTunes RSS Feed API.
This is the most reliable method as it uses Apple's official public RSS feeds.
"""

import requests
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_app_info(
    app_name: str,
    country: str = "us",
    app_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fetch basic information about an Apple App Store app.
    
    Args:
        app_name: The app's name or app ID (e.g., '284882215')
        country: Country code (default: 'us')
        app_id: Optional app ID if known
    
    Returns:
        Dictionary containing app information or error details
    """
    try:
        # Check if app_name is actually an app_id (numeric string)
        if app_name.isdigit():
            app_id = app_name
        
        if not app_id:
            return {
                "error": "App ID is required for App Store scraping",
                "app_name": app_name,
                "suggestion": "Find the numeric app ID from the App Store URL (e.g., '284882215' from apps.apple.com/app/facebook/id284882215)"
            }
        
        logger.info(f"Fetching App Store info for ID: {app_id}")
        
        # Fetch a small number of reviews to get app metadata
        url = f"https://itunes.apple.com/{country}/rss/customerreviews/id={app_id}/sortBy=mostRecent/json"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return {
                "error": f"Failed to fetch app info (HTTP {response.status_code})",
                "app_id": app_id
            }
        
        data = response.json()
        feed = data.get('feed', {})
        
        # First entry contains app info
        app_entry = feed.get('entry', [])[0] if feed.get('entry') else {}
        
        app_info = {
            "app_id": app_id,
            "app_name": app_entry.get('im:name', {}).get('label', 'N/A'),
            "country": country,
            "link": app_entry.get('link', {}).get('attributes', {}).get('href', 'N/A'),
            "icon": app_entry.get('im:image', [{}])[-1].get('label', 'N/A'),  # Get largest image
            "fetched_at": datetime.now().isoformat(),
            "method": "iTunes RSS Feed API"
        }
        
        logger.info(f"Successfully fetched App Store info for: {app_info['app_name']}")
        return app_info
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Network error: {str(e)}"
        logger.error(error_msg)
        return {
            "error": error_msg,
            "app_id": app_id or app_name
        }
    except Exception as e:
        error_msg = f"Error fetching App Store info: {str(e)}"
        logger.error(error_msg)
        return {
            "error": error_msg,
            "app_id": app_id or app_name
        }


def fetch_app_reviews(
    app_name: str,
    country: str = "us",
    count: int = 100,
    app_id: Optional[str] = None,
    sort: str = "mostRecent",
    text_only: bool = False
) -> List[Dict[str, Any]]:
    """
    Fetch user reviews for an Apple App Store app using iTunes RSS Feed.
    
    Args:
        app_name: The app's name or app ID (e.g., '284882215')
        country: Country code (default: 'us')
        count: Maximum number of reviews to fetch (default: 100, max: 500)
        app_id: Optional app ID if known
        sort: Sort order - 'mostRecent' or 'mostHelpful' (default: 'mostRecent')
        text_only: If True, only return reviews with text/comments (default: False)
    
    Returns:
        List of dictionaries containing review data, or list with error dict
    """
    try:
        # Check if app_name is actually an app_id (numeric string)
        if app_name.isdigit():
            app_id = app_name
        
        if not app_id:
            return [{
                "error": "App ID is required for App Store scraping",
                "app_name": app_name,
                "suggestion": "Find the numeric app ID from the App Store URL (e.g., '284882215' for Facebook)"
            }]
        
        logger.info(f"Fetching {count} App Store reviews for ID: {app_id}")
        
        # iTunes RSS Feed supports up to 500 reviews
        # The feed is paginated - we'll fetch the first page
        max_count = min(count, 500)
        
        # Map sort options
        sort_by = "mostRecent" if sort == "mostRecent" else "mostHelpful"
        
        # Build URL
        url = f"https://itunes.apple.com/{country}/rss/customerreviews/id={app_id}/sortBy={sort_by}/json"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return [{
                "error": f"Failed to fetch reviews (HTTP {response.status_code})",
                "app_id": app_id
            }]
        
        data = response.json()
        entries = data.get('feed', {}).get('entry', [])
        
        # First entry is app info, rest are reviews
        review_entries = entries[1:] if len(entries) > 1 else []
        
        if not review_entries:
            return [{
                "error": "No reviews found for this app",
                "app_id": app_id,
                "note": "The app may not have any reviews yet, or reviews may be disabled."
            }]
        
        # Parse reviews
        reviews = []
        for entry in review_entries[:max_count]:
            review_text = entry.get('content', {}).get('label', '')
            
            # Skip reviews without text if text_only is enabled
            if text_only and not review_text.strip():
                continue
            
            review_info = {
                "review_id": entry.get('id', {}).get('label', ''),
                "user_name": entry.get('author', {}).get('name', {}).get('label', 'Anonymous'),
                "rating": entry.get('im:rating', {}).get('label', 'N/A'),
                "date": entry.get('updated', {}).get('label', ''),
                "title": entry.get('title', {}).get('label', ''),
                "text": review_text,
                "version": entry.get('im:version', {}).get('label', 'N/A'),
                "vote_sum": entry.get('im:voteSum', {}).get('label', '0'),
                "vote_count": entry.get('im:voteCount', {}).get('label', '0'),
            }
            reviews.append(review_info)
        
        logger.info(f"Successfully fetched {len(reviews)} App Store reviews" + (" (text only)" if text_only else ""))
        return reviews
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Network error: {str(e)}"
        logger.error(error_msg)
        return [{
            "error": error_msg,
            "app_id": app_id or app_name
        }]
    except Exception as e:
        error_msg = f"Error fetching App Store reviews: {str(e)}"
        logger.error(error_msg)
        return [{
            "error": error_msg,
            "app_id": app_id or app_name
        }]


def fetch_reviews_multi_country(
    app_name: str,
    countries: List[str] = None,
    count_per_country: int = 100,
    app_id: Optional[str] = None,
    sort: str = "mostRecent",
    text_only: bool = False
) -> List[Dict[str, Any]]:
    """
    Fetch reviews from multiple countries to get more comprehensive data.
    
    Args:
        app_name: The app's name or app ID
        countries: List of country codes (default: ['us', 'gb', 'ca', 'au', 'de', 'fr', 'jp', 'kr'])
        count_per_country: Number of reviews to fetch per country (default: 100)
        app_id: Optional app ID if known
        sort: Sort order (default: 'mostRecent')
        text_only: If True, only return reviews with text/comments (default: False)
    
    Returns:
        Combined list of reviews from all countries (duplicates removed by review_id)
    """
    if countries is None:
        countries = ['us', 'gb', 'ca', 'au', 'de', 'fr', 'jp', 'kr']
    
    all_reviews = []
    seen_review_ids = set()
    
    logger.info(f"Fetching App Store reviews from {len(countries)} countries for: {app_name}")
    
    for country in countries:
        try:
            logger.info(f"Fetching from country: {country}")
            reviews = fetch_app_reviews(
                app_name=app_name,
                country=country,
                count=count_per_country,
                app_id=app_id,
                sort=sort,
                text_only=text_only
            )
            
            # Skip if error
            if reviews and isinstance(reviews, list) and "error" in reviews[0]:
                logger.warning(f"No reviews from {country}")
                continue
            
            # Add unique reviews
            for review in reviews:
                review_id = review.get("review_id")
                if review_id and review_id not in seen_review_ids:
                    seen_review_ids.add(review_id)
                    review["fetched_from_country"] = country
                    all_reviews.append(review)
        
        except Exception as e:
            logger.warning(f"Error fetching from {country}: {str(e)}")
            continue
    
    logger.info(f"Total unique App Store reviews fetched: {len(all_reviews)}")
    return all_reviews


def validate_app_name(app_name: str) -> bool:
    """
    Validate if an app name/ID is in a reasonable format.
    
    Args:
        app_name: The app's name or ID to validate
    
    Returns:
        True if valid format, False otherwise
    """
    if not app_name or not isinstance(app_name, str):
        return False
    
    # Basic validation: should not be empty and should be reasonable length
    if len(app_name.strip()) < 2:
        return False
    
    return True
