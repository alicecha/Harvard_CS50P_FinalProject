# National Park Hike Finder

#### Author
[@kryptaki](https://twitter.com/AliceChaverot)
<img src=./profile.png alt="profile picture" width="150" />

#### Video Demo
https://youtu.be/OGvaFRTcbxc
#### Description:
Discover the National Park Hike Finder — an intuitive Python program that puts the full list of National Park hikes at your fingertips. With the hike finder, get quick access to hike durations, when to visit, and brief descriptions, in the format of your choice. And if you need more detail, just click on the link to the hike's official website.

Have fun hiking!

#### How it works
The program prompts the user for the name of a national par. If the name is valid, it sends a call to the National Park Service (NPS) API and receives back the list of hikes. It then asks the user for their preferred output format (pdf, csv or table) and saves the list of hikes in the requested format.

##### Structure
The program runs on 3 python scripts:
- **`project.py`** receives national park as input and returns list of hikes with description in pdf, csv or table format.
- **`parks.py`** extracts park names and codes from parkcodes.csv and saves into `parks[]` list (source: [NPS](https://www.nps.gov/aboutus/foia/upload/NPS-Unit-List.xlsx))
- **`pdf.py`** provides the class to format PDF as needed.

The main functions in **`project.py`** are:

| Name	| Function |
| ----- | -------- | 
| `main()` | Takes park name as input and runs the program |
| `validate(str)` | Returns park code if park name str is valid, otherwise exits the program |
| `call_api(park)` | Takes object of class Park(name, code) and fetches all hikes for that prak from NPS API |
| `fetch_hikes(json)` | Takes API results as json file and returns list conatining all hike details (name, duration, seasons, decsription, url) |
| `get_format()` | Gets user preferred output format: pdf, csv or table (saved in .txt) |
| `create_output(park, list, str)` | Takes object of class Park(name, code) and list of hikes as input, and saves results in file format requested by user (.pdf, .csv or .txt) |


The other program files are:
- **`.env`** contains the NPS API key (which can be freely obtained from the [NPS website](https://www.nps.gov/subjects/developer/get-started.htm))
- **`requirements.txt`** contains all the libraries that need to be installed and imported for the program to run
- **`parkcodes.csv`** is a list of park names and codes (source: [NPS](https://www.nps.gov/aboutus/foia/upload/NPS-Unit-List.xlsx)
- **`test_project.py`** contains the unit tests for the program. It can be run with pytest.

#### Disclaimer
The information provided is only as good as that provided by the API. Some information may be missing - for example the API does not have any information on hikes in the Grand Canyon.

#### Coverage

The tool covers all US National Parks for which the NPS API contains hike information.

##### Parks included:
All national parks are included.

| Name	|
| ----- | 
|Acadia |
|Arches | 
| Badlands |
|Big Bend|
|Biscayne|
|Black Canyon of the Gunnison|
|Bryce Canyon|
|Canyonlands|
|Capitol Reef|
|Carlsbad|
|Caverns|
|Channel Islands|
|Congaree|
|Crater Lake|
|Cuyahoga Valley|
|Death Valley|
|Denali|
|Dry Tortugas|
|Everglades|
|Gates of the Arctic|
|Glacier|
|Glacier Bay|
|Grand Canyon|
|Grand Teton|
|Great Basin|
|Great Sand Dunes|
|Great Smoky Mountains|
|Guadalupe Mountains |
|Haleakala |
|Hawaii Volcanoes  |
|Hot Springs  |
|Isle Royale |
|Joshua Tree |
|Katmai  |
|Kenai Fjords |
|Kings Canyon |
|Kobuk Valley |
|Lake Clark   |
|Lassen Volcanic   |
|Mammoth Cave   |
|Mesa Verde  |
|Mount Rainier  |
|National Park of American Samoa	|
|North Cascades |
|Olympic    |
|Petrified Forest    |
|Pinnacles    |
|Redwood	|
|Rocky Mountain    |
|Saguaro |
|Sequoia  |
|Shenandoah  |
|Theodore Roosevelt   |
|Virgin Islands  |
|Voyageurs   |
|Wind Cave  |
|Wrangell-St. Elias  |
|Yellowstone   |
|Yosemite  |
|Zion  |


