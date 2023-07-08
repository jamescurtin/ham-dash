"""Callsign models."""
from typing import Annotated, Optional

import pycountry
from pydantic import BaseModel, Field, FieldValidationInfo, field_validator


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
    nick: Optional[str] = None
    qth: Optional[str] = None
    country: Optional[str] = None
    adif: Optional[int] = None
    itu: Optional[int] = None
    cq: Optional[int] = None
    grid: Optional[str] = None
    adr_name: Optional[str] = None
    adr_city: Optional[str] = None
    adr_country: Optional[str] = None
    us_state: Optional[str] = None
    utc_offset: Optional[int] = None
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)
    country_code: Annotated[str | None, Field(validate_default=True)] = None

    @field_validator("country_code")
    def set_country_code(cls, _, info: FieldValidationInfo):
        """Set ISO country code based on HamQTH country."""
        return _country_code_lookup(info.data["country"])

    @field_validator("callsign")
    def uppercase_callsign(cls, v):
        """Capitalize call sign."""
        return v.upper()
