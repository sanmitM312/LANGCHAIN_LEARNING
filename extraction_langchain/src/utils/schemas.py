from pydantic import BaseModel, Field
from typing import Optional
from typing import List

class TUnitLinkedPlanField(BaseModel):
    value: Optional[str] = Field(default=None, description="Extracted field value")
    page_number: Optional[str] = Field(default=None, description="Page number where the field was extracted from")
    description: Optional[str] = Field(default=None, description="Description of the field")
    chunks : Optional[List[str]] = Field(default=None, description="Source of the chunks, keep it empty if null")

class TUnitLinkedPlan(BaseModel):
    company_name: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Name of the insurance company"
    )
    product_name: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Name of the insurance product/policy"
    )
    product_uin: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Unique Identification Number of the product"
    )
    product_type: Optional[TUnitLinkedPlanField] = Field(
        default=None,  
        description="Type of the insurance product (e.g., Term, ULIP, Endowment)"
    )
    distribution_channel: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Distribution channel for the product (e.g., Online, Offline, Online and Offline, Agent)"
    )  
    plan_description: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Key features of the insurance product"
    )
    plan_options: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="The available plan options for the policy/product and their short descriptions"
    )
    terminal_illness_benefits: Optional[TUnitLinkedPlanField] = Field(
        default = None,
        description = "Benefits available in case of terminal illness (on diagnosis)"
    )
    other_benefits: Optional[TUnitLinkedPlanField] = Field(
        default = None,
        description = "Other optional benefits like child care benefits adoption, life stage benefits like marriage etc. available to the policyholder"
    )
    death_benefit_payment_option: Optional[TUnitLinkedPlanField] = Field(
        default = None,
        description = "Payout options of the amount to be paid to the nominee in the event of the policyholder's death",
    )

    premium_payment_option: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Different premium payment options available (e.g., Single, Regular, Limited)"
    )
    min_age_at_entry: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Minimum age required to purchase the policy/product (in years) for different plan options"
    )
    max_age_at_entry: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Maximum age allowed for policy/product entry (in years) for different plan options"
    )
    max_age_at_maturity: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Maximum age allowed at policy/product maturity (in years)"
    )
    minimum_sum_assured: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Min. Basic Sum assured for the policy/product"
    )
    maximum_sum_assured: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Max. Basic Sum assured for the policy/product"
    )
    minimum_policy_term: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Minimum policy/product term(in years)"
    )
    maximum_policy_term: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Maximum policy/product term (in years)"
    )
    premium_paying_term: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Premium payment terms along with their term details  (e.g.,5 pay ,7 pay, 10 pay ,15 pay,  less 5 yrs, 60 yrs less Age at Entry (Limited Pay);Regular & Single Pay;"
    )
    minimum_premium: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Minimum annual premium amount  for the policy/product, if applicable"
    )
    maximum_premium: Optional[TUnitLinkedPlanField] = Field(
        default=None, 
        description="Maximum premium amount for the policy/product, if applicable"
    )
    death_benefits: Optional[TUnitLinkedPlanField] = Field(
        default = None,
        description = "The sum assured on death from the policy/product in the event of the policyholder's death"
    )
    instant_cash_benefit: Optional[TUnitLinkedPlanField] = Field(
        default = None,
        description = "The instant cash on claim/benefit available in the policy/product"
    )
    surrender_benefits: Optional[TUnitLinkedPlanField] = Field(
        default = None,
        description = "The surrender value/benefits available in the policy/product, including unexpired risk premium details if available"
    )
    surrender_value_factor: Optional[TUnitLinkedPlanField] = Field(
        default = None,
        description = "The surrender value factor for surrender benefits of the policy/product. Include unexpired risk premium detials formula if available"  
    )
    paid_up_value: Optional[TUnitLinkedPlanField] = Field(
        default = None,
        description = "The paid up value available for the policy/product"
    )
    paid_up_death_benefit : Optional[TUnitLinkedPlanField] = Field(
        default = None,
        description = "The paid up sum assured on death for the policy/product"
    )
    exit_options : Optional[TUnitLinkedPlanField] = Field(
        default = None,
        description = "The exit options available for the policy/product which includes Smart exit options, partial withdrawal, etc."
    )
    exit_option_conditions : Optional[TUnitLinkedPlanField] = Field(
        default = None,
        description = "The conditions to be met to avail the smart exit option(s) etc.  for the policy/product"
    )
    
    discount_online : Optional[TUnitLinkedPlanField] = Field(
        default=None,
        description="Online discounts (if any) for the policy/product"
    )
    discount_staff: Optional[TUnitLinkedPlanField] = Field(
        default = None,
        description = "Discount available to the staff."
    )
    discount_female : Optional[TUnitLinkedPlanField] = Field(
        default = None,
        description = "Discount available to female individuals."
    )
    discount_existing_customers: Optional[TUnitLinkedPlanField] = Field(
        default = None,
        description = "Discount available to the existing customers of the policy/product."
    )
    discount_salaried: Optional[TUnitLinkedPlanField] = Field(
        default = None,
        description = "Discount available to salaried customers of the policy, if available."
    )
    discount_high_sum: Optional[TUnitLinkedPlanField] = Field(
        default = None,
        description = "Discount available on high sum insurance."
    )

    rider_benefits: Optional[TUnitLinkedPlanField] = Field(
        default = None,
        description = "The various rider benefits available for the policy/product along with their description"
    )
