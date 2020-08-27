import json
import requests
from eu4 import app, log
import xml.etree.ElementTree as ET


def xml_map_to_json(xml):
    achiev_map = {}
    root = ET.fromstring(xml)
    achievements = root.find('achievements')
    
    for achievement in achievements:
        key = achievement.find('apiname').text
        value = achievement.find('name').text.lower()
        achiev_map[value] = key

    return achiev_map


def correct_errors(data):
    errors2 = [
        {
            "bad": " i\u2019ll graze my horse here.. and here\u2026",
            "good": "i'll graze my horse here.. and here..."
        },
        {
            "good": 'one faith!',
            "bad": "one faith"
        },
        {
            "good": "why is the rûm gone!?",
            "bad": "why is the r\u00fbm gone!?"
        }
    ]

    errors = {
        " i\u2019ll graze my horse here.. and here\u2026": {
            "good": "i'll graze my horse here.. and here..."
        },
        "one faith": {
            "good": 'one faith!'
        },
        "why is the r\u00fbm gone!?": {
            "good": "why is the rûm gone!?"
        }
    }

    output = {}
    for key, value in data.items():
        if key in errors:
            # log.info(f"Raplacing: {key} with {errors.get(key).get('good')}")
            key = errors.get(key).get("good")

        output[key] = value

    # for error in errors2:
    #     data[error.get("good")] = data[error.get("bad")]
        # del data[error.get("bad")]

    return output


def get_steam_data():
    steam_id = app.config.get("STEAM_ID")
    steam_appid = "236850"
    url = f"https://steamcommunity.com/profiles/{steam_id}/stats/{steam_appid}/?xml=1"

    try:
        response = requests.get(url=url, timeout=150)
    except Exception as err:
        log.error(f"{err}|Error during request. URL:{url}, timeout=150")
        return {"data":{}, "error": {f"Error during steam call request."}}

    try:
        json_map = xml_map_to_json(response.content)
    except Exception as err:
        log.error(f"{err}|Coudnt'd make json from the steam output. Received data: " \
            f", playerstats/achievements is tried to extract", )
        # Output can be very long:
        # log.debug(f"response.content={response.content}")

        return {"data":{}, "error": {f"Error during steam call request."}}

    output = correct_errors(json_map)

    return output


def get_player_stats(steam_id):
    steam_appid = "236850"
    base_URL = "http://api.steampowered.com"
    target_URL = "ISteamUserStats/GetPlayerAchievements/v0001/"

    url = f"{base_URL}/{target_URL}"
    params = {
        "appid": steam_appid,
        "key": app.config.get("STEAM_KEY"),
        "steamid": steam_id
    }

    try:
        response = requests.get(url=url, params=params, timeout=150)
    except Exception as err:
        log.error(f"{err}|Error during request. URL:{url}, params:{params}, timeout=150")
        return {"data":{}, "error": {f"Error during steam call request."}}


    try:
        stats = response.json()['playerstats']['achievements']
    except Exception as err:
        log.error(f"{err}|Coudnt'd make json from the steam output. Received data: " \
            f"{response.content}, playerstats/achievements is tried to extract", )
        return {"data":{}, "error": {f"Error during steam call request."}}

    return stats


def map_paradox_with_steam(paradox_data, steam_data):
    log.debug("map_paradox_with_steam")
    output = []
    for achiev in paradox_data:
        achiev["steam_name"] = steam_data.get(achiev["name"])
        if not achiev["steam_name"]:
            log.error(f"Coudn't get achievement map for {achiev}")
        output.append(achiev)

    return output


def map_user_with_steam(data_steam, data_user):
    log.debug("map_user_with_steam")
    # mistakes = {"achievement_abu_bakr_IIs_ambition": "Abu Bakr II’s Ambition"}

    output = []
    found = False
    for achiev in data_steam:
        for achiev_user in data_user:
            if achiev.get("steam_name") == achiev_user.get("apiname"):
                achiev["achieved"] = achiev_user.get("achieved")
                achiev["unlocktime"] = achiev_user.get("unlocktime")
                found = True

        if not found:
            log.error(f"Coudn\'t find user achiev for {achiev}")

        output.append(achiev)

    return output
