import xml.etree.ElementTree as ET

import pytest
from hamqth.exceptions import HamQTHClientError
from starlette.testclient import TestClient

from app.api.endpoints import hamqth

AUTH_URL = "https://www.hamqth.com/xml.php"
SOME_AUTH_RESPONSE = """
    <?xml version="1.0"?>
    <HamQTH version="2.7" xmlns="https://www.hamqth.com">
    <session>
    <session_id>09b0ae90050be03c452ad235a1f2915ad684393c</session_id>
    </session>
    </HamQTH>
    """.strip()

SOME_CALLSIGN_XML_TEXT = """<?xml version="1.0"?>
<HamQTH version="2.8" xmlns="https://www.hamqth.com">
    <search>
        <callsign>OK2CQR</callsign>
        <nick>Petr</nick>
        <qth>Neratovice</qth>
        <country>Czech Republic</country>
        <adif>503</adif>
        <itu>28</itu>
        <cq>15</cq>
        <grid>JO70GG</grid>
        <adr_name>Petr Hlozek</adr_name>
        <adr_street1>17. listopadu 1065</adr_street1>
        <adr_city>Neratovice</adr_city>
        <adr_zip>27711</adr_zip>
        <adr_country>Czech Republic</adr_country>
        <adr_adif>503</adr_adif>
        <district>BME</district>
        <lotw>Y</lotw>
        <qsldirect>Y</qsldirect>
        <qsl>Y</qsl>
        <eqsl>Y</eqsl>
        <email>petr@ok2cqr.com</email>
        <jabber>petr@ok2cqr.com</jabber>
        <skype>PetrHH</skype>
        <birth_year>1982</birth_year>
        <lic_year>1998</lic_year>
        <web>http://www.ok2cqr.com</web>
        <facebook>https://www.facebook.com/petr.hlozek</facebook>
        <twitter>https://twitter.com/ok2cqr</twitter>
        <linkedin>http://www.linkedin.com/pub/petr-hlo%C5%BEek/45/434/598</linkedin>
        <latitude>50.25344610000001</latitude>
        <longitude>14.515040999999997</longitude>
        <continent></continent>
        <utc_offset>-1</utc_offset>
        <picture>https://www.hamqth.com/userfiles/o/ok/ok2cqr/_header/header.jpg?ver=10</picture>
    </search>
</HamQTH>
    """.strip()


HAMQTH_NAMESPACE = {
    "hamqth": "https://www.hamqth.com",
}
SOME_CALLSIGN_XML = ET.fromstring(SOME_CALLSIGN_XML_TEXT).find(
    "hamqth:search", HAMQTH_NAMESPACE
)

EXPECTED_CALLSIGN_DICT = {
    "callsign": "OK2CQR",
    "nick": "Petr",
    "qth": "Neratovice",
    "country": "Czech Republic",
    "adif": "503",
    "itu": "28",
    "cq": "15",
    "grid": "JO70GG",
    "adr_name": "Petr Hlozek",
    "adr_street1": "17. listopadu 1065",
    "adr_city": "Neratovice",
    "adr_zip": "27711",
    "adr_country": "Czech Republic",
    "adr_adif": "503",
    "district": "BME",
    "lotw": "Y",
    "qsldirect": "Y",
    "qsl": "Y",
    "eqsl": "Y",
    "email": "petr@ok2cqr.com",
    "jabber": "petr@ok2cqr.com",
    "skype": "PetrHH",
    "birth_year": "1982",
    "lic_year": "1998",
    "web": "http://www.ok2cqr.com",
    "facebook": "https://www.facebook.com/petr.hlozek",
    "twitter": "https://twitter.com/ok2cqr",
    "linkedin": "http://www.linkedin.com/pub/petr-hlo%C5%BEek/45/434/598",
    "latitude": "50.25344610000001",
    "longitude": "14.515040999999997",
    "continent": None,
    "utc_offset": "-1",
    "picture": "https://www.hamqth.com/userfiles/o/ok/ok2cqr/_header/header.jpg?ver=10",
}


@pytest.fixture(autouse=True)
def clear_client():
    hamqth._hamqth_client = None


def test__get_hamqh_client__creates_authenticated_client(requests_mock):
    requests_mock.get(AUTH_URL, text=SOME_AUTH_RESPONSE)
    client = hamqth._get_hamqh_client()
    assert client.is_authenticated


def test__get_hamqh_client__caches_client(requests_mock):
    get_session_id_mock = requests_mock.get(AUTH_URL, text=SOME_AUTH_RESPONSE)
    hamqth._get_hamqh_client()
    hamqth._get_hamqh_client()
    assert get_session_id_mock.call_count == 1


def test_fetch_callsign_data__response__converts_to_dict(mocker):
    hamqth_client = mocker.Mock()
    hamqth_client.search_callsign = mocker.Mock(return_value=SOME_CALLSIGN_XML)
    mocker.patch(
        "app.api.endpoints.hamqth._get_hamqh_client", return_value=hamqth_client
    )
    assert hamqth.fetch_callsign_data("ok2cqr") == EXPECTED_CALLSIGN_DICT


def test_fetch_callsign_data__response__handles_exception(mocker):
    hamqth_client = mocker.Mock()
    hamqth_client.search_callsign = mocker.Mock(side_effect=HamQTHClientError)
    mocker.patch(
        "app.api.endpoints.hamqth._get_hamqh_client", return_value=hamqth_client
    )
    assert hamqth.fetch_callsign_data("98765notreal") == {
        "callsign": "98765notreal",
        "country": "Unknown",
    }


def test_callsign_endpoint__successful_response(testclient: TestClient, mocker):
    mocker.patch(
        "app.api.endpoints.hamqth.fetch_callsign_data",
        return_value=EXPECTED_CALLSIGN_DICT,
    )
    r = testclient.get(
        "/api/v1/hamqth/callsign/ok2cqr",
    )

    assert r.status_code == 200, r.text


@pytest.mark.parametrize(
    ["callsign", "country"],
    [("KC123", "United States of America"), ("M123", "England")],
)
def test__get_fallback_country_information__known_callsign__returns_correct_country(
    callsign,
    country,
):
    assert hamqth._get_fallback_country_information(callsign) == country
