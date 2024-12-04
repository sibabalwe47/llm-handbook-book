from zenml import step
from typing import Annotated
from zenml.logger import get_logger

logger = get_logger(__name__)

@step
def crawl_links(
    user: str,
    links: list[str]
) -> str:
    """Crawls a user's links"""
    logger.info(f"Starting to crawl {len(links)} link(s).")
    return "LINK_CRAWLED"