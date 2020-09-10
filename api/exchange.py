"""Contains all the functions to retrieve the exchange rates of all the possible sources.

API key and Token are retrieved as env vars.
"""
import os
import requests
import bs4

BANXICO_TOKEN = os.getenv("BANXICO_TOKEN")
FIXER_API_KEY = os.getenv("FIXER_API_KEY")

BANXICO_URL = f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno?token={BANXICO_TOKEN}"
DOF_URL = "https://www.banxico.org.mx/tipcamb/tipCamMIAction.do"
FIXER_URL = (
    f"http://data.fixer.io/api/latest?access_key={FIXER_API_KEY}&symbols=MXN,USD"
)


def get_sources():
    """Returns a dictionary with all the sources for the exchange rate.

    In case of an error it returns an empty dict for the source.
    """
    # using this map to allow new sources in an easy way
    return {
        "diario_oficial": get_dof_source(),
        "fixer": get_fixer_source(),
        "banxico": get_banxico_source(),
    }


def get_dof_source():
    """Returns the latest exchange rate from Diario Oficial de la Federacion."""
    response = requests.get(DOF_URL)
    if response.status_code != 200:
        return _empty_dict()

    data = bs4.BeautifulSoup(response.text, "html.parser")

    head_columns = data.find_all(class_="renglonTituloColumnas")
    table = head_columns[0].parent

    for element in table:
        if (
            element.name == "tr"
            and element.attrs
            and element.attrs["class"][0] == "renglonNon"
        ):
            value = float(element.contents[5].text.strip())
            value_date = element.contents[1].text.strip()
            return {"value": value, "source_date": value_date}


def get_fixer_source():
    """Returns the latest exchange rate Fixer.

    Unfortunately the convert endpoint is not available for a free account
     so a simple convert is needed.
    """
    response = requests.get(FIXER_URL)
    if response.status_code != 200:
        return _empty_dict()
    json_response = response.json()

    if not json_response["success"]:
        return _empty_dict()

    # to convert from USD to MXN
    mxn = json_response["rates"]["MXN"]
    usd = json_response["rates"]["USD"]
    value = mxn / usd

    value_date = json_response["date"]
    return {"value": value, "source_date": value_date}


def get_banxico_source():
    """Returns the latest exchange rate from Banxico"""
    response = requests.get(BANXICO_URL)
    if response.status_code != 200:
        return _empty_dict()

    json_response = response.json()
    series = json_response["bmx"]["series"]
    value = series[0]["datos"][0]["dato"]
    value_date = series[0]["datos"][0]["fecha"]
    return {"value": float(value), "source_date": value_date}


def _empty_dict():
    return {"value": 0.0, "source_date": None}
