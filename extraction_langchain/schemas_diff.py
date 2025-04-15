from pydantic import BaseModel, Field
from typing import Optional
from typing import List

class Company_Name(BaseModel):
    value: Optional[str] = Field(
        ..., description="Name of the insurance company"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Product_Name(BaseModel):
    value: Optional[str] = Field(
        ..., description="Name of the insurance product"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Product_Type(BaseModel):
    value: Optional[str] = Field(
        ..., description="Type of the insurance product (e.g., Term, ULIP, Endowment)"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Product_UIN(BaseModel):
    value: Optional[str] = Field(
        ..., description="Unique Identification Number of the product"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Plan_Description(BaseModel):
    value: Optional[str] = Field(
        ..., description="Brief and statistical description of the insurance plan"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Plan_Options(BaseModel):
    value: Optional[str] = Field(
        ..., description="Available plan options with statistical details"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Death_Benefits(BaseModel):
    value: Optional[str] = Field(
        ..., description="The sum assured on death from the policy in the event of the policyholder's death"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Other_Benefits(BaseModel):
    value: Optional[str] = Field(
        ..., description="Other benefits like child-care benefits, life-stage benefits etc. available to the policyholder"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Surrender_Benefits(BaseModel):
    value: Optional[str] = Field(
        ..., description="The surrender value/benefits available in the policy"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Surrender_Value_Factor(BaseModel):
    value: Optional[str] = Field(
        ..., description="The surrender value factor for surrender benefits of the policy"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Paid_Up_Value(BaseModel):
    value: Optional[str] = Field(
        ..., description="The paid up value available for the policy"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Paid_Up_Death_Benefit(BaseModel):
    value: Optional[str] = Field(
        ..., description="The paid up sum assured on death for the policy"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Exit_Options(BaseModel):
    value: Optional[str] = Field(
        ..., description="The exit options available for the policy"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Exit_Option_Conditions(BaseModel):
    value: Optional[str] = Field(
        ..., description="The conditions to be met to avail the exit option(s) available for the policy"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Premium_Payment_Option(BaseModel):
    value: Optional[str] = Field(
        ..., description="Available premium payment options (e.g., Annual, Monthly)"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Min_Age_At_Entry(BaseModel):
    value: Optional[str] = Field(
        ..., description="Minimum age required to purchase the policy (in years)"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Max_Age_At_Entry(BaseModel):
    value: Optional[str] = Field(
        ..., description="Maximum age allowed for policy entry (in years)"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Max_Age_At_Maturity(BaseModel):
    value: Optional[str] = Field(
        ..., description="Maximum age allowed at policy maturity (in years)"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Minimum_Sum_Assured(BaseModel):
    value: Optional[str] = Field(
        ..., description="Minimum sum assured for the policy (in INR)"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Maximum_Sum_Assured(BaseModel):
    value: Optional[str] = Field(
        ..., description="Maximum sum assured for the policy"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Minimum_Policy_Term(BaseModel):
    value: Optional[str] = Field(
        ..., description="Minimum term for the policy (in years)"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Maximum_Policy_Term(BaseModel):
    value: Optional[str] = Field(
        ..., description="Maximum term for the policy (in years)"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Premium_Paying_Term(BaseModel):
    value: Optional[str] = Field(
        ..., description="Premium paying term (e.g., 'Equal to policy term')"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Annual_Minimum_Premium(BaseModel):
    value: Optional[str] = Field(
        ..., description="Minimum annual premium amount (in INR)"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Maximum_Premium(BaseModel):
    value: Optional[str] = Field(
        ..., description="Maximum premium amount"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Discount_Online(BaseModel):
    value: Optional[str] = Field(
        ..., description="Online discounts (if any) for the policy"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Discount_Staff(BaseModel):
    value: Optional[str] = Field(
        ..., description="Discount available to the staff"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Discount_Female(BaseModel):
    value: Optional[str] = Field(
        ..., description="Discount available to female individuals"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Discount_Existing_Customers(BaseModel):
    value: Optional[str] = Field(
        ..., description="Discount available to the existing customers of the company"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Discount_Salaried(BaseModel):
    value: Optional[str] = Field(
        ..., description="Discount available to salaried individuals"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Discount_High_Sum(BaseModel):
    value: Optional[str] = Field(
        ..., description="Discount available on high sum"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )

class Rider_Benefits(BaseModel):
    value: Optional[str] = Field(
        ..., description="Rider benefits available in the policy"
    )
    page_number: Optional[str] = Field(
        ..., description="Page number where the field was extracted from"
    )
    chunks: Optional[List[str]] = Field(
        ...,
        description="Source of the chunks, keep it empty if null",
    )
