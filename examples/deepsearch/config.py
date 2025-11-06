"""
Configuration for DeepSearch agent rate limiting and concurrency.

API Rate Limit: 10 queries per second
- Theoretical minimum: 0.1s between calls (100ms)
- Safe minimum with margin: 0.15s between calls (6.67 queries/sec)
- Conservative with overhead: 0.2s between calls (5 queries/sec)
"""

# Rate limiting configuration for API calls
RATE_LIMIT_CONFIG = {
    # Minimum seconds between API calls
    # Set to 0.15s for safe operation under 10 QPS limit
    # Adjust based on actual performance:
    # - 0.1s = theoretical max (10 QPS)
    # - 0.15s = safe with 33% margin (6.67 QPS)
    # - 0.2s = conservative with overhead (5 QPS)
    "min_time_between_calls": 0.15,
    # Maximum retry attempts for failed API calls
    "max_retries": 3,
    # Initial backoff time for retries (doubles each retry)
    "initial_backoff_seconds": 1,
    # Maximum concurrent subagents allowed
    # With 10 QPS limit and 0.15s throttle, you can safely run 4-6 subagents in parallel
    "max_concurrent_subagents": 4,
}

# Search tool configuration
SEARCH_CONFIG = {
    "depth": "standard",
    "output_type": "sourcedAnswer",
    "include_images": False,
    "include_inline_citations": False,
}
