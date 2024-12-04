from zenml import pipeline
from zenml.logger import get_logger
from steps.etl import crawl_links, get_or_create_user

logger = get_logger(__name__)

@pipeline
def digital_data_etl(
    user_full_name: str, 
    links: list[str]
) -> str:
    """Loads user data using links and a user's full name."""

    user = get_or_create_user(user_full_name)

    last_step = crawl_links(user=user, links=links)

    return last_step