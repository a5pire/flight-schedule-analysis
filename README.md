###Flight Schedule Analysis

---

A simple command line interface parses flight schedule information from 
a specific text file format and further analyses the generated JSON for 
potentially fatiguing pilot duties. Output is presented to the terminal for
visual analysis while a JSON file is generated and inserted into a MongoDB Atlas
Database.
---
### Table of Contents

-   [Description](#Description)
-   [Installation](#Installation)
-   [Usage](#Usage)
-   [Learning Outcomes](#Learning-Outcomes)
---

### Installation
So far, this project has only been tested on a linux platform and Python 2 is not supported.
1. Clone this repo to a local directory
2. [optional] - Create and activate a virtual environment
3. Run this command: `pip install -r requirements.txt`
---

### Usage
In order to use this project, you'll need access to the specific text file
(`trip_report`) generated with all the published flight information.

#### options
- `-i` the absolute file path of the input file (flight schedule text file).
- `-o` the absolute file path of the output file. If this is omitted `output_file.json` will
automatically be generated. This will be generated into the parent directory along side `main.py`

To run the project:
1. `cd` into the top level directory
2. Open `mongo.py` and on line 16, replace `os.getenv('connection_string')` with your
connection string to your MongoDB Atlas Cluster.
3. Run: `python main.py -i <trip_report_file_location> -o <output_file_location>`
---
### Learning Outcomes
- Iteration and looping
- Reading and writing JSON files
- Database integration
- Supplying command line arguments
- Object orientation
- Usage of `requirements.txt`
- Mark down
---