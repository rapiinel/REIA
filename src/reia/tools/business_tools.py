from typing import Type
import json
import os
import requests
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class SearchBusinessInput(BaseModel):
    search_address: str = Field(..., description="Normalized full address")


class SearchBusinessTool(BaseTool):
    name: str = "search_business_tool"
    description: str = (
        "Search the web for the actual business operating at an exact address."
    )
    args_schema: Type[BaseModel] = SearchBusinessInput

    def _run(self, search_address: str) -> str:
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            return json.dumps({"error": "SERPER_API_KEY not set"})

        url = "https://google.serper.dev/places"
        payload = {
            # "q": f'"{search_address}" business OR company OR tenant OR office OR warehouse' # original query
            # "q": f'{search_address} OR {search_address} business OR {search_address} company OR {search_address} location'
            "q": f'What businesses are at {search_address}',
            "location": "United States",
            "autocorrect": False
        }
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=20)
            response.raise_for_status()
            data = response.json()
            print('='*10)
            print(data)
            print('='*10)
            organic = data.get("places", [])[:8]
            return json.dumps({
                "query": payload["q"],
                "results": organic
            })
        except Exception as e:
            return json.dumps({"error": str(e)})