# harvester

## Requirements

- Python 3.10+
- pip (Python package manager)

## Installation

1. **Clone or download the project:**

   ```bash
   git clone https://github.com/azamos/harvester
   cd harvester
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv

   # On Windows:
   venv\Scripts\activate

   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the scraper(CURRENTLY ONLY TEST MODE - Runs on locally stored pages):**
   The script expects arguments in the following format(replace '/' with '\' if using Windows cmd):
   python src/scraper.py --num_post NUM_POST --min_score MIN_SCORE --max_score MAX_SCORE --list_string
   LIST_STRING

   Replace NUM_POST with a positive integer, MIN_SCORE with a non-negative integer,
   MAX_SCORE with a non-negative integer >= MIN_SCORE, and --list_string with a comma seperated
   list of positive integer numbers(duplicates are fine)

   An example usage(bash):

   ```bash
   python src/main.py --num_post 50 --min_score 100 --max_score 200 --list_string 1,2,3
   ```

   # On Windows:

   python src\main.py --num_post 50 --min_score 100 --max_score 200 --list_string 1,2,3

   If you wish to view debug printings, please add the --debug flag lastly, like this:

   ```bash
   python src/main.py --num_post 50 --min_score 100 --max_score 200 --list_string 1,2,3 --debug
   ```

   # On Windows:

   python src\main.py --num_post 50 --min_score 100 --max_score 200 --list_string 1,2,3 --debug

## Dependencies

- `requests` - For making HTTP requests
- `beautifulsoup4` - For HTML parsing
