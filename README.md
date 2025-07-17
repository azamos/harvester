# Harvester

A Python-based web scraper for extracting post data from hacker news (https://news.ycombinator.com/) into a CSV.

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
   ```

3. **Activate the virtual environment:**

   **On Windows:**

   ```bash
   venv\Scripts\activate
   ```

   **On macOS/Linux:**

   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

> **Note:** Currently tested on Windows Command Prompt, but should work on macOS and Linux as well. The application is currently in test mode and runs on locally stored pages.

### Basic Command Structure

```bash
python -m src.main --num_post NUM_POST --min_score MIN_SCORE --max_score MAX_SCORE --list_string LIST_STRING
```

### Parameters

- `--num_post`: Number of posts to process (positive integer)
- `--min_score`: Minimum score threshold (non-negative integer)
- `--max_score`: Maximum score threshold (non-negative integer, must be >= min_score)
- `--list_string`: Comma-separated list of positive integers (duplicates allowed)

### Example Usage

```bash
python -m src.main --num_post 50 --min_score 100 --max_score 200 --list_string 1,2,3
```

### Debug Mode

To view debug output, add the `--debug` flag:

```bash
python -m src.main --num_post 50 --min_score 100 --max_score 200 --list_string 1,2,3 --debug
```

## Dependencies

- `requests` - For making HTTP requests
- `beautifulsoup4` - For HTML parsing

## Sample Output

Below is a screenshot comparing the original Hacker News page and the extracted CSV output:

![Comparison Screenshot](assets/comparison.JPG)
