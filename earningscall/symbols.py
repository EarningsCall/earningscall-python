import json
import logging
from collections import defaultdict
from typing import Optional, Iterator, List

from earningscall.api import get_symbols_v2, is_demo_account
from earningscall.errors import InsufficientApiAccessError
from earningscall.sectors import sector_to_index, industry_to_index, index_to_sector, index_to_industry

# WARNING: Add new indexes to the *END* of this list
EXCHANGES_IN_ORDER = [
    "NYSE",
    "NASDAQ",
    "AMEX",
    "TSX",
    "TSXV",
    "OTC",
    "LSE",
    "CBOE",
    "STO",
]

log = logging.getLogger(__file__)


def exchange_to_index(_exchange: Optional[str]) -> int:
    if not _exchange:
        return -1
    try:
        return EXCHANGES_IN_ORDER.index(_exchange)
    except ValueError:
        return -1


def index_to_exchange(_index: int) -> str:
    if _index == -1:
        return "UNKNOWN"
    try:
        return EXCHANGES_IN_ORDER[_index]
    except IndexError:
        return "UNKNOWN"


security_type_pattern = {
    "NASDAQ": r" - .*$",
    "NYSE": r" (Common Stock|Warrants)$",
    "AMEX": r" (Common Stock|Warrants)$",
}


class CompanyInfo:

    exchange: Optional[str]
    symbol: Optional[str]
    name: Optional[str]
    security_name: Optional[str]
    sector: Optional[str]
    industry: Optional[str]

    def __init__(self, **kwargs):
        self.exchange = None
        self.symbol = None
        self.name = None
        self.sector = None
        self.industry = None
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def __str__(self):
        return f"({self.exchange}: {self.symbol} - {self.name})"

    def to_json(self):
        return json.dumps(self.__dict__)

    def to_txt_row(self):
        return [
            str(exchange_to_index(self.exchange)),
            self.symbol,
            self.name,
        ]

    def to_txt_v2_row(self):
        return [
            str(exchange_to_index(self.exchange)),
            self.symbol,
            self.name,
            str(sector_to_index(self.sector)),
            str(industry_to_index(self.industry)),
        ]

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        k = self.__dict__.keys()
        sorted(k)
        return sum(map(lambda x: f"{x}-{self.__dict__[x]}".__hash__(), k))

    def exchange_symbol(self):
        return f"{self.exchange}_{self.symbol}"


class Symbols:

    def __init__(self):
        self.exchanges = set()
        self.by_name = defaultdict(set)
        self.by_exchange_and_sym = {}

    def add(self, _sym: CompanyInfo):
        # size_before = len(self.by_exchange_and_sym)
        self.exchanges.add(_sym.exchange)
        self.by_name[_sym.name].add(_sym)
        self.by_exchange_and_sym[f"{_sym.exchange}_{_sym.symbol}"] = _sym
        # if len(self.by_exchange_and_sym) == size_before:
        #     log.debug(f"Duplicate: {_sym}")

    def get_all(self) -> Iterator[CompanyInfo]:
        for _exchange_symbol, _symbol in self.by_exchange_and_sym.items():
            yield _symbol

    def get(self, _exchange: str, _symbol: str) -> CompanyInfo:
        return self.get_exchange_symbol(f"{_exchange}_{_symbol}")

    def get_exchange_symbol(self, exchange_symbol: str) -> CompanyInfo:
        return self.by_exchange_and_sym[exchange_symbol]

    def lookup_company(self, symbol: str, exchange: Optional[str] = None) -> Optional[CompanyInfo]:
        if exchange:
            return self.get(exchange, symbol.upper())
        for exchange in EXCHANGES_IN_ORDER:
            try:
                _symbol = self.get(exchange, symbol.upper())
                if _symbol:
                    return _symbol
            except KeyError:
                pass
        if is_demo_account():
            raise InsufficientApiAccessError(
                f"\"{symbol}\" requires an API Key for access.  To get your API Key,"
                f" see: https://earningscall.biz/api-pricing"
            )
        return None

    def remove_exchange_symbol(self, exchange_symbol: str):
        _symbol = self.by_exchange_and_sym[exchange_symbol]
        del self.by_name[_symbol.name]
        del self.by_exchange_and_sym[exchange_symbol]

    @staticmethod
    def remove_keys(symbol_as_dict: dict, keys_to_remove: set):
        return {key: value for key, value in symbol_as_dict.items() if key not in keys_to_remove}

    def without_security_names(self) -> List[dict]:
        return [
            self.remove_keys(symbol_as_dict, {"security_name", "sector", "industry"})
            for symbol_as_dict in self.to_dicts()
        ]

    def to_dicts(self) -> List[dict]:
        return [__symbol.__dict__ for __symbol in self.get_all()]

    def to_json(self, remove_security_names: bool = False) -> str:
        if remove_security_names:
            return json.dumps(self.without_security_names())
        return json.dumps(self.to_dicts())

    def to_txt_v2(self) -> str:
        exchange_symbol_names = [__symbol.to_txt_v2_row() for __symbol in self.get_all()]
        sorted_rows = sorted(exchange_symbol_names, key=lambda row: row[1])
        return "\n".join(["\t".join(row) for row in sorted_rows])

    @staticmethod
    def from_json(json_str):
        __symbols = Symbols()
        for item in json.loads(json_str):
            __symbols.add(CompanyInfo(**item))
        return __symbols

    @staticmethod
    def from_txt_v2(txt_str):
        __symbols = Symbols()
        for line in txt_str.split("\n"):
            _exchange_index, _symbol, _name, _sector_index, _industry_index = line.split("\t")
            __symbols.add(
                CompanyInfo(
                    exchange=index_to_exchange(int(_exchange_index)),
                    symbol=_symbol,
                    name=_name,
                    sector=index_to_sector(int(_sector_index)),
                    industry=index_to_industry(int(_industry_index)),
                )
            )
        return __symbols

    @staticmethod
    def load_txt_v2():
        return Symbols.from_txt_v2(get_symbols_v2())

    def __iter__(self):
        for _exchange_symbol, _symbol in self.by_exchange_and_sym.items():
            yield _symbol

    def __len__(self):
        return len(self.by_exchange_and_sym)


def load_symbols() -> Symbols:
    return Symbols.load_txt_v2()


_symbols = None


def get_symbols() -> Symbols:
    global _symbols
    if not _symbols:
        _symbols = load_symbols()
    return _symbols


def clear_symbols():
    global _symbols
    _symbols = None
