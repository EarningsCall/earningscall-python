import argparse
import logging

from earningscall import get_all_companies, get_sp500_companies
from earningscall.utils import configure_sane_logging

parser = argparse.ArgumentParser(description='')
parser.add_argument('--debug', action='store_true', help='Enable debug logs')
parser.add_argument('--sp-500', action='store_true', help='Show S&P500 Companies')

args = parser.parse_args()
level = logging.DEBUG
if args.debug:
    level = logging.DEBUG
configure_sane_logging(level=level)

if args.sp_500:
    get_func = get_sp500_companies
else:
    get_func = get_all_companies

for company in get_func():
    print(f"{company.company_info} -- {company.company_info.sector} -- {company.company_info.industry}")
