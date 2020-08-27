from eu4 import app
import json
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


EU4_URL = "https://eu4.paradoxwikis.com"
DIFFICULT = {
    "VE": "Very Easy",
    "E": "Easy",
    "M": "Medium",
    "H": "Hard",
    "VH": "Very Hard",
    "I": "Insane",
    "UC": "Uncategorized"
}


def fetch_acievements_html_table():
    """Return extracted from forum html table"""
    data = requests.get(f"{EU4_URL}/Achievements")
    soup = BeautifulSoup(data.content.decode("utf-8"), 'html.parser')
    table = soup.find('table', attrs={'class': 'mildtable sortable plainlist'})

    return table.find_all('tr')


def html_to_dict(table):
    """Turn html table into list of dicts"""
    output = []
    index=0
    for row in table:
        achievement = {
            "id": index,
            "name": "",
            "title": "",
            "description": "",
            "image": "",
            "starting_conditions": [],
            "requirements": [],
            "notes": "",
            "version": "",
            "difficult": ""
        }
        columns = []

        # change <td> into columns
        for column in row.find_all('td'):
            columns.append(column)

        if columns:
            achievement['name'] = list(columns[0].div.div)[0].text.strip().lower()
            achievement['title'] = list(columns[0].div.div)[0].text.strip()
            achievement['description'] = list(columns[0].div.div)[1].text.strip()
            achievement['image_url'] = f"{EU4_URL}{columns[0].find('img')['src']}"
            achievement['starting_conditions'].extend([x for x in columns[1].text.strip().split("\n") if x])
            achievement['requirements'].extend([x for x in columns[2].text.strip().split("\n") if x])
            achievement['notes'] = columns[3].text.strip()
            achievement['version'] = columns[5].text.strip()
            achievement['difficult'] = DIFFICULT[columns[6].text.strip()]

        if achievement['name']:
            output.append(achievement)

        index += 1

    return output


def get_paradox_data():

    html_table = fetch_acievements_html_table()

    achievements_list = html_to_dict(html_table)

    return achievements_list
