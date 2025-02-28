# Standard library imports
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

# Third-party imports
from collections import defaultdict
from fastapi import HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
import requests

# Pydantic models for data validation
from pydantic import BaseModel

class Recommendation(BaseModel):
    destination_tag: str
    title: str
    link: str

class UserAnalysis(BaseModel):
    general: str
    recommendations: List[Recommendation]

# Global variables
user_links = defaultdict(list)
link_metadata = defaultdict(list)
pending_tags = {}
link_mapping = {}

async def view_summary(file_name: str) -> List[Recommendation]:
    """Serve a saved summary file as HTML."""
    file_path = os.path.join("/app/storage/links_history", file_name)
    try:
        with open(file_path, "r") as file:
            content = file.read()
            cleaned_json = clean_json_string(content)
            analysis = parse_analysis_from_json(cleaned_json)

            return analysis.recommendations
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Summary file not found.")

async def _generate_and_send_html(chat_id: int, first_name: str) -> str:
    """Generate HTML and return the URL for the user's link list."""
    print("_generate_and_send_html")
    # Note: You'll need to adapt this part based on your database setup
    user_links = []  # Replace with your database query
    link_metadata = [
        {
            "title": link.title,
            "description": link.description,
            "url": link.url,
            "price": link.price,
            "images": link.images if isinstance(link.images, list) else 
                     (link.images.split(",") if link.images else []),
            "site_name": link.site_name,
            "tags": [tag.name for tag in link.tags],
            "created_at": link.created_at,
        }
        for link in user_links
    ]
    return await generate_html(
        chat_id,
        user_links,
        link_metadata,
        await view_summary("995527624_summary.json"),
        first_name,
    )

async def send_message_with_buttons(chat_id: int, text: str, buttons: dict):
    """Send a message with inline keyboard buttons."""
    url = os.getenv("TELEGRAM_API_URL") + "sendMessage"
    payload = {"chat_id": chat_id, "text": text, "reply_markup": buttons}

    print(
        "send message with buttons: ",
        text,
        " with buttons: ",
        buttons,
        " to chat: ",
        chat_id,
    )

    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

def clean_json_string(raw_json: str) -> str:
    """Cleans a JSON string by removing the ```json prefix and ``` suffix if present."""
    raw_json = raw_json.strip()
    if raw_json.startswith("```json"):
        raw_json = raw_json[len("```json"):].strip()
    if raw_json.endswith("```"):
        raw_json = raw_json[:-len("```")].strip()
    return raw_json

def parse_analysis_from_json(json_data: str) -> UserAnalysis:
    try:
        data = json.loads(json_data)
        return UserAnalysis(
            general=data.get("general", ""),
            recommendations=[
                Recommendation(**rec)
                for rec in data.get("recommendations", [])
            ]
        )
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        return UserAnalysis(general="Error in parsing", recommendations=[])

async def regenerate_html(chat_id: int):
    # Note: Adapt this to your database setup
    user_links = []  # Replace with your database query
    link_metadata = [
        {
            "title": link.title,
            "description": link.description,
            "url": link.url,
            "price": link.price,
            "images": link.images if isinstance(link.images, list) else 
                     (link.images.split(",") if link.images else []),
            "site_name": link.site_name,
            "tags": [t.name for t in link.tags],
            "created_at": link.created_at,
        }
        for link in user_links
    ]
    await generate_html(
        chat_id,
        user_links,
        link_metadata,
        await view_summary("995527624_summary.json"),
        first_name="User",
    )

