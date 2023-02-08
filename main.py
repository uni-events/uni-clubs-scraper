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

    get_url = driver.current_url

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
    return f.read()


def writeToFileHTML(htmlCode):
    soup = BeautifulSoup(htmlCode, features="html.parser")
    htmlCode = soup.decode(htmlCode)
    f = open("code.txt", "w")
    f.write(htmlCode)


def GetClubNames(htmlCode):
    # regex = "<h3 class=\"mb-1 flex max-h-12 w-full items-center font-ProximaNovaMedium text-base line-clamp-1 md:line-clamp-2\">"
    soup = BeautifulSoup(htmlCode, features="html.parser")
    htmlCode = soup.decode(htmlCode)

    # pattern = r"<h3 class =\"mb-1 flex max-h-12 w-full items-center font-ProximaNovaMedium text-base line-clamp-1 md: line-clamp-2\">"
    # pattern = re.compile(pattern)
    matches = re.search(r"AD\ Space", htmlCode)
    print(matches)


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
        club_names.append(match)
    return club_names


def FetchClubData(club_names, api):
    f =
    for name in club_names:
        response = requests.get(f"{api}", params={"id": name})
        if response.status_code == 200:
            response.json()
        else:
            print(f"error reached with request: {response.status_code}")


def GetClubData():
    htmlCode = getFileData("rawClubDataHTML.txt")
    club_names = FindMatchesClubNames(htmlCode)
    club_names = CleanClubNameStr(club_names)
    FetchClubData(club_names, "https://api.linkupevents.com.au/unsw/club")


def main():
    GetClubData()


if __name__ == "__main__":
    main()
