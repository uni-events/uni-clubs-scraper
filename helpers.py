from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import json


# takes a link to a page and returns the html code of the page
def get_html(link):
    # start the browser
    chrome_options = webdriver.ChromeOptions()
    # load html preview without images
    pref = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", pref)
    driver = webdriver.Chrome(
        options=chrome_options, service=Service(ChromeDriverManager().install())
    )
    # get the html code
    driver.get(link)
    page_source = driver.page_source
    driver.quit()
    return page_source


# takes the html code of a club page and returns the json data of that club
def get_club_data(html):
    # get the json data stored in the script tag
    club_json_data = re.search(
        r"<script\sid=\"__NEXT_DATA__\"\stype=\"application/json\">.*?</script>", html
    )
    club_json_data = re.sub(
        r"<script id=\"__NEXT_DATA__\" type=\"application/json\">",
        "",
        club_json_data.group(),
    )
    club_json_data = re.sub(r"</script>", "", club_json_data)
    # convert string to json object
    club_json_data = json.loads(club_json_data)
    return club_json_data


# write json data with indents to a specified file
def write_to_file(data, file_name):
    json_data = json.dumps(data, indent=4)
    with open(file_name, "w") as f:
        f.write(json_data)
