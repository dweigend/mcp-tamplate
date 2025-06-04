"""🔍 Search Tool - Web Search with Filtering and Validation.

Provides web search capabilities with domain filtering, result limits,
and structured responses. Includes rate limiting and error handling.

Features:
- Web search with configurable limits
- Domain filtering for targeted results
- Language support
- Relevance scoring
- Rate limiting protection
- Structured result formatting

Note: This is a template implementation. In production, integrate with
real search APIs like Google Custom Search, Bing Search, or others.

References:
- Search API integration patterns
- Rate limiting best practices
- Coding standards: Early returns, validation
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

logger = logging.getLogger(__name__)


class SearchTool:
    """🔍 Web search tool with filtering and validation."""
    
    def __init__(self) -> None:
        """Initialize search tool with rate limiting."""
        self._initialized = False
        self._last_search_time = 0
        self._min_search_interval = 1.0  # Minimum seconds between searches
        
        # Mock search data for template (replace with real API in production)
        self._mock_results = [
            {
                "title": "Python Official Documentation",
                "url": "https://docs.python.org/3/",
                "snippet": "The official Python documentation with tutorials, library reference, and more.",
                "domain": "docs.python.org"
            },
            {
                "title": "Real Python Tutorials", 
                "url": "https://realpython.com/",
                "snippet": "Learn Python programming with tutorials, courses, and community.",
                "domain": "realpython.com"
            },
            {
                "title": "Python Package Index (PyPI)",
                "url": "https://pypi.org/",
                "snippet": "Find and install Python packages from the Python Package Index.",
                "domain": "pypi.org"
            },
            {
                "title": "GitHub Python Projects",
                "url": "https://github.com/topics/python",
                "snippet": "Explore Python projects and repositories on GitHub.",
                "domain": "github.com"
            },
            {
                "title": "Stack Overflow Python Questions",
                "url": "https://stackoverflow.com/questions/tagged/python",
                "snippet": "Python programming questions and answers from the community.",
                "domain": "stackoverflow.com"
            }
        ]
    
    def initialize(self) -> None:
        """🔧 Initialize search tool."""
        if self._initialized:
            return
        
        # In production, initialize API clients here
        # Example: self.search_client = GoogleCustomSearchClient(api_key=API_KEY)
        
        self._initialized = True
        logger.info("🔍 Search tool initialized")
    
    def health_check(self) -> bool:
        """💚 Verify search tool is working correctly."""
        try:
            # Test search with minimal query
            test_query = SearchQuery(text="test", limit=1)
            result = self.search(
                text=test_query.text,
                domains=test_query.domains,
                limit=test_query.limit,
                language=test_query.language
            )
            
            return len(result.results) >= 0  # Even 0 results is OK for health check
            
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
        """🔍 Perform the actual search (mock implementation).
        
        NOTE: This is a mock implementation for template purposes.
        In production, replace with real search API integration.
        """
        # Simulate API call delay
        time.sleep(0.1 + random.uniform(0, 0.2))
        
        # Filter mock results based on query and domains
        filtered_results = []
        
        for mock_result in self._mock_results:
            # Simple text matching (in production, use search API)
            if self._matches_query(mock_result, text):
                # Apply domain filtering if specified
                if domains and not self._matches_domains(mock_result, domains):
                    continue
                
                # Convert to SearchResult model
                result = SearchResult(
                    title=mock_result["title"],
                    url=mock_result["url"],
                    snippet=mock_result["snippet"],
                    domain=mock_result["domain"],
                    relevance_score=self._calculate_relevance(mock_result, text)
                )
                
                filtered_results.append(result)
        
        # Sort by relevance score (descending)
        filtered_results.sort(key=lambda r: r.relevance_score or 0, reverse=True)
        
        # Apply limit
        return filtered_results[:limit]
    
    def _matches_query(self, result: dict, query: str) -> bool:
        """🎯 Check if result matches search query (simple implementation)."""
        query_lower = query.lower()
        title_lower = result["title"].lower()
        snippet_lower = result["snippet"].lower()
        
        # Simple keyword matching
        query_words = query_lower.split()
        text_content = f"{title_lower} {snippet_lower}"
        
        # Check if any query words appear in the content
        return any(word in text_content for word in query_words)
    
    def _matches_domains(self, result: dict, domains: List[str]) -> bool:
        """🌐 Check if result matches domain filters."""
        result_domain = result["domain"].lower()
        
        for domain_filter in domains:
            if domain_filter.lower() in result_domain:
                return True
        
        return False
    
    def _calculate_relevance(self, result: dict, query: str) -> float:
        """📊 Calculate relevance score for result (simple implementation)."""
        query_lower = query.lower()
        title_lower = result["title"].lower()
        snippet_lower = result["snippet"].lower()
        
        score = 0.0
        
        # Title matches get higher score
        if query_lower in title_lower:
            score += 0.8
        
        # Snippet matches get medium score
        if query_lower in snippet_lower:
            score += 0.4
        
        # Count word matches
        query_words = query_lower.split()
        title_words = set(title_lower.split())
        snippet_words = set(snippet_lower.split())
        
        # Word overlap scoring
        title_overlap = len(set(query_words) & title_words) / len(query_words)
        snippet_overlap = len(set(query_words) & snippet_words) / len(query_words)
        
        score += title_overlap * 0.6
        score += snippet_overlap * 0.2
        
        # Domain authority boost (mock implementation)
        domain = result["domain"]
        if domain in ["docs.python.org", "github.com", "stackoverflow.com"]:
            score += 0.1
        
        return min(score, 1.0)  # Cap at 1.0
    
    def get_search_info(self) -> dict:
        """ℹ️ Get information about search capabilities."""
        return {
            "max_results": SEARCH_MAX_RESULTS,
            "default_limit": SEARCH_DEFAULT_LIMIT,
            "timeout": SEARCH_TIMEOUT,
            "rate_limit_interval": self._min_search_interval,
            "supported_languages": ["en", "de", "es", "fr"],  # Example
            "max_domains": 10,
            "max_query_length": 1000
        }
    
    # =============================================================================
    # 🚀 PRODUCTION INTEGRATION TEMPLATES
    # =============================================================================
    
    def _integrate_google_search(self, query: str, **kwargs) -> List[dict]:
        """🚀 Template for Google Custom Search API integration.
        
        Replace the mock implementation with this pattern for production use.
        """
        # Example integration pattern:
        # 
        # from googleapiclient.discovery import build
        # 
        # service = build("customsearch", "v1", developerKey=API_KEY)
        # result = service.cse().list(
        #     q=query,
        #     cx=SEARCH_ENGINE_ID,
        #     num=kwargs.get('limit', 10),
        #     lr=f"lang_{kwargs.get('language', 'en')}",
        #     siteSearch=kwargs.get('domains', [])
        # ).execute()
        # 
        # return result.get('items', [])
        
        raise NotImplementedError("Google Search integration not implemented")
    
    def _integrate_bing_search(self, query: str, **kwargs) -> List[dict]:
        """🚀 Template for Bing Search API integration."""
        # Example integration pattern:
        #
        # import requests
        # 
        # headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
        # params = {
        #     "q": query,
        #     "count": kwargs.get('limit', 10),
        #     "mkt": kwargs.get('language', 'en-US')
        # }
        # 
        # response = requests.get(BING_SEARCH_URL, headers=headers, params=params)
        # response.raise_for_status()
        # 
        # return response.json().get('webPages', {}).get('value', [])
        
        raise NotImplementedError("Bing Search integration not implemented")