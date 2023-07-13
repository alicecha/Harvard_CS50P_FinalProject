import os
from dotenv import load_dotenv

import sys
import requests
import json
import re
from decimal import Decimal
import inquirer
import csv
import pandas as pd
from tabulate import tabulate

from parks import parks
from pdf import PDF

"""
Loads environment variable (API key)
"""
load_dotenv()
NPS_API_KEY = os.getenv('NPS_API_KEY')

"""
Park class which sets the properties of park objects
"""
class Park():
    def __init__(self, name, code):
        self.name = name
        self.code = code

    def __str__(self):
        return f"{self.name} ({self.code})"

"""
Hike class which sets the properties of hike objects
"""
class Hike():
    def __init__(self, name, duration = None, seasons = None, description = None, url = None):
        self.name = name
        self.duration = duration
        self.seasons = seasons
        self.description = description
        self.url = url
    
    def __str__(self):
        return f"{self.name}, duration: {self.duration}"
    
    @property
    def name(self):
        return self._name
    
    """
    Standardises hike name format: removes "hike" and adds "trail" if not already included
    """
    @name.setter
    def name(self, name):
        if not name.endswith(" Trail"):
            name = name + " Trail"
        self._name = name.strip("Hike").strip()

    @property
    def duration(self):
        return self._duration
    
    """
    Saves hike duration as average of min and max duration
    """
    @duration.setter
    def duration(self, duration):
        if matches := re.match(r"(\d+)\s(Minutes|Hours)", duration, re.IGNORECASE):
            duration, unit = matches.groups()
            self._duration = f"{Decimal(duration)} {unit.lower()}"
        elif matches := re.match(r"(\d+)-(\d+)\s(Minutes|Hours)", duration, re.IGNORECASE):
            min, max, unit = matches.groups()
            ave_duration = (int(min) + int(max)) / 2
            self._duration = f"{Decimal(ave_duration)} {unit.lower()}"
        else:
            sys.exit("Duration in wrong format")
    
    """
    Reads seasons as string rather than list
    """
    @property
    def seasons(self):
        return ', '.join(self._seasons)
    
    @seasons.setter
    def seasons(self, seasons):
        self._seasons = seasons
    
    @property
    def description(self):
        return self._description
    
    """
    Cleans description of html formatting
    """
    @description.setter
    def description(self, description):
        self._description = description.replace("\u00a0", "").strip().encode('utf-8').decode('latin-1')

    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, url):
        self._url = url

"""
Takes park name as input and returns list of hike in pdf, csv or table format
"""
def main():
    p = validate(input("Park Name: "))
    park = Park(p["name"], p["code"])
    hikes = fetch_hikes(call_api(park))
    output_format = get_format()
    create_output(park, hikes, output_format)

"""
Returns park code if name is valid, otherwise exits programme
"""
def validate(str):
    try:
        return next(p for p in parks if p["name"] == str.strip().title())
    except StopIteration:
        sys.exit("Park name not valid. For a list of valid names, please refer to README.md (Coverage section)")

"""
Fetches park hikes and description from NPS API, returns hikes as list
""" 
def call_api(park):
    print(f"Fetching hikes for {park.name}...")
    response = requests.get(f"https://developer.nps.gov/api/v1/thingstodo?parkCode={park.code}&q=BFF8C027-7C8F-480B-A5F8-CD8CE490BFBA&api_key={NPS_API_KEY}").json()
    # Save response in json file
    with open("results.json", "w") as outfile:
        outfile.write(json.dumps(response, indent = 4))
    return response

def fetch_hikes(response):
    hikes = []
    for d in response["data"]:
        hike = Hike(d['title'], d['duration'], d['season'], d['longDescription'], d['url'])
        hikes.append({'name': hike.name, 'duration': hike.duration, 'seasons': hike.seasons, 'description': hike.description, 'url': hike.url})
    if hikes:
        return hikes
    else:
        sys.exit("No hikes could be found.")

"""
Prompts user for output format (must select from list) and returns user choice
"""
def get_format():
    options = ['pdf', 'csv', 'table']
    question = [
        inquirer.List('format',
                      message="What format do you want the output in?",
                      choices=options,
                      ),
    ]
    answer = inquirer.prompt(question)
    return answer['format']

"""
Creates output in format chosen by user
"""
def create_output(park, list, format):
    
    file_name = park.name.replace(" ", "_").lower()

    match format:
        case "pdf":
            print(f"Saving hikes to {file_name}.pdf...")
            pdf = PDF()
            pdf.add_page()
            pdf.title(f"{park.name} Park hikes")
            for i, item in enumerate(sorted(list, key=lambda i: i["name"])):
                pdf.print_para(
                    num=i+1,
                    title=item["name"],
                    link=item["url"],
                    subtitle=f"Duration: {str(item['duration'])}",
                    subtitle_bold=f"Best season to visit: {item['seasons']}",
                    body=item["description"]
                )
            pdf.output(f"{file_name}.pdf")
        
        case "csv":
            print(f"Saving hikes to {file_name}.csv...")
            with open(f"{file_name}.csv", "w") as file:
                writer = csv.DictWriter(file, fieldnames=["name", "link", "duration", "seasons", "description"])
                writer.writeheader()
                for item in sorted(list, key=lambda i: i["name"]):
                    writer.writerow({"name": item['name'], "link": item["url"], "duration": item['duration'], "seasons": item['seasons'], "description": item['description']})
        
        case "table":
            print(f"Saving hikes to {file_name}.txt...")
            df = pd.DataFrame.from_records(list)
            with open(f"{file_name}.txt", "w") as file:
                file.write(f"{park.name} Park hikes\n\n")
                file.write(
                    tabulate(
                        df[["name", "duration", "seasons", "url"]],
                        headers="keys",
                        tablefmt = "grid",
                        showindex="never"
                    )
                )

        case _:
            sys.exit("No document produced")


    

if __name__ == "__main__":
    main()
    