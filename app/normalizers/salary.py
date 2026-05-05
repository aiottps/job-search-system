import re
from typing import Tuple, Optional, NamedTuple

class SalaryParseResult(NamedTuple):
    annual_min: Optional[int]
    annual_max: Optional[int]
    is_estimated: bool
    note: Optional[str]

def parse_salary(salary_text: str) -> SalaryParseResult:
    """
    Parses salary text and returns structured results.
    Assumes monthly salary * 12 for annual estimate.
    """
    if not salary_text:
        return SalaryParseResult(None, None, False, None)

    salary_text = salary_text.replace(',', '').strip()
    
    # Handle specific "面議" with monthly 40k+ hint
    if "面議" in salary_text and "4萬" in salary_text:
        return SalaryParseResult(
            annual_min=480000, 
            annual_max=None, 
            is_estimated=True, 
            note="平台僅揭露經常性薪資達 4 萬元以上，實際薪資資料不足"
        )

    # If it's just "面議" or "待遇依公司規定" without numbers
    if "面議" in salary_text or "待遇依公司規定" in salary_text:
        return SalaryParseResult(None, None, False, "薪資面議或依公司規定，無具體數字")

    # Detect period
    is_annual = "年薪" in salary_text or "年" in salary_text
    is_monthly = "月薪" in salary_text or "月" in salary_text
    
    # Extract numbers (supporting decimals)
    # Using regex to find numbers like 4.5, 6, 1.2
    numbers = re.findall(r'\d+(?:\.\d+)?', salary_text)
    if not numbers:
        return SalaryParseResult(None, None, False, "無法解析薪資數字")

    # Determine base multiplier
    # Default to monthly if not explicitly annual and first number < 200 (e.g. 4.5, 50, 150)
    # If first number is large (e.g. 700000), it's likely annual or raw monthly.
    first_val = float(numbers[0])
    
    if not is_annual and (is_monthly or first_val < 200):
        multiplier = 12
    else:
        multiplier = 1

    # Handle "萬" or "百萬" units
    unit_multiplier = 1
    if "百萬" in salary_text:
        unit_multiplier = 1000000
    elif "萬" in salary_text:
        unit_multiplier = 10000

    total_multiplier = multiplier * unit_multiplier
    
    low = int(float(numbers[0]) * total_multiplier)
    high = int(float(numbers[1]) * total_multiplier) if len(numbers) > 1 else low
    
    return SalaryParseResult(low, high, False, None)
