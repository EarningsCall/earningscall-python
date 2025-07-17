#!/usr/bin/env python3
"""
Script to download slides for a given company and quarter
"""

import earningscall


def test_slides_api():
    """Test the new slides API functionality"""

    # Get a company
    company = earningscall.get_company("MSFT")
    if not company:
        print("Could not find MSFT company")
        return

    print(f"Testing slides API for {company.company_info.name}")

    try:
        # Try to download slides for Q1 2025 (using demo data)
        slide_file = company.download_slide_deck(year=2025, quarter=1)
        if slide_file:
            print(f"Successfully downloaded slides: {slide_file}")
        else:
            print("No slides available for the requested quarter")

    except Exception as e:
        print(f"Error downloading slides: {e}")
        # This is expected for demo account or if slides aren't available


if __name__ == "__main__":
    test_slides_api()
