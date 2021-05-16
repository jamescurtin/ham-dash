import logging
from functools import lru_cache
from typing import Mapping, Optional, Union

import call_to_dxcc
from fastapi import APIRouter
from hamqth import HamQTHClient
from hamqth.exceptions import HamQTHClientError

from app.core.config import settings
from app.core.utils import etree_to_dict
from app.models.callsign import CallSign

router = APIRouter()
_hamqth_client: Optional[HamQTHClient] = None
_logger = logging.getLogger(__name__)

HAM_QTH_PREFIX = "{https://www.hamqth.com}"


def _get_hamqh_client() -> HamQTHClient:
    global _hamqth_client
    if _hamqth_client is None or not _hamqth_client.is_authenticated:
        _hamqth_client = HamQTHClient()
        _hamqth_client.authenticate(
            settings.HAM_QTH_USERNAME, settings.HAM_QTH_PASSWORD.get_secret_value()
        )
    return _hamqth_client


def _get_fallback_country_information(callsign: str) -> str:
    try:
        country, _, _ = call_to_dxcc.data_for_call(callsign)
    except call_to_dxcc.DxccUnknownException:
        country = "Unknown"
    return country


@lru_cache
def fetch_callsign_data(callsign: str) -> Mapping[str, Union[str, float]]:
    client = _get_hamqh_client()
    try:
        callsign_xml_data = client.search_callsign(callsign)
    except HamQTHClientError:
        _logger.info(f"Callsign {callsign} could not be found")
        country = _get_fallback_country_information(callsign)
        callsign_data = {"callsign": callsign, "country": country}
    else:
        raw_callsign_data = etree_to_dict(callsign_xml_data)
        callsign_data = {
            key.replace(HAM_QTH_PREFIX, ""): value
            for key, value in raw_callsign_data[f"{HAM_QTH_PREFIX}search"].items()
        }
    return callsign_data


@router.get("/callsign/{callsign}")
def callsign(callsign: str) -> Optional[CallSign]:
    """Get publically available data for a call sign."""
    callsign_data = fetch_callsign_data(callsign)
    return CallSign(**callsign_data)
