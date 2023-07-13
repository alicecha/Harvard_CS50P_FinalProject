import pytest
import json
import requests
from project import Park, validate, call_api, fetch_hikes, create_output

import os
from dotenv import load_dotenv
load_dotenv()
NPS_API_KEY = os.getenv('NPS_API_KEY')

"""
Tests case insensivity, returns titlecased name and correct code, exits when name does not exist
"""
def test_validate():
    assert validate("joshua tree")["name"] == "Joshua Tree"
    assert validate("JOSHUA TREE")["name"] == "Joshua Tree"
    assert validate("Joshua Tree")["code"] == "JOTR"
    with pytest.raises(SystemExit):
        validate("GrandCanyon")

"""
Tests returns the correct data from API
"""
def test_call_api():
    park1 = Park("Joshua Tree", "JOTR")
    park2 = Park("Unknown", "UNKN")
    assert call_api(park1) == requests.get(f"https://developer.nps.gov/api/v1/thingstodo?parkCode=JOTR&q=BFF8C027-7C8F-480B-A5F8-CD8CE490BFBA&api_key={NPS_API_KEY}").json()
    assert call_api(park2)["data"] == []

"""
Tests fetch_hikes returns list of hikes with name, duration, description, seasons and url, otherwise exits when no result found
"""
def test_fetch_hikes():
    hikes = fetch_hikes(requests.get(f"https://developer.nps.gov/api/v1/thingstodo?parkCode=JOTR&q=BFF8C027-7C8F-480B-A5F8-CD8CE490BFBA&api_key={NPS_API_KEY}").json())
    assert hikes
    for hike in hikes:
        assert "name", "duration" in hike
        assert "seasons", "description" in hike
        assert "url" in hike
    with pytest.raises(SystemExit):
        fetch_hikes(requests.get(f"https://developer.nps.gov/api/v1/thingstodo?parkCode=UNKN&q=BFF8C027-7C8F-480B-A5F8-CD8CE490BFBA&api_key={NPS_API_KEY}").json())

"""
Tests that pdf, csv and table txt get created with create_output
"""
def test_create_output():
    park = Park("Joshua Tree", "JOTR")
    hikes = fetch_hikes(call_api(park))
    assert os.path.isfile("./joshua_tree.pdf") == False
    create_output(park, hikes, "pdf")
    assert os.path.isfile("./joshua_tree.pdf")
    assert os.path.isfile("./joshua_tree.csv") == False
    create_output(park, hikes, "csv")
    assert os.path.isfile("./joshua_tree.csv")
    assert os.path.isfile("./joshua_tree.txt") == False
    create_output(park, hikes, "table")
    assert os.path.isfile("./joshua_tree.txt")
    os.remove("./joshua_tree.pdf")
    os.remove("./joshua_tree.csv")
    os.remove("./joshua_tree.txt")
    