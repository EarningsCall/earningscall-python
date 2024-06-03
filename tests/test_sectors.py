from earningscall.sectors import index_to_sector, index_to_industry, sector_to_index, industry_to_index


def test_unknown_sector():
    assert sector_to_index("Bad Sector") == -1


def test_unknown_sector_index():
    assert index_to_sector(-1) == "Unknown"


def test_unknown_industry():
    assert industry_to_index("Bad Industry") == -1


def test_unknown_industry_index():
    assert index_to_industry(-1) == "Unknown"
