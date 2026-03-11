from typing import Type
import json
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


NAICS_MAP = {
    "accounting": {"code": "541211", "title": "Offices of Certified Public Accountants"},
    "law firm": {"code": "541110", "title": "Offices of Lawyers"},
    "restaurant": {"code": "722511", "title": "Full-Service Restaurants"},
    "warehouse": {"code": "493110", "title": "General Warehousing and Storage"},
    "manufacturing": {"code": "333999", "title": "All Other Miscellaneous General Purpose Machinery Manufacturing"},
    "medical clinic": {"code": "621498", "title": "All Other Outpatient Care Centers"},
    "logistics": {"code": "488510", "title": "Freight Transportation Arrangement"},
    "auto repair": {"code": "811111", "title": "General Automotive Repair"},
}


class InferNaicsInput(BaseModel):
    business_description: str = Field(..., description="Business description or services")
    business_name: str = Field(..., description="Business name")


class InferNaicsTool(BaseTool):
    name: str = "infer_naics_tool"
    description: str = (
        "Infer a likely NAICS code from business description and name using a simple ruleset."
    )
    args_schema: Type[BaseModel] = InferNaicsInput

    def _run(self, business_description: str, business_name: str) -> str:
        text = f"{business_name} {business_description}".lower()
        for keyword, value in NAICS_MAP.items():
            if keyword in text:
                return json.dumps({
                    "primary_naics_code": value["code"],
                    "primary_naics_title": value["title"],
                    "method": f"keyword_match:{keyword}",
                    "confidence": "medium"
                })

        return json.dumps({
            "primary_naics_code": None,
            "primary_naics_title": None,
            "method": "no_match",
            "confidence": "low"
        })