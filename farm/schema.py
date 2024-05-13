from pydantic import BaseModel
from typing import Literal, List, Optional
from langchain_core.pydantic_v1 import BaseModel as BaseModel_V1, Field
import json


class PestsAndDiseasesSchema(BaseModel):
    pests: str | None = "No pests"
    diseases: str | None = "No diseases"

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str):
        return cls.from_dict(json.loads(json_str))

    class Config:
        json_schema_extra = {
            "example": {
                "pests": "Aphids, Thrips, Whiteflies",
                "diseases": "Powdery Mildew, Downy Mildew, Fusarium Wilt"
            }
        }


class SoilSchema(BaseModel):
    soil_type: Literal["Clay", "Sandy", "Loamy", "Chalky", "Silt"]
    soil_ph: Literal[
        "Strong acidic (3.5–4.4)",
        "Acidic (4.5-6.5)",
        "Neutral (6.6–7.3)",
        "Alkaline (7.4-9)",
        "Strongly alkaline: > 9.0",
    ]
    pct_soil_moisture: float
    soil_fertility: Literal["Low", "Medium", "High"]

class Crop(BaseModel):
    crop: str
    growth_stage: str

class FarmDataSchema(BaseModel):
    crop: Crop
    soil: SoilSchema
    pests_and_diseases: Optional[PestsAndDiseasesSchema] = None
    key_weeds: str | None = None

class PestAndDiseasePrevention(BaseModel_V1):
    """Extract recommendations for pest and disease prevention based on farm data."""

    recommendations: List[str] = Field(
        description="List of recommendations for pest and disease prevention based on farm data"
    )


class PestAndDiseaseTreatment(BaseModel_V1):
    """Extract recommendations for pest and disease treatment based on farm data."""

    organic: str = Field(description="organic treatments for pest and disease")
    chemical: str = Field(description="chemical treatments for pest and disease")


class PestAndDiseaseControl(BaseModel_V1):
    """Extract recommendations for pest and disease control based on farm data."""
    prevention: PestAndDiseasePrevention
    treatment: PestAndDiseaseTreatment


class WeedControlPlan(BaseModel_V1):
    """Detailed weed control recommendations by crop at crop growth stage."""
    pre_emergent: List[str] = Field(..., description="A list of pre-emergent herbicide recommendations.")
    post_emergent: List[str] = Field(..., description="A list of post-emergent herbicide recommendations.")
    cultural: List[str] = Field(..., description="A list of cultural control practices.")
    mechanical: List[str] = Field(..., description="A list of mechanical control practices.")
    chemical: List[str] = Field(..., description="A list of chemical control practices.")
    special: str= Field(..., description="Special considerations given the crop, growth stage, and weather.")


class SoilHealthRecommendations(BaseModel_V1):
    """
    Recommendations for improving soil health.
    """

    soil_amendments: List[str]
    cover_cropping_strategies: List[str]
    tillage_practices: List[str]
    organic_matter_management: str

class IntegratedCropManagement(BaseModel_V1):
    """
    Recommendations for integrated crop management.
    """

    irrigation_scheduling: str
    irrigation_techniques: str
    harvest_and_post_harvest: str


class SoilHealthAndCropManagementPlan(BaseModel_V1):
    """
    Extracted the comprehensive soil health and crop management plan.
    """

    soil_health_recommendations: SoilHealthRecommendations
    integrated_crop_management: IntegratedCropManagement


class ChemicalTreatment(BaseModel_V1):
    """
    Represents a chemical treatment recommendation for pest and disease control.
    """
    product: str = Field(..., description="The commercial name of the chemical product.")
    application_rate: str = Field(..., description="The recommended application rate for the chemical product.")
    safety_precautions: str = Field(..., description="The safety precautions associated with the chemical product.")
class OrganicTreatment(BaseModel_V1):
    """
    Represents an organic treatment recommendation for pest and disease control.
    """
    treatment: str = Field(..., description="The name or description of the organic treatment.")
    application_rate: str = Field(..., description="The recommended application rate for the organic treatment.")
    safety_precautions: str = Field(..., description="The safety precautions associated with the organic treatment.")
    
class PestDiseaseControlRecommendations(BaseModel_V1):
    """
    The structured output schema for pest and disease control recommendations. The output should follow this schema to ensure consistency and compatibility with downstream processes.
    """
    prevention_recommendations: List[str] = Field(..., description="A list of Recommendations for preventive measures against pests and diseases.")
    organic_treatments: List[OrganicTreatment] = Field(..., description="A list of recommended organic treatments for pest and disease control.")
    chemical_treatments: List[ChemicalTreatment] = Field(..., description="A list of recommended chemical treatments for pest and disease control.")