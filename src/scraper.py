import requests
from bs4 import BeautifulSoup
import csv
import argparse

DEFAULT_NUM_POST = 50
DEAULT_MIN_SCORE = 0
DEFAULT_MAX_SCORE = 10000
DEFAULT_SKIP_PAGES = {}

HELP_NUM_POST = "Maximum numbers of posts to scrape"
HELP_MIN_SCORE = "Filter: score >= "
HELP_MAX_SCORE = "Filter: score <="
HELP_SKIP_PAGES = "Specify a list of pages to skip, in the format --pages = p1,p2,p3"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_post",type=int,default=DEFAULT_NUM_POST,help=HELP_NUM_POST)
    parser.add_argument("--min_score",type=int,default=DEAULT_MIN_SCORE,help=HELP_MIN_SCORE)
    parser.add_argument("--max_score",type=int,default=DEFAULT_MAX_SCORE,help=HELP_MAX_SCORE)
    parser.add_argument("--list_string",type=str,default="",help=HELP_SKIP_PAGES)
    return parser.parse_args()

URL = "https://news.ycombinator.com/"

if __name__ == "__main__":
    args = parse_args()
    print("Trying to prase arguments...")
    try:
        print(args.num_post)
        print(args.min_score)
        print(args.max_score)
        s = args.list_string
        print(s)
        skip_pages = [int(i) for i in s.split(",") if i]
        print(f"The skip list is: {skip_pages}")
    except Exception as e:
        print(f"[WARN] something went wrong: {e}")