from enum import Enum


class ColNames(str, Enum):
    TECH_NAME = 'event_agent_name'
    EVENT_ID = 'event_id'
    ASSET_ID = 'asset_id'
    PRODUCT_TYPE = 'product_type'
    EVENT_DATE = 'event_date'
    CUSTOMER_NAME = 'customer_name'
    TOTAL_PART_COST = 'total_part_cost'
    TOTAL_LABOR_COST = 'total_labor_cost'
    LABOR_DURATION = 'labor_duration'
    TRAVEL_TIME = 'travel_duration'
    FREE_TEXT = 'free_text'



