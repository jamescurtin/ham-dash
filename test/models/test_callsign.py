import pytest

from app.models.callsign import CallSign, _country_code_lookup

SOME_CALLSIGN_DATA = {
    "callsign": "w1ze",
    "qth": "Mattapoisett, MA",
    "nick": "Irving",
    "country": "United States",
    "adif": 291,
    "itu": 8,
    "cq": 5,
    "grid": "FN41op",
    "adr_name": "Irving Vermilya",
    "adr_city": "Mattapoisett",
    "adr_country": "United States",
    "us_state": "MA",
    "utc_offset": -5,
    "latitude": 41.662191,
    "longitude": -70.810344,
}


@pytest.mark.parametrize(
    ["country", "expected", "type"],
    [
        ("Germany", "DE", "Single Match"),
        ("United States", "US", "Multiple Match"),
        ("Not a Country", None, "No Matches"),
    ],
)
def test__country_code_lookup__exact_match__successful_lookup(country, expected, type):
    actual = _country_code_lookup(country)
    assert expected == actual, type


def test_CallSign__validator__parses_country_code():
    call_sign = CallSign(**SOME_CALLSIGN_DATA)
    assert call_sign.country_code == "US"


def test_CallSign__validator__uppercase_callsign():
    call_sign = CallSign(**SOME_CALLSIGN_DATA)
    assert call_sign.callsign == SOME_CALLSIGN_DATA["callsign"].upper()


def test_CallSign__validator__missing_latlng():
    call_sign_data = SOME_CALLSIGN_DATA.copy()
    del call_sign_data["latitude"]
    del call_sign_data["longitude"]

    call_sign = CallSign(**call_sign_data)

    assert call_sign.latitude is None
    assert call_sign.longitude is None
