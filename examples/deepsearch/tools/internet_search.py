"""
Tools for searching the web using Linkup and Tavily.
"""

import asyncio
import logging
import random

from dotenv import load_dotenv
from linkup import LinkupClient
from strands import tool
from strands_tools import tavily

load_dotenv()

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)


@tool
def linkup_search(query: str) -> str:
    """Search the web using Linkup
    Args:
        query: The query to search for
    Returns:
        The search results
    """
    client = LinkupClient()

    response = client.search(
        query=query,
        depth="standard",
        output_type="sourcedAnswer",
        include_images=False,
        include_inline_citations=False,
    )

    return str(response)


@tool
def internet_search(query: str) -> str:
    """Search the web using the internet
    Args:
        query: The query to search for
    Returns:
        The search results
    """
    internet_tools = [
        "linkup_search",
        # "tavily_search", # If you have tavily credits, you can use it here
        # Add your favorite internet tools here
    ]
    selected_tool = random.choice(internet_tools)
    logger.debug(f"Using tool: {selected_tool}")
    if selected_tool == "linkup_search":
        return linkup_search(query=query)
    if selected_tool == "tavily_search":
        return asyncio.run(tavily.tavily_search(query=query))


if __name__ == "__main__":
    print(internet_search(query="What is the capital of France?"))
