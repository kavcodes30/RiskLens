from pydantic import BaseModel, Field, computed_field,field_validator
from typing import Annotated, Literal
from config.city_tier import tier_1_cities, tier_2_cities

class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the user")]
    weight: Annotated[float, Field(..., gt=0, lt=500, description="Weight of the user in kg")]
    height: Annotated[float, Field(..., gt=0, lt=3, description="Height of the user in meters")]
    income_lpa: Annotated[float, Field(..., gt=0, description="Income of the user in LPA")]
    smoker: Annotated[bool, Field(..., description="User is smoker or non smoker")]
    city: Annotated[
        Literal[
            "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune",
            "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
            "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
            "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
            "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
            "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
            "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri",
        ],
        Field(..., description="City of the user", examples=["Mumbai"]),
    ]
    occupation: Annotated[
        Literal[
            "retired", "student", "freelancer", "government_job",
            "private_job", "business_owner", "unemployed",
        ],
        Field(..., description="Occupation of the user", examples=["private_job"]),
    ]
 
    # mode="before" so "  mumbai " is cleaned up BEFORE the Literal check runs
    @field_validator("city", mode="before")
    @classmethod
    def normalize_city(cls, v):
        if isinstance(v, str):
            return v.strip().title()
        return v

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        else:
            return "senior"

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3