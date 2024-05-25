import json
import logging


log = logging.getLogger(__file__)
sectors_file_name = "sectors.json"


SECTORS_IN_ORDER = [
    'Basic Materials',
    'Communication Services',
    'Consumer Cyclical',
    'Consumer Defensive',
    'Energy',
    'Financial Services',
    'Healthcare',
    'Industrials',
    'Real Estate',
    'Technology',
    'Utilities'
]


INDUSTRIES_IN_ORDER = [
    'Advertising Agencies',
    'Aerospace & Defense',
    'Agricultural Inputs',
    'Airlines',
    'Airports & Air Services',
    'Aluminum',
    'Apparel Manufacturing',
    'Apparel Retail',
    'Asset Management',
    'Auto & Truck Dealerships',
    'Auto Manufacturers',
    'Auto Parts',
    'Banks - Diversified',
    'Banks - Regional',
    'Beverages - Brewers',
    'Beverages - Non-Alcoholic',
    'Beverages - Wineries & Distilleries',
    'Biotechnology',
    'Broadcasting',
    'Building Materials',
    'Building Products & Equipment',
    'Business Equipment & Supplies',
    'Capital Markets',
    'Chemicals',
    'Coking Coal',
    'Communication Equipment',
    'Computer Hardware',
    'Confectioners',
    'Conglomerates',
    'Consulting Services',
    'Consumer Electronics',
    'Copper',
    'Credit Services',
    'Department Stores',
    'Diagnostics & Research',
    'Discount Stores',
    'Drug Manufacturers - General',
    'Drug Manufacturers - Specialty & Generic',
    'Education & Training Services',
    'Electrical Equipment & Parts',
    'Electronic Components',
    'Electronic Gaming & Multimedia',
    'Electronics & Computer Distribution',
    'Engineering & Construction',
    'Entertainment',
    'Farm & Heavy Construction Machinery',
    'Farm Products',
    'Financial Conglomerates',
    'Financial Data & Stock Exchanges',
    'Food Distribution',
    'Footwear & Accessories',
    'Furnishings, Fixtures & Appliances',
    'Gambling',
    'Gold',
    'Grocery Stores',
    'Health Information Services',
    'Healthcare Plans',
    'Home Improvement Retail',
    'Household & Personal Products',
    'Industrial Distribution',
    'Information Technology Services',
    'Infrastructure Operations',
    'Insurance - Diversified',
    'Insurance - Life',
    'Insurance - Property & Casualty',
    'Insurance - Reinsurance',
    'Insurance - Specialty',
    'Insurance Brokers',
    'Integrated Freight & Logistics',
    'Internet Content & Information',
    'Internet Retail',
    'Leisure',
    'Lodging',
    'Lumber & Wood Production',
    'Luxury Goods',
    'Marine Shipping',
    'Medical Care Facilities',
    'Medical Devices',
    'Medical Distribution',
    'Medical Instruments & Supplies',
    'Metal Fabrication',
    'Mortgage Finance',
    'Oil & Gas Drilling',
    'Oil & Gas E&P',
    'Oil & Gas Equipment & Services',
    'Oil & Gas Integrated',
    'Oil & Gas Midstream',
    'Oil & Gas Refining & Marketing',
    'Other Industrial Metals & Mining',
    'Other Precious Metals & Mining',
    'Packaged Foods',
    'Packaging & Containers',
    'Paper & Paper Products',
    'Personal Services',
    'Pharmaceutical Retailers',
    'Pollution & Treatment Controls',
    'Publishing',
    'REIT - Diversified',
    'REIT - Healthcare Facilities',
    'REIT - Hotel & Motel',
    'REIT - Industrial',
    'REIT - Mortgage',
    'REIT - Office',
    'REIT - Residential',
    'REIT - Retail',
    'REIT - Specialty',
    'Railroads',
    'Real Estate - Development',
    'Real Estate - Diversified',
    'Real Estate Services',
    'Recreational Vehicles',
    'Rental & Leasing Services',
    'Residential Construction',
    'Resorts & Casinos',
    'Restaurants',
    'Scientific & Technical Instruments',
    'Security & Protection Services',
    'Semiconductor Equipment & Materials',
    'Semiconductors',
    'Shell Companies',
    'Silver',
    'Software - Application',
    'Software - Infrastructure',
    'Solar',
    'Specialty Business Services',
    'Specialty Chemicals',
    'Specialty Industrial Machinery',
    'Specialty Retail',
    'Staffing & Employment Services',
    'Steel',
    'Telecom Services',
    'Textile Manufacturing',
    'Thermal Coal',
    'Tobacco',
    'Tools & Accessories',
    'Travel Services',
    'Trucking',
    'Uranium',
    'Utilities - Diversified',
    'Utilities - Independent Power Producers',
    'Utilities - Regulated Electric',
    'Utilities - Regulated Gas',
    'Utilities - Regulated Water',
    'Utilities - Renewable',
    'Waste Management'
]


def sector_to_index(_sector: str) -> int:
    try:
        return SECTORS_IN_ORDER.index(_sector)
    except ValueError:
        return -1


def index_to_sector(_index: int) -> str:
    if _index == -1:
        return "UNKNOWN"
    return SECTORS_IN_ORDER[_index]


def index_to_industry(_index: int) -> str:
    if _index == -1:
        return "UNKNOWN"
    return INDUSTRIES_IN_ORDER[_index]


def industry_to_index(_industry: str) -> int:
    try:
        return INDUSTRIES_IN_ORDER.index(_industry)
    except ValueError:
        return -1


class Sectors:

    def __init__(self,
                 sectors: set = None,
                 industries: set = None):
        if sectors:
            self.sectors = sectors
        else:
            self.sectors = set()
        if industries:
            self.industries = industries
        else:
            self.industries = set()

    def add_sector(self, sector: str):
        if sector is not None:
            self.sectors.add(sector)

    def add_industry(self, industry: str):
        if industry is not None:
            self.industries.add(industry)

    def to_dicts(self) -> {}:
        return {
            "sectors": list(self.sectors),
            "industries": list(self.industries),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dicts())

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return Sectors(set(data["sectors"]), set(data["industries"]))

