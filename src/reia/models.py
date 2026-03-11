from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_validator

ConfidenceLevel = Literal["high", "medium", "low"]


class SourceRef(BaseModel):
    label: str
    url: Optional[str] = None


class ReiaOutput(BaseModel):
    input_address: str
    normalized_address: Optional[str] = None

    confirmed_business_name: Optional[str] = None
    dba_name: Optional[str] = None
    business_type: Optional[str] = None
    business_confidence: ConfidenceLevel = "low"

    primary_naics_code: Optional[str] = None
    primary_naics_title: Optional[str] = None
    secondary_naics_codes: List[str] = Field(default_factory=list)

    business_description: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    employee_estimate: Optional[str] = None

    industry_category: Optional[str] = None
    property_use_type: Optional[str] = None
    industrial_subtype: Optional[str] = None
    occupancy_type: Optional[str] = None

    owner_name: Optional[str] = None
    owner_entity_type: Optional[str] = None
    building_sqft: Optional[float] = None
    lot_size: Optional[str] = None
    year_built: Optional[int] = None
    multi_tenant_flag: Optional[bool] = None

    expansion_signals: List[str] = Field(default_factory=list)

    sources: List[SourceRef] = Field(default_factory=list)
    final_confidence: ConfidenceLevel = "low"
    notes: List[str] = Field(default_factory=list)

    @field_validator(
        "secondary_naics_codes",
        "expansion_signals",
        "sources",
        "notes",
        mode="before",
    )
    @classmethod
    def ensure_list(cls, v):
        if v is None:
            return []
        return v