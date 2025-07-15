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
   python hackernews_scraper.py
   ```

2. **Run tests:**
   ```bash
   pytest
   ```

## Dependencies

- `requests` - For making HTTP requests
- `beautifulsoup4` - For HTML parsing
