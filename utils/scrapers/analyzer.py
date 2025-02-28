import time
from .amazon import fetch_from_soax_api
from .opengraph import fetch_opengraph_metadata
from .models import ProductData

async def analyze_link(link: str) -> ProductData:
    """Analyze a link to retrieve structured data."""
    start_time = time.time()  # Record the start time
    
    if "amazon" in link:
        result = await fetch_from_soax_api(link)
    else:
        result = await fetch_opengraph_metadata(link)
    
    end_time = time.time()  # Record the end time
    duration = end_time - start_time  # Calculate the duration
    print(f"Link analysis took {duration:.4f} seconds.")
    
    return result 