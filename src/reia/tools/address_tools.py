from typing import Type
import json
import requests
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class NormalizeAddressInput(BaseModel):
    street: str = Field(..., description="Street address")
    city: str = Field(..., description="City")
    state: str = Field(..., description="State")
    zip_code: str = Field(..., description="ZIP code")


class NormalizeAddressTool(BaseTool):
    name: str = "normalize_address_tool"
    description: str = (
        "Normalize and validate a US address using OpenStreetMap Nominatim."
    )
    args_schema: Type[BaseModel] = NormalizeAddressInput

    def _run(self, street: str, city: str, state: str, zip_code: str) -> str:
        query = f"{street}, {city}, {state} {zip_code}, USA"
        url = "https://nominatim.openstreetmap.org/search"
        headers = {"User-Agent": "reia-agent/1.0"}
        params = {"q": query, "format": "jsonv2", "limit": 1}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=20)
            response.raise_for_status()
            data = response.json()
            if not data:
                return json.dumps({
                    "normalized_address": None,
                    "address_status": "not_found",
                    "address_notes": "No matching address found",
                    "confidence": "low"
                })
            hit = data[0]
            return json.dumps({
                "normalized_address": hit.get("display_name"),
                "search_address": f"{street} {city} {state} {zip_code}",
                "lat": hit.get("lat"),
                "lon": hit.get("lon"),
                "address_status": "validated",
                "address_notes": "Address matched via Nominatim",
                "confidence": "medium"
            })
        except Exception as e:
            return json.dumps({
                "normalized_address": None,
                "address_status": "error",
                "address_notes": str(e),
                "confidence": "low"
            })