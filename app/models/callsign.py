"""Callsign models."""
from typing import Optional

import pycountry
from pydantic import BaseModel, Field, validator


def _country_code_lookup(country_name: str) -> Optional[str]:
    """Attempt to get ISO country code from country name."""
    try:
        fuzzy_countries = pycountry.countries.search_fuzzy(country_name)
    except LookupError:
        return None
    else:
        return fuzzy_countries[0].alpha_2


class CallSign(BaseModel):
    """Callsign data returned by HamQTH API."""

    callsign: str
    nick: Optional[str]
    qth: Optional[str]
    country: Optional[str]
    adif: Optional[int]
    itu: Optional[int]
    cq: Optional[int]
    grid: Optional[str]
    adr_name: Optional[str]
    adr_city: Optional[str]
    adr_country: Optional[str]
    us_state: Optional[str]
    utc_offset: Optional[int]
    latitude: float = Field(type=Optional[float], ge=-90, le=90)
    longitude: float = Field(type=Optional[float], ge=-180, le=180)
    country_code: Optional[str] = None

    @validator("country_code", always=True)
    def set_country_code(cls, v, values):
        """Set ISO country code based on HamQTH country."""
        return _country_code_lookup(values["country"])

    @validator("callsign", always=True)
    def uppercase_callsign(cls, v, values):
        """Capitalize call sign."""
        return v.upper()
