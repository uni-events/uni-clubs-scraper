from helperFunctions import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import codecs
import re
from webdriver_manager.chrome import ChromeDriverManager
import requests
import json
from datetime import date
from urllib.parse import unquote


def GetHTML(link):
    chrome_options = webdriver.ChromeOptions()
    # load html preview without images
    pref = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", pref)

    driver = webdriver.Chrome(
        options=chrome_options,
        service=Service(ChromeDriverManager().install()))

    wait = WebDriverWait(driver, 60)

    driver.get(link)

    get_url = driver.current_urls

    wait.until(EC.url_to_be(link))

    if get_url == link:

        page_source = driver.page_source
        driver.quit()
        writeToFileHTML(page_source)
        return page_source


def cleanFileCode():
    f = open("code.txt", "r")
    htmlCode = f.read()
    soup = BeautifulSoup(htmlCode, features="html.parser")
    htmlCode = soup.decode(htmlCode)
    f = open("code.txt", "w")
    f.write(htmlCode)


def getFileData(file_name):
    # open and read the file after the overwriting:
    f = open(file_name, "r")
    data = f.read()
    f.close()
    return data


def writeToFileHTML(htmlCode):
    soup = BeautifulSoup(htmlCode, features="html.parser")
    htmlCode = soup.decode(htmlCode)
    f = open("code.txt", "w")
    f.write(htmlCode)
    f.close()


# FindMatchesClubNames
# params: htmlCode ( raw html code *not decoded )
# returns: club_names ( list of club names )
def FindMatchesClubNames(htmlCode):
    matches = re.findall(r"<h3 class=\".*?\">.*?<\/h3>", htmlCode)
    club_names = []
    for match in matches:
        match = re.sub(r"<span class=\".*?\">.*?<\/span>", "", match)
        match = re.sub(r"<h3 class=\".*\">", "", match)
        match = re.sub(r"<\/h3>", "", match)
        match = re.sub(r"&amp;", "&", match)
        club_names.append(match)
    return club_names


def LogErrors(file_name, error_message, data_to_log):
    today = date.today()
    with open(f"logs/{today}-{file_name}", "w") as log_file:
        log_message = {
            "error": error_message, "data": data_to_log}
        json.dump(log_message, log_file)
        print(f"logged errors in file {log_file.name}")
    return True


def FetchClubPage(club_names, api):
    bad_requests = []
    json_data = []
    with open("data/clubData.json", "w") as file:
        file.write("[")
    for name in club_names:
        response = requests.get(f"{api}/{name}")
        if response.status_code == 200:
            print(f"fetched data for {name}")
            response_json = getJSONfromHTML(str(response.content))
            json_data.append(response_json)
        else:
            print(
                f"error reached with request: {response.status_code} while fetching data for {name}")
            bad_requests.append(name)

    if len(bad_requests) > 0:
        print(
            f"experience issues while collecting some clubs data")
        LogErrors("ClubData.json",
                  "error reached with following club names", bad_requests)
    # gets rid of last "," in file that breaks json
    with open('data/clubData.json', 'rb+') as file:
        file.seek(-1, 2)
        file.truncate()
    with open("data/clubData.json", "a") as file:
        file.write("]")
    return json_data


def cleanBrokenJSON():
    broken_file = open("data/clubData.json", "rt")
    data = broken_file.read()
    data = data.replace(r"\'", r"'")
    data = data.replace("\\\\\"", "\\\"")
    # unicodeescape errors fixed after prev replace
    data = data.replace("\\x", "\\\\x")
    broken_file.close()
    broken_file = open("data/clubData.json", "wt")
    broken_file.write(data)
    broken_file.close()


def GetClubData():
    htmlCode = getFileData("rawClubDataHTML.txt")
    club_names = FindMatchesClubNames(htmlCode)
    club_names = CleanClubNameURLStr(club_names)
    FetchClubPage(
        club_names, "https://arc-discovery.linkupevents.com/club")
    cleanBrokenJSON()
    # WriteJsonToFile(json_data, "data/clubData.json")


def main():
    GetClubData()
    # cleanBrokenJSON()


if __name__ == "__main__":
    main()
