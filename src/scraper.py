import requests
from bs4 import BeautifulSoup
import csv
import argparse
import os

SOURCE_URL = "https://news.ycombinator.com/"
TR_CLASS_NAME = "athing submission"
TITLE_A_CLASS_NAME = "titleline"
USER_CLASS_NAME = "hnuser"

debug_mode = False

NA = "NA"

#HTML fields and elements
HREF="href"
TR="tr"
ID="id"
SPAN="span"
A="a"
COMMENTS_SPLITTER = "\xa0"

#fields/features names
TITLE = "Title"
URL = "URL"
POINTS = "Points"
AUTHOR = "Author"
NUMBER_OF_COMMENTS = "Number of comments"
PAGE_NUMBER = "Page number"


DEFAULT_NUM_POST = 50
DEAULT_MIN_SCORE = 0
DEFAULT_MAX_SCORE = 10000
DEFAULT_SKIP_PAGES = {}

STATIC_FILE_PATH = "./htmlTestPages"
OUTPUT_FILE_PATH = "./output/result.csv"
HTM_SUFFIX = ".htm"
HTML_SUFFIX = ".html"

HELP_NUM_POST = "Maximum numbers of posts to scrape"
HELP_MIN_SCORE = "Filter: score >= "
HELP_MAX_SCORE = "Filter: score <="
HELP_SKIP_PAGES = "Specify a list of pages to skip, in the format --pages = p1,p2,p3"
HELP_DEBUG = "Allows debug mode"

def dbgprint(msg):
    if(debug_mode):
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

def extract_from_soup(soup,p_num):
    extracted_data = []
    for tr in soup.find_all(TR, class_ = TR_CLASS_NAME):
        id = tr[ID]
        title_td = tr.find(SPAN,class_ = TITLE_A_CLASS_NAME)
        title_a = title_td.find(A)
        title = title_a.get_text()
        url = title_a[HREF]
        # sibling = tr.next
        # print(sibling)

        #TODO: efficiency maybe can be improved by using parent or next
        score_sp = soup.find(SPAN,id = "score_"+id)
        score = NA
        #TODO: instead of checking for the missing score, it will be smarter to
        #check for missing "subline" class span(child of class="subtext" td - always present)
        if score_sp:#I've noticed that when score is missing, so is author - must validate this assumption
            score = score_sp.get_text()
            score_parent = score_sp.parent
            user_a = score_parent.find(A,class_ = USER_CLASS_NAME)
            author_name = user_a.get_text()
            author_link = user_a[HREF]
            comments_str = score_parent.find_all("a")[-1].get_text()
            num_comments = NA
            try:
                num_comments_str = comments_str.split(COMMENTS_SPLITTER)[0]#TODO: remove magic number
                num_comments = int(num_comments_str)
            except Exception as e:
                errprint(e)
        else:#have to set to NA since previous author_name and link might have values from the previous iteration
            author_name = NA
            author_link = NA

        extracted_data.append(
            {
            TITLE:title,
            URL: url,
            AUTHOR:{"name":author_name,"url":author_link},
            POINTS: score,
            NUMBER_OF_COMMENTS: num_comments,
            PAGE_NUMBER: p_num
            })
    return extracted_data

def save_to_csv(posts_list):
    os.makedirs(os.path.dirname(OUTPUT_FILE_PATH),exist_ok=True)
    fields = [TITLE,URL,AUTHOR,POINTS,NUMBER_OF_COMMENTS,PAGE_NUMBER]

    is_file_exists = os.path.exists(OUTPUT_FILE_PATH) and os.path.getsize(OUTPUT_FILE_PATH) > 0

    with open(OUTPUT_FILE_PATH,'a',newline='') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=fields)
        if not is_file_exists:
            writer.writeheader()
        for post_dict in posts_list:
            writer.writerow(post_dict)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_post",type=int,default=DEFAULT_NUM_POST,help=HELP_NUM_POST)
    parser.add_argument("--min_score",type=int,default=DEAULT_MIN_SCORE,help=HELP_MIN_SCORE)
    parser.add_argument("--max_score",type=int,default=DEFAULT_MAX_SCORE,help=HELP_MAX_SCORE)
    parser.add_argument("--list_string",type=str,default="",help=HELP_SKIP_PAGES)
    parser.add_argument("--debug",action="store_true",help=HELP_DEBUG)
    return parser.parse_args()



if __name__ == "__main__":
    print("Trying to prase arguments...")
    args = parse_args()
    try:
        debug_mode = args.debug
        dbgprint("DEBUG MODE ON!")
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
    extracted_data = []
    try:
        for i in range(1,2):
            i_soup = local_parser(STATIC_FILE_PATH+"/"+str(i)+HTM_SUFFIX)
            extracted_data += extract_from_soup(i_soup,i)
    except Exception as e:
        errprint(f"Error during scraping: {e}")

    dbgprint(f"Extracted data: {extracted_data}")
    print("Writing data to csv...")
    try:
        save_to_csv(extracted_data)
    except Exception as e:
        errprint(f"Saving to CSV failed: {e}")
    print("DONE")