async def send_message(chat_id: int, text: str):
    url = os.getenv("TELEGRAM_API_URL") + "sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    print("send message: ", text, " to chat: ", chat_id)
    
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

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

    def generate_styles():
        return """
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
                color: #333;
            }
            .container {
                padding: 16px;
            }
            .profile {
                margin-bottom: 16px;
                text-align: center;
            }
            .profile h2 {
                margin: 0;
                font-size: 24px;
                color: #2c3e50;
            }
            .filters {
                margin-bottom: 16px;
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                justify-content: center;
            }
            .filter {
                background-color: #e0f7fa;
                color: #00796b;
                padding: 6px 12px;
                font-size: 0.9rem;
                border-radius: 12px;
                cursor: pointer;
                user-select: none;
            }
            .filter.active {
                background-color: #00796b;
                color: #ffffff;
            }
            .bookmarks {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 16px;
            }
            .bookmark {
                background-color: #fff;
                padding: 16px;
                display: flex;
                align-items: flex-start;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                transition: transform 0.2s;
                position: relative;
            }
            .bookmark:hover {
                transform: translateY(-5px);
            }
            .bookmark img {
                width: 70px;
                height: 70px;
                object-fit: cover;
                border-radius: 4px;
                margin-right: 12px;
                border: 1px solid #ddd;
            }
            .bookmark-content {
                flex: 1;
            }
            .bookmark h3 {
                font-size: 1rem;
                color: #3498db;
                margin: 0;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: normal;
                word-wrap: break-word;
                max-width: 100%;
            }
            .bookmark h3 a {
                text-decoration: none;
                color: inherit;
            }
            .bookmark h3 a:hover {
                text-decoration: underline;
            }
            .bookmark p {
                font-size: 0.9rem;
                color: #555;
                margin: 8px 0 0;
            }
            .price {
                font-weight: bold;
                color: #27ae60;
                margin-top: 8px;
            }
            .tags {
                margin-top: 8px;
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
            }
            .tag {
                background-color: #e0f7fa;
                color: #00796b;
                padding: 4px 8px;
                font-size: 0.8rem;
                border-radius: 12px;
                display: inline-block;
            }
            .add-tag {
                background-color: #d4edda;
                color: #155724;
                padding: 4px 8px;
                font-size: 0.8rem;
                border-radius: 12px;
                cursor: pointer;
                border: 1px solid #c3e6cb;
            }
            .delete-link {
                position: absolute;
                bottom: 8px;
                left: 8px;
                color: #b00;
                padding: 4px 8px;
                font-size: 0.8rem;
                cursor: pointer;
            }
            .delete-all {
                background-color: #f8d7da;
                color: #721c24;
                padding: 10px 20px;
                border: 1px solid #f5c6cb;
                border-radius: 8px;
                cursor: pointer;
                margin-top: 16px;
                display: block;
                text-align: center;
            }
            .delete-all:hover {
                background-color: #f5c6cb;
            }
            .delete-active-tag {
                background-color: #f8d7da;
                color: #721c24;
                padding: 10px 20px;
                border: 1px solid #f5c6cb;
                border-radius: 8px;
                cursor: pointer;
                margin-top: 16px;
                display: inline-block;
                text-align: center;
            }
            .delete-active-tag:hover {
                background-color: #f5c6cb;
            }

        </style>
        """

    def generate_tag_filters():
        filters_html = '<div class="filters">'
        filters_html += '<span class="filter active" data-tag="all" onclick="filterByTag(\'all\')">All</span>'
        for tag in all_tags:
            filters_html += f'<span class="filter" data-tag="{tag}" onclick="filterByTag(\'{tag}\')">{tag}</span>'
        filters_html += "</div>"
        return filters_html

    def generate_bookmark_cards(chat_id):
        cards_html = ""
        current_time = datetime.now()

        for link, metadata in zip(user_links, link_metadata):
            # Handle images
            images = metadata.get("images", [])
            image_html = f'<img src="{images[0]}" alt="Image">' if images else ""

            # Format price if available
            price = metadata.get("price", None)
            price_html = (
                f'<p class="price">Price: ${price}</p>'
                if price and price != "N/A"
                else ""
            )

            # Handle tags
            tags = metadata.get("tags", [])
            tags_html = (
                '<div class="tags">'
                + f'<span class="add-tag" onclick="openTagDialog({link.id})">+</span>'
                + "".join(
                    [
                        f'<span class="tag" onclick="deleteTagFromLink({link.id}, \'{tag}\')">{tag}</span>'
                        for tag in tags
                    ]
                )
                + "</div>"
            )

            # Format creation time
            created_at = metadata.get("created_at")
            created_at_html = ""
            if created_at:
                days_difference = (current_time - created_at).days
                formatted_time = (
                    created_at.strftime("%d/%m/%y %H:%M")
                    if days_difference == 0
                    else created_at.strftime("%d/%m/%y")
                    if days_difference == 1
                    else f"{days_difference} days ago"
                )
                created_at_html = f'<p style="text-align: right; font-size: 0.8rem; color: #888;">{formatted_time}</p>'

            # Handle title safely
            title = metadata.get("title", "Untitled") or "Untitled"
            title = title[:100]  # Ensure it's a string and slice it safely

            # Add pencil button if the title is "No title found"
            edit_button_html = ""
            if title == "No title found":
                edit_button_html = f"""
                <button onclick="editTitle({link.id})" style="
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    background: none;
                    border: none;
                    color: #3498db;
                    font-size: 1.2rem;
                    cursor: pointer;">
                    ✏️
                </button>
                """

            # Generate bookmark card
            tags_attr = "|".join(tags)  # Use pipe "|" as delimiter
            cards_html += f"""
            <div class="bookmark" data-tags="{tags_attr}" data-id="{link.id}">
                {image_html}
                <div class="bookmark-content">
                    <h3><a href="{metadata.get("url", link.link)}" target="_blank">{title}</a></h3> {edit_button_html}
                    <p>{(metadata.get("description") or "")[:200] + ("..." if metadata.get("description") and len(metadata.get("description")) > 200 else "")}</p>
                    {price_html}
                    {tags_html}
                    {created_at_html}
                </div>
                <span class="delete-link" onclick="deleteLink({link.id})">🗑️</span>
            </div>
            """

        # Add AI-generated recommendation cards
        for recommendation in user_recommendations:
            print("Adding recomendation card", recommendation)
            destination_tag = recommendation.destination_tag
            cards_html += f"""
            <div class="bookmark" data-tags="{destination_tag}" style="background-color: #e8d8f8; border-left: 4px solid #6a1b9a;">
                <div class="bookmark-content">
                    <h3><a href="{recommendation.link}" target="_blank">{recommendation.title}</a></h3>
                    <p style="font-size: 0.9rem; color: #444;">Recommended for tag: {destination_tag}</p>
                </div>
            </div>
            """

        return cards_html

    def generate_scripts(chat_id):
        return f"""
        <script>
            const chatId = "{chat_id}";

            // Define filterByTag function
            function filterByTag(tag) {{
                const bookmarks = document.querySelectorAll('.bookmark');
                const filters = document.querySelectorAll('.filter');

                // Update active filter
                filters.forEach(filter => {{
                    if (filter.dataset.tag === tag) {{
                        filter.classList.add('active');
                    }} else {{
                        filter.classList.remove('active');
                    }}
                }});

                // Filter bookmarks
                bookmarks.forEach(bookmark => {{
                    const tags = bookmark.getAttribute('data-tags').split('|'); // Use pipe "|" as delimiter
                    if (tag === 'all' || tags.includes(tag)) {{
                        bookmark.style.display = 'flex';
                    }} else {{
                        bookmark.style.display = 'none';
                    }}
                }});
            }}

            // Refresh the filters bar dynamically
            function refreshFiltersBar() {{
                fetch(`/get_tags/${{chatId}}`)
                    .then(response => response.json())
                    .then(tags => {{
                        const filtersContainer = document.querySelector('.filters');
                        if (filtersContainer) {{
                            let filtersHtml = '';
                            filtersHtml += `<span class="filter active" data-tag="all">All</span>`;
                            tags.forEach(tag => {{
                                filtersHtml += `<span class="filter" data-tag="${{tag}}">${{tag}}</span>`;
                            }});
                            filtersContainer.innerHTML = filtersHtml;

                            // Attach event listeners to the filters
                            filtersContainer.querySelectorAll('.filter').forEach(filter => {{
                                filter.addEventListener('click', () => {{
                                    filterByTag(filter.dataset.tag);
                                }});
                            }});
                        }}
                    }})
                    .catch(error => {{
                        console.error("Error refreshing filters bar:", error);
                    }});
            }}
            // Define other functions
            function deleteAllLinks() {{
                if (confirm("Are you sure you want to delete all links and tags? This action cannot be undone.")) {{
                    fetch(`/delete_all/${{chatId}}`, {{ method: "DELETE" }})
                        .then(response => response.json())
                        .then(data => {{
                            if (data.message === "All links and tags deleted successfully!") {{
                                alert(data.message);
                                location.reload(); // Reload the page to reflect the changes
                            }} else {{
                                alert(data.error || "Failed to delete all links.");
                            }}
                        }})
                        .catch(error => {{
                            console.error("Error deleting all links:", error);
                            alert("An error occurred while deleting all links and tags.");
                        }});
                }}
            }}

            function openTagDialog(linkId) {{
                const existingTags = Array.from(document.querySelectorAll('.filter:not(.active)')).map(tag => tag.innerText);

                // Create a modal-like dialog
                const modal = document.createElement('div');
                modal.style.position = 'fixed';
                modal.style.top = '50%';
                modal.style.left = '50%';
                modal.style.transform = 'translate(-50%, -50%)';
                modal.style.backgroundColor = '#fff';
                modal.style.padding = '20px';
                modal.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.1)';
                modal.style.zIndex = '1000';
                modal.style.borderRadius = '8px';
                modal.style.maxWidth = '90%';
                modal.style.textAlign = 'center';

                // Modal content
                modal.innerHTML = `
                    <h3>Select Tags</h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">
                        ${{
                            existingTags.map(tag => `
                                <span class="filter" style="cursor: pointer; padding: 6px 12px; border-radius: 12px; background-color: #e0f7fa; color: #00796b;" data-tag="${{tag}}">
                                    ${{tag}}
                                </span>
                            `).join('')
                        }}
                    </div>
                    <div style="margin-top: 15px;">
                        <input id="newTagInput" type="text" placeholder="Add a new tag" 
                            style="padding: 6px 10px; width: calc(100% - 24px); border: 1px solid #ddd; border-radius: 8px;">
                    </div>

                    <button id="saveTags" style="margin-top: 20px; padding: 10px 20px; background-color: #00796b; color: white; border: none; border-radius: 8px; cursor: pointer;">
                        Save Tags
                    </button>
                    <button id="cancelTags" style="margin-top: 20px; padding: 10px 20px; background-color: #f8d7da; color: #721c24; border: none; border-radius: 8px; cursor: pointer; margin-left: 10px;">
                        Cancel
                    </button>
                `;

                // Add modal to the document
                document.body.appendChild(modal);

                // Handle tag selection
                const selectedTags = new Set();
                modal.querySelectorAll('.filter').forEach(tagElement => {{
                    tagElement.addEventListener('click', () => {{
                        const tag = tagElement.dataset.tag;
                        if (selectedTags.has(tag)) {{
                            selectedTags.delete(tag);
                            tagElement.style.backgroundColor = '#e0f7fa';
                            tagElement.style.color = '#00796b';
                        }} else {{
                            selectedTags.add(tag);
                            tagElement.style.backgroundColor = '#00796b';
                            tagElement.style.color = 'white';
                        }}
                    }});
                }});

                // Handle save action
                modal.querySelector('#saveTags').addEventListener('click', () => {{
                const newTag = document.getElementById('newTagInput').value.trim();
                if (newTag) {{
                    selectedTags.add(newTag); // Add the new tag to the selected tags
                }}

                if (selectedTags.size > 0) {{
                    const tagsArray = Array.from(selectedTags);

                    // Use `Promise.all` to handle multiple tag additions
                    Promise.all(tagsArray.map(tag =>
                        fetch(`/add_tag/${{linkId}}`, {{
                            method: "POST",
                            headers: {{
                                "Content-Type": "application/json"
                            }},
                            body: JSON.stringify({{ tag }})
                        }})
                        .then(response => {{
                            if (!response.ok) {{
                                throw new Error(`Failed to add tag: ${{tag}}`);
                            }}
                            return response.json();
                        }})
                        .then(data => {{
                            if (data.message !== "Tag added successfully!") {{
                                throw new Error(data.error || `Error adding tag: ${{tag}}`);
                            }}
                        }})
                    ))
                    .then(() => {{
                        refreshFiltersBar(); // Refresh the filters bar dynamically
                        location.reload();   // Reload the page to reflect changes
                    }})
                    .catch(error => {{
                        console.error("Error adding tags:", error);
                        alert("An error occurred while adding the tags. Please try again.");
                    }});
                }}

                document.body.removeChild(modal);
            }});



                // Handle cancel action
                modal.querySelector('#cancelTags').addEventListener('click', () => {{
                    document.body.removeChild(modal);
                }});
            }}


            function deleteLink(linkId) {{
                if (confirm("Are you sure you want to delete this link?")) {{
                    fetch(`/delete_link/${{linkId}}`, {{ method: "DELETE" }})
                        .then(response => {{
                            if (response.ok) {{
                                alert("Link deleted successfully!");
                                location.reload(); // Reload the page to update the UI
                            }} else {{
                                alert("Failed to delete the link.");
                            }}
                        }})
                        .catch(error => {{
                            console.error("Error deleting link:", error);
                            alert("An error occurred while deleting the link.");
                        }});
                }}
            }}

            function deleteActiveTag() {{
                const activeFilter = document.querySelector('.filter.active');
                const activeTag = activeFilter ? activeFilter.dataset.tag : 'all';
                if (activeTag === 'all') {{
                    alert("Cannot delete the 'All' tag.");
                    return;
                }}
                if (confirm(`Are you sure you want to delete the tag '${{activeTag}}'? This action cannot be undone.`)) {{
                    fetch(`/delete_tag/${{chatId}}/${{activeTag}}`, {{ method: "DELETE" }})
                        .then(response => response.json())
                        .then(data => {{
                            if (data.message === "Tag deleted successfully!") {{
                                alert(data.message);
                                location.reload();
                            }} else {{
                                alert(data.error || "Failed to delete the tag.");
                            }}
                        }})
                        .catch(error => {{
                            console.error("Error deleting tag:", error);
                            alert("An error occurred while deleting the tag.");
                        }});
                }}
            }}

            function deleteTagFromLink(linkId, tagName) {{
                if (confirm(`Are you sure you want to remove the tag '${{tagName}}' from this link?`)) {{
                    fetch(`/delete_tag_from_link/${{linkId}}/${{encodeURIComponent(tagName)}}`, {{ method: "DELETE" }})
                        .then(response => response.json())
                        .then(data => {{
                            if (data.message === "Tag removed successfully!") {{
                                alert(data.message);
                                location.reload(); // Reload to reflect changes
                            }} else {{
                                alert(data.error || "Failed to remove the tag.");
                            }}
                        }})
                        .catch(error => {{
                            console.error("Error deleting tag:", error);
                            alert("An error occurred while removing the tag.");
                        }});
                }}
            }}

            function editTitle(linkId) {{
                const newTitle = prompt("Enter a new title for the link:");
                if (newTitle && newTitle.trim() !== "") {{
                    fetch(`/update_link_title/${{linkId}}`, {{
                        method: "POST",
                        headers: {{
                            "Content-Type": "application/json"
                        }},
                        body: JSON.stringify({{ title: newTitle }})
                    }})
                    .then(response => response.json())
                    .then(data => {{
                        if (data.message === "Title updated successfully!") {{
                            alert(data.message);
                            location.reload(); // Reload to reflect the updated title
                        }} else {{
                            alert(data.error || "Failed to update the title.");
                        }}
                    }})
                    .catch(error => {{
                        console.error("Error updating title:", error);
                        alert("An error occurred while updating the title.");
                    }});
                }}
            }}


        </script>
        """

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
                <div class="actions">
                    <button class="delete-all" onclick="deleteAllLinks()">Delete All Links</button>
                    <button class="delete-active-tag" onclick="deleteActiveTag()">Delete Active Tag</button>
                </div>

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