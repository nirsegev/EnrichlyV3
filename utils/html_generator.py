import os
from datetime import datetime
from typing import List, Any
from utils.models import Recommendation
from utils.templates import generate_styles, generate_scripts

async def generate_html(
    chat_id: int,
    user_links: list,
    link_metadata: list,
    user_recommendations: List[Recommendation],
    first_name: str
) -> str:
    """Generate a mobile-friendly HTML file with link history and metadata."""
    print("generating html")
    directory = "/app/storage/links_history"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Extract all unique tags
    all_tags = sorted(
        set(tag for metadata in link_metadata for tag in metadata.get("tags", []))
    )

    def generate_tag_filters():
        # ... tag filters generation code ...
        pass

    def generate_bookmark_cards(chat_id):
        # ... bookmark cards generation code ...
        pass

    # Build HTML
    history_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{first_name}'s Bookmarks</title>
        {generate_styles()}
    </head>
    <body>
        <div class="container">
            {generate_tag_filters()}
            <div class="bookmarks">
                {generate_bookmark_cards(chat_id)}
            </div>
            <div class="actions">
                <button class="delete-all" onclick="deleteAllLinks()">Delete All Links</button>
                <button class="delete-active-tag" onclick="deleteActiveTag()">Delete Active Tag</button>
            </div>
        </div>
        {generate_scripts(chat_id)}
    </body>
    </html>
    """

    file_path = os.path.join(directory, f"{chat_id}_history.html")
    with open(file_path, "w") as file:
        file.write(history_html)
        print("saved html to file: ", file_path)

    return f"https://your-app-url.railway.app/storage/links_history/{chat_id}_history.html" 