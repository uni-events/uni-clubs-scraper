from helpers import *
import re
import requests
from urllib.parse import unquote

# some constants
club_names_link = "https://arc-discovery.linkupevents.com"
club_page_link = "https://arc-discovery.linkupevents.com/club/"


# gets a list of all club names available on arc website
def get_club_list():
    # get raw html code from arc club list page
    html_code = get_html(club_names_link)
    # find lines with club names
    matches = re.findall(r"<h3 class=\".*?\">.*?<\/h3>", html_code)
    # clean club names and store in array
    club_names = []
    for match in matches:
        match = re.sub(r"<span class=\".*?\">.*?<\/span>", "", match)
        match = re.sub(r"<h3 class=\".*\">", "", match)
        match = re.sub(r"<\/h3>", "", match)
        match = re.sub(r"&amp;", "&", match)
        club_names.append(match)
    return club_names


# takes in a list of club names and returns a dictionary of data for each club
def get_all_club_pages(club_list):
    all_club_data = []
    # for each club get data and append to all_club_data
    for club in club_list:
        clean_name = club.replace(" ", "%20")
        response = requests.get(f"{club_page_link}/{clean_name}")
        if response.status_code == 200:
            print(f"fetched data for {club}")
            response_json = get_club_data(str(unquote(response.content)))
            all_club_data.append(response_json)
        else:
            print(
                f"error {response.status_code} reached while fetching data for {club}"
            )
    return all_club_data


def main():
    club_list = get_club_list()
    print("COMPLETED: got all club names")
    club_data = get_all_club_pages(club_list)
    print("COMPLETED: got all club data")
    write_to_file(club_list, "./data/all_club_names.json")
    write_to_file(club_data, "./data/all_club_data.json")
    print("COMPLETED: stored all club data in files")


if __name__ == "__main__":
    main()
