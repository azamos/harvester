import requests
from bs4 import BeautifulSoup
import csv
import argparse

URL = "https://news.ycombinator.com/"
TR_CLASS_NAME = "athing submission"
TITLE_A_CLASS_NAME = "titleline"

#fields/features names
TITLE = "Title"


DEFAULT_NUM_POST = 50
DEAULT_MIN_SCORE = 0
DEFAULT_MAX_SCORE = 10000
DEFAULT_SKIP_PAGES = {}

STATIC_FILE_PATH = "./htmlTestPages"
HTM_SUFFIX = ".htm"
HTML_SUFFIX = ".html"

HELP_NUM_POST = "Maximum numbers of posts to scrape"
HELP_MIN_SCORE = "Filter: score >= "
HELP_MAX_SCORE = "Filter: score <="
HELP_SKIP_PAGES = "Specify a list of pages to skip, in the format --pages = p1,p2,p3"

def dbgprint(msg):
    print(f"[DEBUG] {msg}")

def errprint(msg):
    print(f"[ERROR] {msg}")


#Temp: extract the data from locally downloaded html pages of the intended target site
#TODO 1: Switch to lxml parser instead (suggested by BeautifulSoup documentation)
#TODO 2: When working locally, swap to fetch from online and cache
def local_parser(file_path):
    dbgprint(f"Parsing for: {file_path}")
    with open(file_path,"r",encoding="utf-8") as f:
        html = f.read()
    return BeautifulSoup(html,"html.parser")

#TODO: add filtering function

def extract_from_soup(soup):
    extracted_data = {}
    for tr in soup.find_all('tr', class_ = TR_CLASS_NAME):
        title_td = tr.find("span",class_ = TITLE_A_CLASS_NAME)
        # dbgprint(title_td)
        title = title_td.find("a").get_text()
        id = title_td.parent.parent["id"] #TODO:horrendous: remove later
        # dbgprint(f"title = {title}")
        extracted_data[id] = {TITLE:title}
    return extracted_data



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_post",type=int,default=DEFAULT_NUM_POST,help=HELP_NUM_POST)
    parser.add_argument("--min_score",type=int,default=DEAULT_MIN_SCORE,help=HELP_MIN_SCORE)
    parser.add_argument("--max_score",type=int,default=DEFAULT_MAX_SCORE,help=HELP_MAX_SCORE)
    parser.add_argument("--list_string",type=str,default="",help=HELP_SKIP_PAGES)
    return parser.parse_args()



if __name__ == "__main__":
    args = parse_args()
    dbgprint("Trying to prase arguments...")
    try:
        dbgprint(args.num_post)
        dbgprint(args.min_score)
        dbgprint(args.max_score)
        s = args.list_string
        dbgprint(s)
        skip_pages = [int(i) for i in s.split(",") if i]
        dbgprint(f"The skip list is: {skip_pages}")
    except Exception as e:
        errprint(f"something went wrong with argument parsing: {e}")
    dbgprint("After argument parsing...")
    extracted_data = {}
    try:
        for i in range(1,2):
            x = local_parser(STATIC_FILE_PATH+"/"+str(i)+HTM_SUFFIX)
            extracted_data[str(i)] = extract_from_soup(x)
    except Exception as e:
        errprint(f"something went wrong with scraping: {e}")

    dbgprint(f"Extracted data: {extracted_data}")
    print("DONE")