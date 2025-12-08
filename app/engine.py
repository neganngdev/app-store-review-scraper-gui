"""
Google Play Store scraping engine.
Handles all data fetching operations using gplay-scraper.
"""

from gplay_scraper import GPlayScraper
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global scraper instance using curl_cffi for better reliability
scraper = GPlayScraper(http_client="curl_cffi")


def fetch_app_info(
    app_id: str,
    lang: str = "en",
    country: str = "us"
) -> Dict[str, Any]:
    """
    Fetch detailed information about a Google Play Store app.
    
    Args:
        app_id: The app's package name (e.g., 'com.instagram.android')
        lang: Language code (default: 'en')
        country: Country code (default: 'us')
    
    Returns:
        Dictionary containing app information or error details
    """
    try:
        logger.info(f"Fetching app info for: {app_id}")
        
        # Fetch app details from Google Play Store using app_analyze method
        result = scraper.app_analyze(
            app_id=app_id,
            lang=lang,
            country=country
        )
        
        if not result:
            return {
                "error": "No data returned",
                "app_id": app_id
            }
        
        # Extract and structure the most relevant information
        # Note: gplay-scraper uses camelCase for field names
        app_info = {
            "app_id": result.get("appId", app_id),
            "title": result.get("title", "N/A"),
            "developer": result.get("developer", "N/A"),
            "developer_id": result.get("developerId"),
            "icon": result.get("icon"),
            "rating": result.get("score"),
            "ratings_count": result.get("ratings"),
            "reviews_count": result.get("reviews"),
            "installs": result.get("minInstalls"),
            "price": result.get("price"),
            "currency": result.get("currency"),
            "description": result.get("description"),
            "summary": result.get("summary"),
            "released": result.get("released"),
            "last_updated": result.get("updated"),
            "version": result.get("version"),
            "category": result.get("genre"),
            "content_rating": result.get("contentRating"),
            "url": result.get("url"),
        }
        
        logger.info(f"Successfully fetched info for: {app_info['title']}")
        return app_info
        
    except Exception as e:
        error_msg = f"Error fetching app info: {str(e)}"
        logger.error(error_msg)
        return {
            "error": error_msg,
            "app_id": app_id
        }


def fetch_app_reviews(
    app_id: str,
    count: int = 100,
    lang: str = "en",
    country: str = "us",
    sort: str = "newest",
    text_only: bool = False
) -> List[Dict[str, Any]]:
    """
    Fetch user reviews for a Google Play Store app.
    
    Args:
        app_id: The app's package name (e.g., 'com.instagram.android')
        count: Maximum number of reviews to fetch (default: 100)
        lang: Language code (default: 'en')
        country: Country code (default: 'us')
        sort: Sort order - 'newest', 'rating', or 'helpfulness' (default: 'newest')
        text_only: If True, only return reviews with text/comments (default: False)
    
    Returns:
        List of dictionaries containing review data, or list with error dict
    """
    try:
        logger.info(f"Fetching {count} reviews for: {app_id}")
        
        # Map sort parameter to gplay-scraper format (uses uppercase strings)
        sort_mapping = {
            "newest": "NEWEST",
            "rating": "RATING",
            "helpfulness": "RELEVANT"
        }
        sort_value = sort_mapping.get(sort.lower(), "NEWEST")
        
        # Fetch reviews from Google Play Store using reviews_analyze method
        reviews_data = scraper.reviews_analyze(
            app_id=app_id,
            lang=lang,
            country=country,
            count=count,
            sort=sort_value
        )
        
        if not reviews_data:
            return [{
                "error": "No reviews found",
                "app_id": app_id
            }]
        
        # Structure the review data
        # Note: gplay-scraper uses camelCase for field names
        reviews = []
        for review in reviews_data:
            review_text = review.get("text")
            
            # Skip reviews without text if text_only is enabled
            if text_only and not review_text:
                continue
            
            review_info = {
                "review_id": review.get("reviewId"),
                "user_name": review.get("userName"),
                "user_image": review.get("userImage"),
                "rating": review.get("score"),
                "date": review.get("date"),
                "text": review_text,
                "thumbs_up": review.get("thumbsUp", 0),
                "app_version": review.get("appVersion"),
                "reply_text": review.get("replyText"),
                "reply_date": review.get("replyDate"),
            }
            reviews.append(review_info)
        
        logger.info(f"Successfully fetched {len(reviews)} reviews" + (" (text only)" if text_only else ""))
        return reviews
        
    except Exception as e:
        error_msg = f"Error fetching reviews: {str(e)}"
        logger.error(error_msg)
        return [{
            "error": error_msg,
            "app_id": app_id
        }]


def fetch_reviews_multi_country(
    app_id: str,
    countries: List[str] = None,
    count_per_country: int = 100,
    lang: str = "en",
    sort: str = "newest",
    text_only: bool = False
) -> List[Dict[str, Any]]:
    """
    Fetch reviews from multiple countries to get more comprehensive data.
    
    Args:
        app_id: The app's package name
        countries: List of country codes (default: ['us', 'kr', 'jp', 'gb', 'de', 'fr'])
        count_per_country: Number of reviews to fetch per country (default: 100)
        lang: Language code (default: 'en')
        sort: Sort order (default: 'newest')
        text_only: If True, only return reviews with text/comments (default: False)
    
    Returns:
        Combined list of reviews from all countries (duplicates removed by review_id)
    """
    if countries is None:
        countries = ['us', 'kr', 'jp', 'gb', 'de', 'fr', 'in', 'br']
    
    all_reviews = []
    seen_review_ids = set()
    
    logger.info(f"Fetching reviews from {len(countries)} countries for: {app_id}")
    
    for country in countries:
        try:
            logger.info(f"Fetching from country: {country}")
            reviews = fetch_app_reviews(
                app_id=app_id,
                count=count_per_country,
                lang=lang,
                country=country,
                sort=sort,
                text_only=text_only
            )
            
            # Skip if error
            if reviews and isinstance(reviews, list) and "error" in reviews[0]:
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
    
    logger.info(f"Total unique reviews fetched: {len(all_reviews)}")
    return all_reviews


def validate_app_id(app_id: str) -> bool:
    """
    Validate if an app ID is in the correct format.
    
    Args:
        app_id: The app's package name to validate
    
    Returns:
        True if valid format, False otherwise
    """
    if not app_id or not isinstance(app_id, str):
        return False
    
    # Basic validation: should contain at least one dot and only valid characters
    parts = app_id.split(".")
    if len(parts) < 2:
        return False
    
    # Check if all parts contain valid characters (alphanumeric and underscore)
    for part in parts:
        if not part or not all(c.isalnum() or c == "_" for c in part):
            return False
    
    return True
