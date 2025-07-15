# harvester

## Requirements

- Python 3.1+
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

1. **Run the scraper:**

   ```bash
   python src/scraper.py --num_post 5 --min_score 10 --max_score 1000 --list_string 1,2,3
   ```

   Replace the ingegers after num_post, min_score and max_score as you wish. The list_string expects integers in a similar format.

## Dependencies

- `requests` - For making HTTP requests
- `beautifulsoup4` - For HTML parsing
