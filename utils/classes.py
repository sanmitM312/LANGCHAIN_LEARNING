from pydantic import BaseModel, Field
from typing import Optional
from typing import List

class TUnitLinkedPlanField(BaseModel):
    value: Optional[str] = Field(default=None, description="Extracted field value")
    page_number: Optional[str] = Field(default=None, description="Page number where the field was extracted from")
    description: Optional[str] = Field(default=None, description="Description of the field")

class TUnitLinkedPlan(BaseModel):
    company_name: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Name of the insurance company"
    )
    product_name: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Name of the insurance product"
    )
    product_type: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Type of the insurance product (e.g., Term, ULIP, Endowment)"
    )
    product_uin: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Unique Identification Number of the product"
    )
    plan_description: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Brief and statistical description of the insurance plan"
    )
    key_features: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Key features of the insurance product"
    )
    plan_options: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Available plan options with statistical details"
    )
    premium_payment_option: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Available premium payment modes (e.g., Annual, Monthly)"
    )
    min_age_at_entry: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Minimum age required to purchase the policy (in years)"
    )
    max_age_at_entry: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Maximum age allowed for policy entry (in years)"
    )
    max_age_at_maturity: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Maximum age allowed at policy maturity (in years)"
    )
    minimum_sum_assured: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Minimum sum assured for the policy (in INR)"
    )
    maximum_sum_assured: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Maximum sum assured for the policy"
    )
    minimum_policy_term: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Minimum term for the policy (in years)"
    )
    maximum_policy_term: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Maximum term for the policy (in years)"
    )
    premium_paying_term: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Premium paying term (e.g., 'Equal to policy term')"
    )
    annual_minimum_premium: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Minimum annual premium amount (in INR)"
    )
    maximum_premium: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Maximum premium amount"
    )
    minimum_top_up_premium: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Minimum top-up premium amount (in INR)"
    )
    maximum_top_up_premium: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Maximum top-up premium amount"
    )

