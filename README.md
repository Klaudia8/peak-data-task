peak-data-task
=============
Names extracting tool from publications data

### Usage

Requirements:
* Python 3.8 with virtualenv

1. Create virutalenv with `python -m venv`
2. Activate virtualenv with `source /your_venv_paht/bin/activate`
3. Install project requirements with `pip install -r requirements.txt`
4. Ensure that data is available in `data/publications_min.csv`
5. Execute code by `python main.py`

### Approach
1. Firstly separate list of names to unique records.
2. Then take last word for the record as surname. In case of surnames with some defined parts of surname such as: [van, der, etc.] take the surnames after this part.
3. Take the name as the rest of record.
4. With list of names and surnames in dataframe, find duplicates. It sorts the records by surname, length of name and find duplicates if the abbreviation of the name is the same and has the length of 1. Then it deletes duplicated records.

### Failure points
1. In the file there are surnames with initials or full name with second name as initial. The code doesn't differ between these people and find them unique. Better approach could be applied using Google API or the library with list of names and surnames.
2. The records with initials should be either deleted or replaced with full name, based on searching the Internet.

### Next steps
1. Improvement of algorithm for finding unique people, e.g. by downloading the full names from Google API or other websites.
2. Testing the code with unit tests.