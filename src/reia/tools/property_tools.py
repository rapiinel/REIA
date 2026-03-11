from typing import Type
import json
import os
import requests
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class PropertyIntelInput(BaseModel):
    normalized_address: str = Field(..., description="Normalized full address")
    business_name: str = Field(..., description="Confirmed business name")


class PropertyIntelTool(BaseTool):
    name: str = "property_intel_tool"
    description: str = (
        "Search public web results for commercial property intelligence tied to an address."
    )
    args_schema: Type[BaseModel] = PropertyIntelInput

    def _run(self, normalized_address: str, business_name: str) -> str:
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            return json.dumps({"error": "SERPER_API_KEY not set"})

        url = "https://google.serper.dev/search"
        query = (
            f'"{normalized_address}" "{business_name}" '
            f'owner OR assessor OR appraisal OR sqft OR square feet OR year built OR parcel'
        )

        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                url, headers=headers, json={"q": query}, timeout=20
            )
            response.raise_for_status()
            data = response.json()
            organic = data.get("organic", [])[:8]
            return json.dumps({
                "query": query,
                "results": organic
            })
        except Exception as e:
            return json.dumps({"error": str(e)})