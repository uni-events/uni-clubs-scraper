import requests
import json
from datetime import date
from bs4 import BeautifulSoup


def FetchClubData(club_names, api):
    # cleans the existing data in the file
    with open('data/clubData.json', 'w') as file:
        file.write("[]")
        file.close()

    with open("data/clubData.json", "r") as file:
        data = json.load(file)
    bad_requests = []

    for name in club_names:
        response = requests.get(f"{api}", params={"id": name})
        if response.status_code == 200:
            data.append(response.json())
            print(f"fetched data for {name}")
        else:
            bad_requests.append(name)
            print(
                f"error reached with request: {response.status_code} while fetching data for {name}")

    with open("data/clubData.json", "w") as file:
        json.dump(data, file)
        file.close()
    print("completed fetching club data")
    if len(bad_requests) > 0:
        print(
            f"experience issues while collecting some clubs data")
        LogErrors("ClubData.json",
                  "error reached with following club names", bad_requests)


def LogErrors(file_name, error_message, data_to_log):
    today = date.today()
    with open(f"logs/{today}-{file_name}", "w") as log_file:
        log_message = {
            "error": error_message, "data": data_to_log}
        json.dump(log_message, log_file)
        print(f"logged errors in file {log_file.name}")
    return True


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


def WriteJsonToFile(json_data, file_name):
    with open(f"{file_name}", "w") as file:
        file.write("[]")
        json.dump(json_data, file)
        print(f"wrote data to file: {file.name}")
