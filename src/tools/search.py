"""🔍 Example Search Tool - Demonstrates web search patterns.

Example implementation showing MCP tool structure with:
- API layer separation
- Mock search results for template purposes
- Rate limiting and validation patterns
- Structured error handling

Replace with real search API integration for production use.
"""

from __future__ import annotations

import logging
import random
import time
from typing import List
from urllib.parse import urlparse

from src.config import (
    SEARCH_DEFAULT_LIMIT,
    SEARCH_MAX_RESULTS,
    SEARCH_TIMEOUT,
)
from src.models import SearchQuery, SearchResponse, SearchResult
from src.api.web_search import WebSearchAPI

logger = logging.getLogger(__name__)


class SearchTool:
    """🔍 Example search tool demonstrating API integration patterns."""
    
    def __init__(self) -> None:
        """Initialize search tool with API layer separation."""
        self._initialized = False
        self._last_search_time = 0
        self._min_search_interval = 1.0  # Rate limiting
        self._search_api = WebSearchAPI()  # API layer separation
    
    def initialize(self) -> None:
        """🔧 Initialize example search tool and API layer."""
        if self._initialized:
            return
        
        logger.info("🔍 Initializing example search tool...")
        
        # Initialize API layer
        self._search_api.initialize()
        
        self._initialized = True
        logger.info("✅ Example search tool initialized (mock implementation)")
    
    def health_check(self) -> bool:
        """💚 Verify search tool is working correctly."""
        try:
            # Test API layer health
            return self._search_api.health_check()
        except Exception as e:
            logger.error(f"❌ Search health check failed: {e}")
            return False
    
    def search(
        self,
        text: str,
        domains: List[str] = None,
        limit: int = SEARCH_DEFAULT_LIMIT,
        language: str = "en"
    ) -> SearchResponse:
        """🔍 Perform web search with filtering and validation.
        
        Args:
            text: Search query text
            domains: Optional domain filters
            limit: Maximum number of results (1-100)
            language: Search language code
            
        Returns:
            SearchResponse: Structured search results
            
        Raises:
            ValueError: For invalid search parameters
            RuntimeError: For search service errors
        """
        if not self._initialized:
            self.initialize()
        
        start_time = time.time()
        
        # Validate inputs
        self._validate_search_params(text, domains, limit, language)
        
        # Rate limiting
        self._enforce_rate_limit()
        
        try:
            # Perform search (mock implementation - replace with real API)
            results = self._perform_search(text, domains, limit, language)
            
            search_time = time.time() - start_time
            
            logger.info(f"🔍 Search completed: '{text}' -> {len(results)} results ({search_time:.3f}s)")
            
            return SearchResponse(
                query=text,
                results=results,
                total_found=len(results),
                search_time=search_time
            )
            
        except Exception as e:
            logger.error(f"❌ Search failed for '{text}': {e}")
            raise RuntimeError(f"Search service error: {e}")
    
    def _validate_search_params(
        self,
        text: str,
        domains: List[str],
        limit: int,
        language: str
    ) -> None:
        """✅ Validate search parameters."""
        # Validate query text
        if not text or not text.strip():
            raise ValueError("Search text cannot be empty")
        
        if len(text) > 1000:
            raise ValueError("Search text too long (max 1000 characters)")
        
        # Validate limit
        if not isinstance(limit, int) or limit < 1:
            raise ValueError("Limit must be a positive integer")
        
        if limit > SEARCH_MAX_RESULTS:
            raise ValueError(f"Limit too high (max {SEARCH_MAX_RESULTS})")
        
        # Validate language
        if not isinstance(language, str) or len(language) < 2:
            raise ValueError("Language must be a valid language code")
        
        # Validate domains
        if domains:
            if len(domains) > 10:
                raise ValueError("Too many domain filters (max 10)")
            
            for domain in domains:
                if not self._is_valid_domain(domain):
                    raise ValueError(f"Invalid domain format: {domain}")
    
    def _is_valid_domain(self, domain: str) -> bool:
        """✅ Validate domain format."""
        if not domain or not domain.strip():
            return False
        
        # Basic domain validation
        if "." not in domain:
            return False
        
        # Check for valid characters
        allowed_chars = set("abcdefghijklmnopqrstuvwxyz0123456789.-")
        if not all(c.lower() in allowed_chars for c in domain):
            return False
        
        return True
    
    def _enforce_rate_limit(self) -> None:
        """⏱️ Enforce rate limiting between search requests."""
        current_time = time.time()
        time_since_last = current_time - self._last_search_time
        
        if time_since_last < self._min_search_interval:
            sleep_time = self._min_search_interval - time_since_last
            logger.debug(f"⏱️ Rate limiting: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)
        
        self._last_search_time = time.time()
    
    def _perform_search(
        self,
        text: str,
        domains: List[str],
        limit: int,
        language: str
    ) -> List[SearchResult]:
        """🔍 Perform search via API layer."""
        # Use API layer for search
        api_results = self._search_api.search(
            query=text,
            domains=domains,
            limit=limit,
            language=language
        )
        
        # Convert API results to SearchResult models
        search_results = []
        for api_result in api_results:
            result = SearchResult(
                title=api_result["title"],
                url=api_result["url"],
                snippet=api_result["snippet"],
                domain=api_result.get("domain", ""),
                relevance_score=api_result.get("relevance_score", 0.5)
            )
            search_results.append(result)
        
        return search_results