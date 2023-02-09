import re
import json


def CleanClubNameStr(club_name_raw):
    club_name_clean = []
    for name in club_name_raw:
        name = name.lower()
        name = name.replace(' ', '_')
        name = name.replace('&amp;', 'and')
        club_name_clean.append(name)
    return club_name_clean


def CleanClubNameURLStr(club_name_raw):
    club_name_clean = []
    for name in club_name_raw:
        name = name.replace(' ', '%20')
        club_name_clean.append(name)
    return club_name_clean


def getJSONfromHTML(html):
    club_json_data = re.search(
        r"<script\sid=\"__NEXT_DATA__\"\stype=\"application/json\">.*?</script>", html)
    # club_json_data = json.loads(club_json_data.group())
    club_json_data = re.sub(
        r"<script id=\"__NEXT_DATA__\" type=\"application/json\">", "", club_json_data.group())
    club_json_data = re.sub(
        r"</script>", "", club_json_data)

    with open("data/clubData.json", "a") as file:
        file.write(club_json_data)
        file.write(",")

    # club_json_data = json.loads(rf'{club_json_data}')
    return club_json_data
