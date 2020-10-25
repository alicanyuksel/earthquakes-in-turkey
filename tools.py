from bs4 import BeautifulSoup
import requests
import re
import json


def extract_from_web(file_name):
    """
    To scrape with bs4

    :param file_name: txt file name
    """
    # specify url
    url = 'http://www.koeri.boun.edu.tr/scripts/lst0.asp'

    # request html
    page = requests.get(url)

    # Parse html using BeautifulSoup, you can use a different parser like lxml
    soup = BeautifulSoup(page.content, "html.parser")

    # find searches the given tag (div) with given class attribute and returns the first match it finds
    all_text = soup.find('pre')

    # Extracting the text out of the div
    data_txt = open(file_name, "w", encoding="utf-8")
    data_txt.write(all_text.text)

    return "Data extracted !"


def clean_data(file_name):
    """
    To parse and clean the data with the regex
    :param file_name: txt file name
    """
    with open(file_name, "r+", encoding="utf-8") as fl:
        all_text = fl.read()

        # extract only earthquake data
        regex = re.compile("--------------\n(.*)\n{2}", re.MULTILINE | re.DOTALL)

        # to get the cleaned text
        text_cleaned = re.search(regex, all_text).group(1)

        # removes spaces from the location names to parse the data correctly
        # for example : YESILOVA-GEDIZ (KUTAHYA) will become YESILOVA-GEDIZ-(KUTAHYA).
        regex_location = re.compile(r"([a-zA-Z])(\s)([a-zA-Z()])")
        text_cleaned = re.sub(regex_location, r"\1-\3", text_cleaned)

        fl.seek(0)
        fl.write(text_cleaned)
        fl.truncate()

    return "Data cleaned !"


def create_json_file(file_name):
    """
    To parse the data unstructured in order to create a json file (structured data)

    :param file_name: txt file name
    """
    all_data = list()
    for line in open(file_name, "r", encoding="utf-8"):
        split_data = line.split()

        # our data
        date = split_data[0]
        time = split_data[1]
        latitude = split_data[2]
        longitude = split_data[3]
        depth = split_data[4]
        magnitude = split_data[6]
        location = split_data[8]

        data = {
            "date": date,
            "time": time,
            "latitude": latitude,
            "longitude": longitude,
            "depth": depth,
            "magnitude": magnitude,
            "location": location
        }

        all_data.append(data)

    output_json = "data.json"
    json_file = open(output_json, "w")
    json.dump(all_data, json_file, indent=4)

    return f"Json file {output_json} created !"
