import json
import os
from fastapi import HTTPException
from utils.models import UserAnalysis, Recommendation

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