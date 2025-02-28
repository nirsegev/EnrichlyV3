import requests
from bs4 import BeautifulSoup
import os
from .models import ProductData
from config import get_settings

async def fetch_opengraph_metadata(link: str) -> ProductData:
    """Fallback: Fetch OpenGraph metadata."""
    print("Using OpenGraph metadata extraction.")
    settings = get_settings()
    headers = {"X-SOAX-API-Secret": settings.X_SOAX_API_SECRET}
    print("headers: ", headers)
    soax_unblocker_link = (
        f"https://scraping.soax.com/v1/unblocker/html?xhr=false&url={link}"
    )
    try:
        response = requests.get(soax_unblocker_link, headers=headers, timeout=60)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return extract_opengraph_tags(soup, link)
    except requests.exceptions.RequestException as e:
        print(f"OpenGraph extraction error: {e}")
        return ProductData(
            title="No title found",
            description="No description found",
            images=[],
            url=link,
            site_name="Unknown site name"
        )

def extract_opengraph_tags(soup: BeautifulSoup, link: str) -> ProductData:
    """Extract OpenGraph metadata from the page."""
    print("extract_opengraph_tags")

    def get_meta(property_name: str) -> str:
        # Handle case insensitivity and attribute variations
        tag = soup.find("meta", attrs={"property": property_name})
        if not tag:  # Try name attribute as a fallback
            tag = soup.find("meta", attrs={"name": property_name})
        return tag["content"] if tag and "content" in tag.attrs else None

    return ProductData(
        title=get_meta("og:title") or "No title found",
        description=get_meta("og:description") or "No description found",
        url=get_meta("og:url") or link,
        images=[get_meta("og:image")] if get_meta("og:image") else [],
        site_name=get_meta("og:site_name") or "Unknown site name"
    ) 