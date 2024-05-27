from earningscall import get_all_companies
from earningscall.utils import enable_debug_logs


enable_debug_logs()

for company in get_all_companies():
    print(f"{company.company_info} -- {company.company_info.sector} -- {company.company_info.industry}")
